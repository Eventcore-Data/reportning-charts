"""
Pydantic models for request/response schemas.
"""

from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class GridOptions(BaseModel):
    """Options for chart grid lines."""
    enabled: bool = Field(default=True, description="Show grid lines")
    linestyle: Literal['solid', 'dashed', 'dotted'] = Field(
        default='solid', description="Grid line style"
    )
    alpha: Optional[float] = Field(
        default=None, description="Grid opacity (0.0-1.0). None uses theme default."
    )


class FontOptions(BaseModel):
    """Options for chart fonts."""
    family: Optional[str] = Field(default=None, description="Font family (e.g. 'serif', 'monospace'). None uses theme default.")
    title_size: Optional[int] = Field(default=None, description="Title font size. None uses theme default.")
    label_size: Optional[int] = Field(default=None, description="Axis label font size. None uses theme default.")
    tick_size: Optional[int] = Field(default=None, description="Tick label font size. None uses theme default.")


class UnitFormat(BaseModel):
    """Formatting options for axis tick labels."""
    x_prefix: str = Field(default='', description="Prefix for x-axis values (e.g. '$')")
    x_suffix: str = Field(default='', description="Suffix for x-axis values (e.g. '%')")
    y_prefix: str = Field(default='', description="Prefix for y-axis values (e.g. '$')")
    y_suffix: str = Field(default='', description="Suffix for y-axis values (e.g. '%')")


class DataLabelOptions(BaseModel):
    """Options for showing data labels on chart elements."""
    show: bool = Field(default=False, description="Show data labels on chart elements")
    format: Optional[str] = Field(default=None, description="Python format string for labels (e.g. ',.0f' for thousands)")


class ChartRequest(BaseModel):
    """Request model for chart generation."""
    file_id: str = Field(..., description="ID of the uploaded file")
    chart_type: str = Field(default='auto', description="Type of chart: auto, line, bar, scatter, pie")
    theme: str = Field(default='professional', description="Chart theme")
    format: str = Field(default='png', description="Output format: png, pdf, svg")
    title: Optional[str] = Field(None, description="Custom chart title")
    dpi: int = Field(default=300, description="Image resolution (DPI)")
    xlabel: Optional[str] = Field(None, description="Custom x-axis label")
    ylabel: Optional[str] = Field(None, description="Custom y-axis label")
    colors: Optional[List[str]] = Field(None, description="Custom color list (hex codes) to override theme colors")
    grid: Optional[GridOptions] = Field(default=None, description="Grid customization")
    fonts: Optional[FontOptions] = Field(default=None, description="Font customization")
    units: Optional[UnitFormat] = Field(default=None, description="Axis tick label formatting (prefix/suffix)")
    data_labels: Optional[DataLabelOptions] = Field(default=None, description="Data label display options")

    @field_validator('colors')
    @classmethod
    def colors_must_not_be_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError('colors list must not be empty')
        return v


class DataPreview(BaseModel):
    """Response model for data preview."""
    columns: List[str] = Field(..., description="Column names from Excel")
    rows: List[List[Any]] = Field(..., description="Preview rows")
    total_rows: int = Field(..., description="Total number of rows in dataset")
    row_count: int = Field(..., description="Number of rows in preview")


class UploadResponse(BaseModel):
    """Response model for file upload."""
    file_id: str = Field(..., description="Unique identifier for uploaded file")
    filename: str = Field(..., description="Original filename")
    data_preview: DataPreview = Field(..., description="Preview of the data")
    message: str = Field(default="File uploaded successfully")


class ChartResponse(BaseModel):
    """Response model for chart generation."""
    chart_base64: str = Field(..., description="Base64 encoded chart image")
    format: str = Field(..., description="Chart format")
    filename: str = Field(..., description="Suggested filename for download")


class ThemeInfo(BaseModel):
    """Information about a single theme."""
    name: str
    description: str
    colors: List[str]
    background: str
    grid_color: str
    grid_alpha: float
    font_family: str
    title_size: int
    label_size: int
    tick_size: int


class ThemesResponse(BaseModel):
    """Response model for available themes."""
    themes: dict[str, ThemeInfo]
    default_theme: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
