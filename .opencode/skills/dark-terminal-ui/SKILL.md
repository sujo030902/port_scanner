---
name: dark-terminal-ui
description: Design dark-mode web UIs with monospace terminal aesthetic for hacking/infosec tools
license: MIT
compatibility: opencode
metadata:
  audience: frontend
  stack: html-css-js
---

## Design Principles

- **Dark-only theme** — no light mode toggle. Use GitHub Dark-inspired palette.
- **Monospace font stack** — `'SF Mono', 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace`
- **Flat design, no shadows** — use borders to separate sections.
- **Terminal/CLI feel** — the UI should look like it belongs in a terminal emulator.

## Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--bg-primary` | `#0d1117` | Page background |
| `--bg-secondary` | `#161b22` | Card/panel background |
| `--bg-tertiary` | `#21262d` | Hover/highlight |
| `--border` | `#30363d` | Borders, dividers |
| `--text-primary` | `#e6edf3` | Main text |
| `--text-secondary` | `#8b949e` | Muted text, labels |
| `--accent-green` | `#3fb950` | Success, primary actions |
| `--accent-red` | `#f85149` | Errors, danger, stop |
| `--accent-blue` | `#58a6ff` | Headings, info |
| `--accent-yellow` | `#d29922` | Warnings, banners |
| `--accent-purple` | `#bc8cff` | Service tags, secondary accents |
| `--accent-cyan` | `#39d2c0` | Stats, port numbers |

## CSS Patterns

- Cards: `background: var(--bg-secondary)` + `border: 1px solid var(--border)` + `border-radius: 8px`
- Inputs: `background: var(--bg-primary)` + `border: 1px solid var(--border)` + focus state uses `var(--accent-blue)`
- Buttons: primary = `var(--accent-green)` bg with `#0d1117` text; secondary = `var(--bg-tertiary)` with border
- Tables: `background: var(--bg-primary)` headers, `border-bottom: 1px solid var(--border)` rows, hover = `var(--bg-tertiary)`
- Progress bar: `linear-gradient(90deg, var(--accent-blue), var(--accent-cyan))`
- Status dots: `10px` circle with `@keyframes pulse` animation for running state

## Typography

- Uppercase letter-spaced labels (`font-size: 11px; text-transform: uppercase; letter-spacing: 1px`)
- Section headings: `14px` uppercase with `var(--accent-blue)` color
- Monospace everywhere — no serif/sans-serif fallback

## Layout

- Centered single-column max `960px`
- Section headers have `border-bottom: 1px solid var(--border)`
- Stats displayed in a CSS grid `repeat(auto-fit, minmax(140px, 1fr))`
- Flexbox for form rows with `gap: 12px`
- Results table is inside `overflow-x: auto` wrapper for responsiveness

## Interaction Patterns

- Polling-based async operations with status bar (idle/running/complete/error)
- Progress bar updates in real-time during background tasks
- Toast notifications at bottom-right for success/error feedback
- Disabled state on action buttons during processing
- `cursor: not-allowed` for disabled elements

## HTML Structure Convention

```
.container > .header + .card + .card#results
Each .card has: h2 title + content
.status-bar with .dot and #statusText
.progress-container > .progress-bar
.stats-grid > .stat-item*4
#resultsBody with table or empty-state
.btn-group for actions
```

## Toast Notification

Fixed bottom-right, dark card with colored left border matching type (error=red, success=green). Auto-dismiss after 4s.
