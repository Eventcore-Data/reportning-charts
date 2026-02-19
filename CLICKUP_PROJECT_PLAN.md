# Excel Chart Maker — ClickUp Project Plan

**Project:** Excel Chart Maker
**Developer:** Solo
**Start Date:** February 13, 2025
**Deadline:** March 6, 2025 (3 weeks)
**Repository:** https://github.com/aaronforreal/chart-maker
**Success Criteria:** Every chart produced is consistent, good-looking, and ready to go straight into a report.

---

## Timeline Overview

| Week | Focus | Dates |
|------|-------|-------|
| **Week 0** | Phase 1: MVP | COMPLETED |
| **Week 1** | Phase 2: Chart Customization | Feb 13 – Feb 19 |
| **Week 2** | Phase 3: Multi-Chart & Multi-Table | Feb 20 – Feb 26 |
| **Week 3** | Polish, Testing & Launch | Feb 27 – Mar 6 |

**Phases 4 & 5** (Integration & Scale, Advanced Capabilities) are deferred to post-launch backlog. The 3-week deadline covers delivering a fully functional, tested, and deployed product with all core chart features.

---

## Phase 1: MVP (COMPLETED)

> **Status:** Done
> **ClickUp List:** Phase 1 — MVP

| # | Task | Duration | Priority | Status | Dependencies |
|---|------|----------|----------|--------|--------------|
| 1.1 | Project setup, README, .gitignore | 0.5d | High | Done | — |
| 1.2 | CLI chart generator (chart_maker.py) | 1d | High | Done | — |
| 1.3 | Theme system (config/themes.json) | 0.5d | High | Done | — |
| 1.4 | FastAPI backend — project structure | 0.5d | High | Done | — |
| 1.5 | Backend — Excel upload & parsing endpoint | 1d | High | Done | 1.4 |
| 1.6 | Backend — Chart generation endpoint | 1d | High | Done | 1.4 |
| 1.7 | Backend — Themes, download, cleanup endpoints | 0.5d | Medium | Done | 1.4 |
| 1.8 | Frontend — React + Vite + Tailwind setup | 0.5d | High | Done | — |
| 1.9 | Frontend — FileUpload component (drag & drop) | 1d | High | Done | 1.8 |
| 1.10 | Frontend — DataTable component | 0.5d | Medium | Done | 1.8 |
| 1.11 | Frontend — ChartOptions component | 1d | High | Done | 1.8 |
| 1.12 | Frontend — ChartPreview component | 1d | High | Done | 1.8 |
| 1.13 | Frontend — DownloadButton component | 0.5d | High | Done | 1.8 |
| 1.14 | Frontend — API service layer | 0.5d | Medium | Done | 1.8 |
| 1.15 | Fix Tailwind CSS v4 PostCSS config | 0.5d | Urgent | Done | 1.8 |
| 1.16 | Fix PDF & SVG chart preview | 0.5d | High | Done | 1.12 |
| 1.17 | GitHub repo setup & initial push | 0.5d | Medium | Done | All above |
| 1.18 | Project proposal document | 0.5d | Low | Done | All above |

---

## Week 1: Phase 2 — Chart Customization (Feb 13 – Feb 19)

> **Goal:** Give users full control over chart appearance.
> **ClickUp List:** Phase 2 — Chart Customization

### Backend Tasks

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 2.1 | Add axis titles (X and Y labels) to chart generation | 0.5d | High | — | Update `chart_service.py` to accept and render axis labels |
| 2.2 | Add unit formatting for axis tick marks | 0.5d | High | 2.1 | Prefix/suffix on tick labels (e.g. "$100", "50%", "10kg") |
| 2.3 | Add data labels on chart elements | 1d | High | — | Show values on bars, points, pie slices |
| 2.4 | Add grid line controls | 0.5d | Medium | — | Toggle on/off, style (dashed/dotted/solid), opacity |
| 2.5 | Add custom font support | 1d | Medium | — | Font family + size for title, labels, ticks |
| 2.6 | Add custom colour picker for data series | 1d | Medium | — | Accept user-defined colour list, override theme colours |
| 2.7 | Update API schemas for new chart options | 0.5d | High | 2.1–2.6 | Update Pydantic models in `schemas.py` |
| 2.8 | Update `/api/generate` endpoint for new options | 0.5d | High | 2.7 | Pass new fields through to chart service |

### Frontend Tasks

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 2.9 | Add axis titles input fields to ChartOptions | 0.5d | High | 2.1 | Two text inputs for X and Y axis labels |
| 2.10 | Add unit selector/input to ChartOptions | 0.5d | High | 2.2 | Dropdown with common units + custom input |
| 2.11 | Add data labels toggle to ChartOptions | 0.5d | Medium | 2.3 | Checkbox/toggle switch |
| 2.12 | Add grid line controls to ChartOptions | 0.5d | Medium | 2.4 | Toggle + style dropdown + opacity slider |
| 2.13 | Add font controls to ChartOptions | 0.5d | Medium | 2.5 | Font family dropdown + size input |
| 2.14 | Add colour picker for data series | 1d | Medium | 2.6 | Colour input per series, with preview swatches |
| 2.15 | Update API service for new options | 0.5d | High | 2.7 | Update `api.js` generate call |
| 2.16 | Test all customization options end-to-end | 1d | High | All above | Generate charts with every combination, verify output |

### Week 1 Milestone
- [ ] All 6 customization features working (axis titles, units, data labels, grid lines, fonts, colours)
- [ ] Frontend UI updated with all new controls
- [ ] Charts with customizations render correctly in PNG, SVG, and PDF

---

## Week 2: Phase 3 — Multi-Chart & Multi-Table (Feb 20 – Feb 26)

> **Goal:** Support complex Excel files and multi-chart layouts for reports.
> **ClickUp List:** Phase 3 — Multi-Chart & Multi-Table

### Backend Tasks

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 3.1 | Multi-sheet Excel parsing | 1d | High | — | Detect all sheets, return sheet names in upload response |
| 3.2 | Sheet selector in data preview | 0.5d | High | 3.1 | Allow picking which sheet to chart from |
| 3.3 | Multiple table detection within a sheet | 1d | High | 3.1 | Detect separate tables by blank rows/columns |
| 3.4 | Multi-chart layout engine | 1.5d | High | — | Matplotlib subplot grids: 1x2, 2x2, 2x3 layouts |
| 3.5 | New chart types — stacked bar | 0.5d | Medium | — | Add to chart_service.py |
| 3.6 | New chart types — heatmap | 0.5d | Medium | — | Add to chart_service.py |
| 3.7 | New chart types — box plot | 0.5d | Medium | — | Add to chart_service.py |
| 3.8 | New chart types — violin plot | 0.5d | Low | — | Add to chart_service.py |
| 3.9 | Update API for multi-sheet and multi-chart | 0.5d | High | 3.1–3.4 | New endpoints or params for sheet selection and layout |

### Frontend Tasks

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 3.10 | Sheet selector dropdown in UI | 0.5d | High | 3.1, 3.2 | Show after upload if multiple sheets detected |
| 3.11 | Table selector when multiple tables found | 0.5d | High | 3.3 | Let user pick which table(s) to chart |
| 3.12 | Multi-chart layout selector | 0.5d | High | 3.4 | Grid layout picker (1, 2, 4, 6 charts) |
| 3.13 | New chart type options in ChartOptions | 0.5d | Medium | 3.5–3.8 | Add stacked bar, heatmap, box plot, violin to dropdown |
| 3.14 | Test multi-sheet and multi-chart end-to-end | 1d | High | All above | Test with real multi-sheet Excel files |

### Week 2 Milestone
- [ ] Multi-sheet Excel files parsed correctly with sheet selector
- [ ] Multiple tables detected and selectable
- [ ] Multi-chart grid layouts working (2, 4, 6 charts per page)
- [ ] 4 new chart types available (stacked bar, heatmap, box plot, violin)

---

## Week 3: Polish, Testing & Launch (Feb 27 – Mar 6)

> **Goal:** Stabilize, test with real users, fix issues, deploy.
> **ClickUp List:** Week 3 — Polish & Launch

### Testing & QA

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 4.1 | Create test Excel files covering all scenarios | 0.5d | High | — | Single sheet, multi-sheet, multi-table, edge cases |
| 4.2 | End-to-end testing — all chart types | 1d | High | — | Generate every chart type in every format and theme |
| 4.3 | End-to-end testing — all customization options | 0.5d | High | — | Test every option in combination |
| 4.4 | User testing — recruit 2-3 testers | 0.5d | High | — | Real users try the tool with their own Excel files |
| 4.5 | Collect and triage user feedback | 0.5d | High | 4.4 | Document bugs and usability issues |
| 4.6 | Fix critical bugs from user testing | 1.5d | Urgent | 4.5 | Priority fixes only — ship-blocking issues |

### Polish & Documentation

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 4.7 | Update README with new features | 0.5d | Medium | — | Document Phase 2 and 3 features |
| 4.8 | Error handling audit | 0.5d | Medium | — | Ensure all API errors surface clearly in UI |
| 4.9 | UI polish pass | 0.5d | Medium | — | Spacing, alignment, responsive check, loading states |
| 4.10 | Performance check — large Excel files | 0.5d | Medium | — | Test with 1000+ row files, optimize if needed |

### Deployment

| # | Task | Duration | Priority | Dependencies | Notes |
|---|------|----------|----------|--------------|-------|
| 4.11 | Docker containerization (backend + frontend) | 1d | High | — | Dockerfile + docker-compose.yml |
| 4.12 | Deploy to cloud (Render / Railway / AWS) | 1d | High | 4.11 | Pick simplest option, get it live |
| 4.13 | Verify production deployment | 0.5d | High | 4.12 | Full workflow test on live URL |
| 4.14 | Final Git cleanup and tagged release | 0.5d | Medium | All above | Tag v1.0.0, clean up branches |

### Week 3 Milestone
- [ ] All features tested end-to-end with real data
- [ ] User testing completed, critical bugs fixed
- [ ] Application deployed and accessible online
- [ ] README updated, v1.0.0 tagged

---

## Post-Launch Backlog (After Mar 6)

> These are parked for after the 3-week deadline. Add to a separate ClickUp List.

### Phase 4: Integration & Scale
| # | Task | Priority | Notes |
|---|------|----------|-------|
| 5.1 | User authentication & login | Medium | JWT or OAuth |
| 5.2 | Chart history — save generated charts per user | Medium | Requires auth |
| 5.3 | Reusable chart templates | Medium | Save & load chart configs |
| 5.4 | API key authentication for programmatic access | Low | For external integrations |
| 5.5 | Dashboard/iframe embed support | Low | Embeddable widget mode |

### Phase 5: Advanced Capabilities
| # | Task | Priority | Notes |
|---|------|----------|-------|
| 6.1 | Data filtering & transformation before charting | Medium | Filter rows, sort, aggregate |
| 6.2 | Chart annotations & callouts | Medium | Add text/arrows on charts |
| 6.3 | CSV and JSON file support | Medium | Beyond Excel |
| 6.4 | Batch export — all charts at once | Low | ZIP download |
| 6.5 | Collaborative sharing — shareable chart links | Low | Public URLs for charts |

---

## ClickUp Setup Guide

### Recommended Structure

```
Space: Excel Chart Maker
├── Folder: Development
│   ├── List: Phase 1 — MVP (COMPLETED)
│   ├── List: Phase 2 — Chart Customization
│   ├── List: Phase 3 — Multi-Chart & Multi-Table
│   └── List: Week 3 — Polish & Launch
├── Folder: Post-Launch Backlog
│   ├── List: Phase 4 — Integration & Scale
│   └── List: Phase 5 — Advanced Capabilities
```

### Custom Fields to Add
- **Duration** (number, in days)
- **Priority** (dropdown: Urgent / High / Medium / Low)
- **Dependencies** (relationship field linking to other tasks)
- **Phase** (dropdown: Phase 1 / Phase 2 / Phase 3 / Launch / Backlog)

### Views to Create
- **Timeline View** — Gantt chart across all lists, grouped by phase
- **Board View** — Kanban per list (To Do → In Progress → Testing → Done)
- **Calendar View** — See daily task distribution

### Milestones (add as Milestones in ClickUp)
| Date | Milestone |
|------|-----------|
| Feb 12 | Phase 1 Complete — MVP shipped |
| Feb 19 | Phase 2 Complete — All customization features working |
| Feb 26 | Phase 3 Complete — Multi-chart and multi-table support |
| Mar 3 | User testing complete, critical bugs fixed |
| Mar 6 | v1.0.0 deployed to production |

---

## Daily Schedule (Suggested)

For a solo developer working full days:

**Week 1 (Chart Customization)**
| Day | Tasks |
|-----|-------|
| Thu Feb 13 | 2.1 Axis titles + 2.2 Units + 2.9 + 2.10 (frontend for both) |
| Fri Feb 14 | 2.3 Data labels + 2.4 Grid lines + 2.11 + 2.12 (frontend) |
| Sat Feb 15 | Buffer / catch-up |
| Sun Feb 16 | Buffer / catch-up |
| Mon Feb 17 | 2.5 Custom fonts + 2.13 (frontend) |
| Tue Feb 18 | 2.6 Custom colours + 2.14 (frontend) |
| Wed Feb 19 | 2.7 + 2.8 + 2.15 (API updates) + 2.16 (testing) |

**Week 2 (Multi-Chart & Multi-Table)**
| Day | Tasks |
|-----|-------|
| Thu Feb 20 | 3.1 Multi-sheet parsing + 3.10 Sheet selector UI |
| Fri Feb 21 | 3.3 Multiple table detection + 3.11 Table selector UI |
| Sat Feb 22 | Buffer / catch-up |
| Sun Feb 23 | Buffer / catch-up |
| Mon Feb 24 | 3.4 Multi-chart layout engine + 3.12 Layout selector UI |
| Tue Feb 25 | 3.5–3.8 New chart types + 3.13 UI + 3.9 API updates |
| Wed Feb 26 | 3.14 End-to-end testing of all Phase 3 features |

**Week 3 (Polish & Launch)**
| Day | Tasks |
|-----|-------|
| Thu Feb 27 | 4.1–4.3 Test file creation + full test pass |
| Fri Feb 28 | 4.4–4.5 User testing + feedback collection |
| Sat Mar 1 | Buffer / catch-up |
| Sun Mar 2 | Buffer / catch-up |
| Mon Mar 3 | 4.6 Bug fixes from user testing |
| Tue Mar 4 | 4.7–4.10 Polish + docs + 4.11 Docker |
| Wed Mar 5 | 4.12–4.13 Deploy to cloud + verify |
| Thu Mar 6 | 4.14 Final release tag + any remaining fixes |
