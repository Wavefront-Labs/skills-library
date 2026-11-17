---
id: computing-software.software-engineering.javascript.js-devtools-network-performance-panel
name: js-devtools-network-performance-panel
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, devtools-performance, js-devtools]
level: practitioner
status: docs-checked
description: "Diagnose runtime jank in the Chrome DevTools Performance panel: CPU throttling, FPS and CPU charts, flame chart and forced reflow."
sources: ["https://developer.chrome.com/docs/devtools/performance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DevTools Network and Performance panels

- Profile in an Incognito window so extensions do not add noise.
- Use CPU throttling to simulate a mobile CPU: the tutorial uses 4x slowdown and suggests 20x slowdown to check low-end mobile devices (Capture Settings in the Performance panel).
- Record, then Stop. In the FPS chart a red bar means the frame rate dropped low enough to probably harm the user experience; 60 FPS is the target for animation. A CPU chart full of colour means the CPU was maxed out. The FPS meter is under Rendering > Show Rendering stats.
- The Summary tab breaks down activity (for example mostly rendering). In the Main section the flame chart's x-axis is time, bar width is duration and stacked events show causation. Zoom by dragging in the Overview, or with W/A/S/D after focusing the Main section.
- A red triangle on an event is a warning; on a Task it marks a long task. A Layout event can warn of forced reflow: reading an element's position after changing styles in each animation frame forces re-layout. Click the link next to the source location to jump to the line.
- Prefer properties that only affect compositing (such as transform and opacity) for animation. Compare a second recording after the fix.

Self-check: record the same interaction before and after a fix at the same CPU throttling and compare FPS and the Main flame chart.

## Checked
2026-11-09. Rewritten from and confirmed against the Chrome for Developers page Analyze runtime performance (tutorial based on Chrome 129, last updated 2024-10-23). This page covers only the Performance panel, so the Network panel claims were removed (cache disabling, network throttling presets, waterfall phases, Initiator, request blocking), along with the Web Vitals track, Lighthouse, CrUX/`web-vitals`, remote debugging and saving traces as JSON, none of which the page states.
Method: documentation only; no commands were run.
