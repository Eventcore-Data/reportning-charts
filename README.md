# Excel Chart Maker

A full-stack tool that generates publication-ready charts from Excel data files (.xlsx, .xls, .xlsm). It has a React web UI, a FastAPI backend, and a standalone CLI tool (`chart_maker.py`).

## The Problem

When working with data in Excel and creating charts for reports or documents:
- Copy-pasting charts from Excel to Word often results in skewed, distorted, or improperly scaled visualizations
- Chart formatting frequently breaks during the transfer
- Manual reformatting wastes time and produces inconsistent results
- The final output rarely looks as professional as intended

## The Solution

Excel Chart Maker is a Python-based tool that:
- Reads data directly from Excel files (.xlsx, .xls, .xlsm)
- Generates high-quality, publication-ready charts
- Exports charts as image files (PNG, SVG, PDF) ready to insert into reports
- Ensures consistent formatting and scaling every time
- Produces professional visualizations suitable for presentations and documents

## Features

- **Web Interface & CLI**: Use the modern web UI or command-line interface
- **Interactive Plotly Charts**: Zoom, pan, hover tooltips, and camera-icon PNG download — all client-side via Plotly.js
- **Inline Chart Editing**: Click any title or axis label directly on the chart to rename it
- **Drag to Reposition**: Drag the legend or annotations to any position; layout is preserved on download
- **Undo History**: Up to 20-step undo with a single button click
- **Multiple Chart Types**: Line, bar, horizontal bar, scatter, and pie charts — plus auto-detect
- **Multi-Section Excel Files**: Automatically detects multiple data tables in a single sheet and renders one chart per section
- **Ratings Mode**: Horizontal bar charts color-coded red/yellow/green by configurable thresholds with vertical reference lines
- **Trend Lines**: Independent linear regression and mean lines, each with custom color, dash style, and legend label
- **Per-Bar Colors**: Individual color overrides for each bar in single-series charts
- **Data Labels**: Show values on chart elements with an optional Python format string (e.g. `,.0f` for thousands)
- **Unit Formatting**: Add prefix/suffix to axis tick labels (e.g. `$`, `%`, `k`)
- **Font & Grid Customization**: Override font family, title/label/tick sizes, grid style, and opacity per chart
- **4 Professional Themes**: Professional, Minimal, Vibrant, Academic
- **Excel Integration**: Reads data directly from Excel spreadsheets, auto-detects leading title rows and spacer columns
- **High-Quality Export**: PNG, PDF, or SVG — DPI configurable from 150 to 600
- **Data Review Modal**: Expand the data table to inspect all rows and all detected sections before charting

## Installation

Choose between the **Web UI** (recommended) or **CLI** (for automation):

### Web UI Setup (Recommended)

**Backend (FastAPI):**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend (React + Tailwind):**
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

### CLI Setup

**Prerequisites:** Python 3.8 or higher, pip

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI tool
python chart_maker.py --input data.xlsx
```

## Usage

### Web UI Usage (Recommended)

1. **Start the servers:**
   - Backend: `cd backend && uvicorn app.main:app --reload` (http://localhost:8000)
   - Frontend: `cd frontend && npm run dev` (http://localhost:5173)

2. **Create charts in 4 easy steps:**
   - **Step 1:** Drag & drop your Excel file or click to browse
   - **Step 2:** Review your data in the preview table (click "View all rows" to open the full modal)
   - **Step 3:** Choose chart type, theme, colors, and other options, then click **Generate Chart**
   - **Step 4:** Use the **camera icon** in the Plotly toolbar to download as PNG, or right-click the chart for more options

**Advanced features:**
- **Multi-section files**: When multiple data tables are detected in one sheet, each gets its own chart card automatically
- **Ratings mode**: Enable in chart options to color horizontal bars red/yellow/green based on configurable thresholds
- **Trend lines**: Toggle linear regression or mean line from the chart options panel
- **Inline editing**: Click any title or axis label on the rendered chart to edit it in place
- **Undo**: Click the undo button (Undo) next to Generate to restore the previous chart state
- **Reposition legend**: Drag the legend anywhere on the chart before downloading

**Options panel summary:**
- 5 chart types: Auto, Line, Bar, Horizontal Bar, Scatter, Pie
- 4 themes: Professional, Minimal, Vibrant, Academic
- Custom title, x/y axis labels
- Custom color palette or per-bar colors
- Data labels with format string
- Unit prefix/suffix for each axis
- Font family and size overrides
- Grid style and opacity

### CLI Usage

**Basic Usage**

1. Prepare your Excel file with data in a structured format (rows/columns)

2. Run the chart maker:
```bash
python chart_maker.py --input data.xlsx --output charts/
```

3. Find your generated charts in the output directory, ready to insert into Word, PowerPoint, or any document

### Command Line Options

```bash
python chart_maker.py [options]

Options:
  --input, -i      Path to input Excel file (required)
  --output, -o     Output directory for charts (default: ./output)
  --type, -t       Chart type: line, bar, scatter, pie (default: auto-detect)
  --format, -f     Output format: png, svg, pdf (default: png)
  --theme          Color theme: professional, minimal, vibrant, academic (default: professional)
  --dpi            Image resolution for PNG (default: 300)
  --title          Custom chart title
```

### Example

```bash
# Generate a bar chart from sales data
python chart_maker.py -i sales_data.xlsx -t bar -f png -o reports/charts/

# Generate high-res PDF charts
python chart_maker.py -i quarterly_data.xlsx -f pdf --dpi 600
```

## Excel File Format

Your Excel file should be structured with:
- First row: Column headers (will be used as labels)
- Subsequent rows: Data values
- Multiple sheets supported
- **Multi-section files**: Separate data tables with blank rows between them — each section is auto-detected and charted independently
- Leading title rows and spacer columns are automatically stripped

**Standard (line/bar charts):**
```
| Month    | Sales | Expenses |
|----------|-------|----------|
| January  | 5000  | 3000     |
| February | 6000  | 3200     |
| March    | 5500  | 3100     |
| April    | 7200  | 3500     |
| May      | 6800  | 3400     |
| June     | 7500  | 3600     |
```

**Ratings (horizontal bar with color thresholds):**
```
| Category        | Score |
|-----------------|-------|
| Communication   | 4.10  |
| Collaboration   | 2.90  |
| Innovation      | 3.50  |
| Leadership      | 3.80  |
| Delivery        | 2.75  |
```

## Output

Charts are exported as standalone image files that can be:
- Inserted directly into Word documents without distortion
- Used in PowerPoint presentations
- Included in reports and publications
- Shared with collaborators

## API Endpoints

The FastAPI backend exposes the following endpoints (docs at http://localhost:8000/docs):

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload an Excel file; returns `file_id` and data preview |
| `POST` | `/api/chart-data` | Generate Plotly traces + layout for client-side rendering |
| `POST` | `/api/generate` | Generate a chart server-side; returns base64 PNG/PDF/SVG |
| `GET` | `/api/chart/{file_id}` | Download a chart directly as a file |
| `GET` | `/api/themes` | List all available themes and their configurations |
| `DELETE` | `/api/cleanup/{file_id}` | Delete uploaded file and generated charts |

### POST /api/chart-data (primary web UI endpoint)

**Request:**
```json
{
  "file_id": "uuid-string",
  "chart_type": "auto",
  "theme": "professional",
  "title": "Monthly Sales",
  "xlabel": "Month",
  "ylabel": "Revenue",
  "colors": ["#2E86AB", "#A23B72"],
  "show_data_labels": false,
  "show_linear_trend": false,
  "show_mean_line": false,
  "ratings_mode": false,
  "ratings_low_threshold": 3.15,
  "ratings_high_threshold": 3.85,
  "bar_colors": null,
  "section_index": 0
}
```

**Response:** Plotly `traces` array and `layout` object for use with Plotly.js.

## Testing

The backend has a full pytest test suite:

```bash
cd backend
pytest                          # run all tests
pytest --cov=app tests/         # with coverage report
pytest tests/test_upload.py     # single test module
```

Test files cover: health check, file upload, chart-data endpoint, chart generation, download, cleanup, themes, and end-to-end flows.

## Technology Stack

**Backend:**
- **FastAPI**: Modern Python web framework
- **pandas**: Excel file reading and data manipulation
- **matplotlib / seaborn**: Server-side chart generation (CLI + `/api/generate`)
- **openpyxl / xlrd**: Excel file parsing
- **Pydantic**: Request/response validation
- **pytest / httpx**: Backend test suite

**Frontend:**
- **React 19**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS v4**: Utility-first styling
- **Plotly.js / react-plotly.js**: Interactive client-side chart rendering
- **Axios**: API communication
- **react-dropzone**: Drag & drop file upload
- **lucide-react**: Icons

## Project Structure

```
chart-maker/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── main.py                   # FastAPI app, CORS, mounts
│   │   ├── api/routes.py             # API endpoints
│   │   ├── services/chart_service.py # Chart generation + Plotly data builder
│   │   ├── models/schemas.py         # Pydantic request/response models
│   │   └── config/themes.json        # Theme definitions
│   ├── tests/                        # pytest test suite
│   │   ├── conftest.py
│   │   ├── fixtures/excel_factories.py
│   │   ├── test_health.py
│   │   ├── test_upload.py
│   │   ├── test_chart_data.py
│   │   ├── test_generate.py
│   │   ├── test_download.py
│   │   ├── test_cleanup.py
│   │   ├── test_themes.py
│   │   └── test_flows.py
│   ├── uploads/                      # Temp uploaded files (UUID-named)
│   ├── outputs/                      # Generated chart files
│   └── requirements.txt
├── frontend/                         # React + Tailwind UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx        # Drag & drop upload
│   │   │   ├── DataTable.jsx         # Inline data preview table
│   │   │   ├── DataReviewModal.jsx   # Full-screen data + section viewer
│   │   │   ├── ChartOptions.jsx      # Options sidebar
│   │   │   ├── ChartPreview.jsx      # Plotly chart with toolbar
│   │   │   ├── ChartEditModal.jsx    # Inline chart editing modal
│   │   │   ├── ChartCard.jsx         # Single chart card (multi-section)
│   │   │   ├── MultiChartManager.jsx # One card per detected section
│   │   │   └── DownloadButton.jsx    # Export button
│   │   ├── services/api.js           # Axios API client
│   │   ├── utils/plotlyHelpers.js    # Plotly relayout helpers
│   │   └── App.jsx                   # Root: state + 4-step wizard
│   ├── package.json
│   └── index.html
├── chart_maker.py                    # Standalone CLI tool
├── config/themes.json                # CLI theme config
├── examples/sample_data.xlsx         # Example Excel file
└── README.md
```

## Key Configuration

- **CORS origins**: Hardcoded in `backend/app/main.py` for ports 5173, 3000, 8080. Update for production.
- **Themes**: Defined in `backend/app/config/themes.json` (professional, minimal, vibrant, academic). A separate `config/themes.json` at root is used by the CLI tool.
- **Chart types**: auto, line, bar, horizontal_bar, scatter, pie. Auto-detection prefers `horizontal_bar` when a percentage column is detected.
- **API base URL**: Set via `VITE_API_URL` env var in the frontend (defaults to `http://localhost:8000/api`).
- **Export formats**: png, svg, pdf. DPI configurable (150–600, default 300).

## Roadmap

- [x] Web interface for easier use
- [x] Interactive chart previews
- [ ] More chart types (heatmaps, box plots, violin plots)
- [ ] Batch processing from multiple Excel files
- [ ] Custom template support
- [ ] Chart annotation and labeling tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the examples folder for usage patterns

---
