# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

Excel Chart Maker generates publication-ready charts from Excel data files (.xlsx, .xls). It has a React web UI, a FastAPI backend, and a standalone CLI tool (`chart_maker.py`).

## Development Commands

### Backend (FastAPI, port 8000)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React + Vite, port 5173)
```bash
cd frontend
npm install
npm run dev       # dev server with HMR
npm run build     # production build to dist/
npm run lint      # ESLint
```

### CLI Tool
```bash
python chart_maker.py -i examples/sample_data.xlsx -t line -f png
```

There are no automated tests. API docs are at `http://localhost:8000/docs` (Swagger).

## Architecture

**Full-stack app with two independent processes**: a Vite React frontend and a FastAPI backend. Both must be running for the web UI to work.

### Frontend (`frontend/src/`)

All application state lives in `App.jsx` via `useState` hooks (no Redux/Context). It drives a 4-step wizard: Upload → Data Preview → Chart Config & Preview → Download.

The API client (`services/api.js`) is a configured Axios singleton. Its base URL comes from the `VITE_API_URL` env var (defaults to `http://localhost:8000/api`). Each component (`FileUpload`, `DataTable`, `ChartOptions`, `ChartPreview`, `DownloadButton`) handles one step of the wizard and receives state/callbacks as props from `App.jsx`.

### Backend (`backend/app/`)

Layered architecture: **Routes** (`api/routes.py`) → **Services** (`services/chart_service.py`) → **Models** (`models/schemas.py`).

`ChartService` is the core class. It reads Excel files with pandas, generates charts with matplotlib/seaborn, and applies themes from `config/themes.json` via matplotlib `rcParams`. There is no database — uploaded files are stored in `backend/uploads/` with UUID filenames and tracked by `file_id`.

### Data Transfer Pattern

Charts are generated server-side by matplotlib, encoded as **base64 strings**, and returned in JSON responses. The frontend decodes the base64 to display previews and trigger browser downloads. This avoids serving static files for ephemeral chart output.

## Key Configuration

- **CORS origins**: Hardcoded in `backend/app/main.py` for ports 5173, 3000, 8080. Must be updated for production.
- **Themes**: Defined in `backend/app/config/themes.json` (professional, minimal, vibrant, academic). Each theme sets colors, grid, fonts, and sizes. A separate `config/themes.json` at root is used by the CLI tool.
- **Chart types**: auto, line, bar, scatter, pie. Auto-detection in `ChartService._detect_chart_type()` is based on column count.
- **Export formats**: png, svg, pdf. DPI is configurable (150-600, default 300).
