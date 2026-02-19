"""
Chart Service
Refactored ChartMaker class for API usage with support for base64 encoding.
"""

import base64
import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for API
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter


class ChartService:
    """Service class for generating charts from Excel data."""

    def __init__(self, theme='professional'):
        """Initialize the chart service with a theme."""
        self.theme = theme
        self.theme_config = self._load_theme()
        self._apply_theme()

    def _load_theme(self):
        """Load theme configuration from JSON file."""
        config_path = Path(__file__).parent.parent / 'config' / 'themes.json'
        try:
            with open(config_path, 'r') as f:
                themes = json.load(f)
                if self.theme in themes['themes']:
                    return themes['themes'][self.theme]
                else:
                    default_theme = themes['default_theme']
                    return themes['themes'][default_theme]
        except Exception as e:
            print(f"Error loading theme: {e}")
            return self._get_default_theme()

    def _get_default_theme(self):
        """Return a basic default theme if config file can't be loaded."""
        return {
            "colors": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E"],
            "background": "#FFFFFF",
            "grid_color": "#E0E0E0",
            "grid_alpha": 0.3,
            "font_family": "sans-serif",
            "title_size": 16,
            "label_size": 12,
            "tick_size": 10
        }

    def _apply_theme(self, font_overrides=None, grid_overrides=None):
        """Apply theme settings to matplotlib, with optional overrides."""
        tc = self.theme_config

        rcParams['figure.facecolor'] = tc['background']
        rcParams['axes.facecolor'] = tc['background']

        # Font settings (allow overrides)
        rcParams['font.family'] = (font_overrides.get('family') or tc['font_family']) if font_overrides else tc['font_family']
        rcParams['axes.titlesize'] = (font_overrides.get('title_size') or tc['title_size']) if font_overrides else tc['title_size']
        rcParams['axes.labelsize'] = (font_overrides.get('label_size') or tc['label_size']) if font_overrides else tc['label_size']
        tick_size = (font_overrides.get('tick_size') or tc['tick_size']) if font_overrides else tc['tick_size']
        rcParams['xtick.labelsize'] = tick_size
        rcParams['ytick.labelsize'] = tick_size

        # Grid settings (allow overrides)
        if grid_overrides:
            rcParams['axes.grid'] = grid_overrides.get('enabled', True)
            rcParams['grid.alpha'] = grid_overrides.get('alpha') or tc['grid_alpha']
            rcParams['grid.color'] = tc['grid_color']
            linestyle_map = {'solid': '-', 'dashed': '--', 'dotted': ':'}
            rcParams['grid.linestyle'] = linestyle_map.get(grid_overrides.get('linestyle', 'solid'), '-')
        else:
            rcParams['axes.grid'] = True
            rcParams['grid.alpha'] = tc['grid_alpha']
            rcParams['grid.color'] = tc['grid_color']

        # Set seaborn style
        sns.set_palette(tc['colors'])

    @staticmethod
    def load_themes() -> Dict:
        """Load all available themes from config."""
        config_path = Path(__file__).parent.parent / 'config' / 'themes.json'
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading themes: {e}")
            return {"themes": {}, "default_theme": "professional"}

    def read_excel(self, file_path: str, sheet_name: int = 0) -> pd.DataFrame:
        """Read data from Excel file."""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return df
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {e}")

    def get_data_preview(self, df: pd.DataFrame, max_rows: int = 100) -> Dict:
        """Get a preview of the dataframe for display."""
        return {
            "columns": df.columns.tolist(),
            "rows": df.head(max_rows).values.tolist(),
            "total_rows": len(df),
            "row_count": min(max_rows, len(df))
        }

    def create_chart(self, df: pd.DataFrame, chart_type: str = 'auto',
                     title: Optional[str] = None, xlabel: Optional[str] = None,
                     ylabel: Optional[str] = None,
                     colors: Optional[List[str]] = None,
                     units: Optional[Dict] = None,
                     data_labels: Optional[Dict] = None):
        """Create a chart from the dataframe."""
        effective_colors = colors if colors else self.theme_config['colors']

        fig, ax = plt.subplots(figsize=(10, 6))

        # Auto-detect chart type if needed
        if chart_type == 'auto':
            chart_type = self._detect_chart_type(df)

        # Create the appropriate chart type (sets auto-detected labels from column names)
        if chart_type == 'line':
            self._create_line_chart(df, ax, colors=effective_colors)
        elif chart_type == 'bar':
            self._create_bar_chart(df, ax, colors=effective_colors, data_labels=data_labels)
        elif chart_type == 'scatter':
            self._create_scatter_chart(df, ax, colors=effective_colors, data_labels=data_labels)
        elif chart_type == 'pie':
            self._create_pie_chart(df, ax, colors=effective_colors, data_labels=data_labels)
        else:
            self._create_line_chart(df, ax, colors=effective_colors)

        # Set title and labels AFTER chart creation so user values override auto-detected ones
        if title:
            ax.set_title(title, fontweight='bold', pad=20)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)

        # Apply unit formatting to axes
        if units:
            x_pre = units.get('x_prefix', '')
            x_suf = units.get('x_suffix', '')
            if x_pre or x_suf:
                ax.xaxis.set_major_formatter(
                    FuncFormatter(lambda val, pos, p=x_pre, s=x_suf: f"{p}{val:g}{s}")
                )
            y_pre = units.get('y_prefix', '')
            y_suf = units.get('y_suffix', '')
            if y_pre or y_suf:
                ax.yaxis.set_major_formatter(
                    FuncFormatter(lambda val, pos, p=y_pre, s=y_suf: f"{p}{val:g}{s}")
                )

        plt.tight_layout()
        return fig

    def _detect_chart_type(self, df: pd.DataFrame) -> str:
        """Auto-detect appropriate chart type based on data."""
        if len(df.columns) >= 2:
            return 'line'
        return 'bar'

    def _create_line_chart(self, df: pd.DataFrame, ax, colors: Optional[List[str]] = None):
        """Create a line chart."""
        effective_colors = colors or self.theme_config['colors']
        x_col = df.columns[0]
        for i, col in enumerate(df.columns[1:]):
            color = effective_colors[i % len(effective_colors)]
            ax.plot(df[x_col], df[col], marker='o', linewidth=2, markersize=6,
                    label=col, color=color)

        ax.legend(frameon=True, fancybox=True, shadow=True)
        ax.set_xlabel(x_col)
        plt.xticks(rotation=45, ha='right')

    def _create_bar_chart(self, df: pd.DataFrame, ax,
                          colors: Optional[List[str]] = None,
                          data_labels: Optional[Dict] = None):
        """Create a bar chart."""
        effective_colors = colors or self.theme_config['colors']
        x_col = df.columns[0]

        if len(df.columns) == 2:
            bars = ax.bar(df[x_col], df[df.columns[1]], color=effective_colors[0])
            ax.set_xlabel(x_col)
            ax.set_ylabel(df.columns[1])
            if data_labels and data_labels.get('show'):
                fmt = data_labels.get('format')
                ax.bar_label(bars, fmt=f'{{:{fmt}}}' if fmt else None, padding=3)
        else:
            df_plot = df.set_index(x_col)
            df_plot.plot(kind='bar', ax=ax, color=effective_colors)
            ax.legend(frameon=True, fancybox=True, shadow=True)
            if data_labels and data_labels.get('show'):
                fmt = data_labels.get('format')
                for container in ax.containers:
                    ax.bar_label(container, fmt=f'{{:{fmt}}}' if fmt else None, padding=3)

        plt.xticks(rotation=45, ha='right')

    def _create_scatter_chart(self, df: pd.DataFrame, ax,
                              colors: Optional[List[str]] = None,
                              data_labels: Optional[Dict] = None):
        """Create a scatter plot."""
        if len(df.columns) < 2:
            raise ValueError("Scatter plot requires at least 2 columns")

        effective_colors = colors or self.theme_config['colors']
        x_col = df.columns[0]
        y_col = df.columns[1]

        ax.scatter(df[x_col], df[y_col], s=100, alpha=0.6,
                   color=effective_colors[0], edgecolors='black', linewidth=1)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

        if data_labels and data_labels.get('show'):
            fmt_spec = data_labels.get('format') or 'g'
            for x_val, y_val in zip(df[x_col], df[y_col]):
                label_text = format(y_val, fmt_spec) if isinstance(y_val, (int, float)) else str(y_val)
                ax.annotate(label_text, (x_val, y_val),
                           textcoords="offset points", xytext=(5, 5),
                           fontsize=8, alpha=0.8)

    def _create_pie_chart(self, df: pd.DataFrame, ax,
                          colors: Optional[List[str]] = None,
                          data_labels: Optional[Dict] = None):
        """Create a pie chart."""
        if len(df.columns) < 2:
            raise ValueError("Pie chart requires at least 2 columns (labels and values)")

        effective_colors = colors or self.theme_config['colors']
        labels = df[df.columns[0]]
        values = df[df.columns[1]]

        if data_labels and data_labels.get('show') and data_labels.get('format'):
            fmt = data_labels['format']
            autopct = lambda pct: f'{pct:{fmt}}%'
        else:
            autopct = '%1.1f%%'

        ax.pie(values, labels=labels, autopct=autopct, startangle=90,
               colors=effective_colors)
        ax.axis('equal')

    def save_chart_to_file(self, fig, output_path: str, format: str = 'png', dpi: int = 300):
        """Save the chart to a file."""
        try:
            fig.savefig(output_path, format=format, dpi=dpi, bbox_inches='tight')
            return output_path
        except Exception as e:
            raise ValueError(f"Error saving chart: {e}")
        finally:
            plt.close(fig)

    def chart_to_base64(self, fig, format: str = 'png', dpi: int = 300) -> str:
        """Convert chart figure to base64 encoded string."""
        try:
            buffer = io.BytesIO()
            fig.savefig(buffer, format=format, dpi=dpi, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            return img_base64
        except Exception as e:
            raise ValueError(f"Error encoding chart: {e}")
        finally:
            buffer.close()
            plt.close(fig)

    def chart_to_bytes(self, fig, format: str = 'png', dpi: int = 300) -> bytes:
        """Convert chart figure to bytes."""
        try:
            buffer = io.BytesIO()
            fig.savefig(buffer, format=format, dpi=dpi, bbox_inches='tight')
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            raise ValueError(f"Error converting chart to bytes: {e}")
        finally:
            buffer.close()
            plt.close(fig)

    def generate_chart(self, file_path: str, chart_type: str = 'auto',
                       format: str = 'png', dpi: int = 300,
                       title: Optional[str] = None,
                       return_base64: bool = True,
                       xlabel: Optional[str] = None,
                       ylabel: Optional[str] = None,
                       colors: Optional[List[str]] = None,
                       grid: Optional[Dict] = None,
                       fonts: Optional[Dict] = None,
                       units: Optional[Dict] = None,
                       data_labels: Optional[Dict] = None) -> Tuple[Any, pd.DataFrame]:
        """
        Generate a chart from an Excel file.

        Returns:
            Tuple of (chart_data, dataframe) where chart_data is either base64 string or bytes
        """
        # Re-apply theme with any font/grid overrides
        if fonts or grid:
            self._apply_theme(font_overrides=fonts, grid_overrides=grid)

        df = self.read_excel(file_path)

        if not title:
            title = Path(file_path).stem.replace('_', ' ').title()

        fig = self.create_chart(
            df, chart_type=chart_type, title=title,
            xlabel=xlabel, ylabel=ylabel,
            colors=colors, units=units, data_labels=data_labels
        )

        if return_base64:
            chart_data = self.chart_to_base64(fig, format=format, dpi=dpi)
        else:
            chart_data = self.chart_to_bytes(fig, format=format, dpi=dpi)

        return chart_data, df
