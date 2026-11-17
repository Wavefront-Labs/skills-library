---
id: computing-software.web-development.frontend-development.d3-data-visualisation-with-svg
name: d3-data-visualisation-with-svg
category: computing-software
field: web-development
product: frontend-development
tags: [d3-js, svg-charts, data-visualisation, scales, javascript]
level: practitioner
status: docs-checked
description: "Building SVG charts with D3: scales, axes, the data join with key functions, enter/update/exit, and using D3 inside React with refs."
sources:
  - https://d3js.org/getting-started
  - https://d3js.org/d3-selection/joining
  - https://d3js.org/d3-scale
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data visualisation with D3 and SVG

## 1. Scales and axes
Scales map abstract data to a visual encoding (position, colour, stroke width, size). Pick by data type: linear (quantitative), time (time series), pow/log/symlog (wide ranges), band or point (categorical as position), ordinal, sequential/diverging (colour), quantile/quantize/threshold (discrete). Axes come from d3-axis; see `scale.ticks` and `scale.tickFormat`; colour schemes are in d3-scale-chromatic.
```js
import * as d3 from "d3";
const x = d3.scaleLinear([0, data.length - 1], [marginLeft, width - marginRight]);
const y = d3.scaleLinear(d3.extent(data), [height - marginBottom, marginTop]);
const svg = d3.create("svg").attr("width", width).attr("height", height);
svg.append("g").attr("transform", `translate(0,${height - marginBottom})`).call(d3.axisBottom(x));
svg.append("g").attr("transform", `translate(${marginLeft},0)`).call(d3.axisLeft(y));
container.append(svg.node());
```
The y range runs from the bottom margin to the top margin because SVG's y axis points down. Import everything (`import * as d3 from "d3"`), specific symbols (`import {select} from "d3"`) or submodules (`import {mean} from "d3-array"`).

## 2. The data join
```js
svg.selectAll("circle")
  .data(data, d => d.id)          // key function: replaces join-by-index
  .join(
    enter => enter.append("circle").attr("fill", "green"),
    update => update.attr("fill", "blue"),
    exit => exit.remove()
  )
    .attr("stroke", "black");
```
- `selection.data` binds an array to the selection and defines the enter (data with no element) and exit (elements with no data) selections. `selection.join` appends, removes and reorders elements to match, and returns the merged enter and update selections.
- `.join("circle")` is shorthand for enter = append, update = identity, exit = remove.
- Without a key function the first datum goes to the first element and so on; a key function returning a string identifier binds by identity instead, and by minimising DOM changes can improve performance. Duplicate element keys go to exit; duplicate data keys go to enter.
- With a key function the DOM order may differ from data order; use `selection.order` or `selection.sort` when needed.
- You can animate by creating transitions inside the enter, update and exit functions; if enter/update return transitions the underlying selections are merged and returned, and the exit return value is ignored.
- `selection.datum` sets bound data without a join.

## 3. D3 in React
- Modules that do not touch the DOM (d3-scale, d3-array, d3-interpolate, d3-format) work in React as normal, so you can compute scales and render SVG elements in JSX.
- Modules that operate on selections (d3-selection, d3-transition, d3-axis) manipulate the DOM and compete with React's virtual DOM. Attach a ref to an element and pass it to D3 in `useEffect`:
```jsx
const gx = useRef(), gy = useRef();
useEffect(() => void d3.select(gx.current).call(d3.axisBottom(x)), [gx, x]);
useEffect(() => void d3.select(gy.current).call(d3.axisLeft(y)), [gy, y]);
```

## Verify
- [ ] Updating the data adds, removes and moves the right marks, and keyed marks keep their identity when the order changes.

## Checked

2026-11-09. Read in full the D3 Getting started, Joining data (selection) and d3-scale pages. Confirmed the scale types, axis construction, import styles, the join, key function, enter/exit and transition behaviour, and the React guidance. Removed, as not stated by these pages: Observable Plot advice and its source (blocked, HTTP 429), viewBox/ResizeObserver resizing, crispEdges and non-scaling-stroke, accessibility attributes, the canvas and quadtree threshold advice, UTC/DST and zero-baseline rules, and the exact margins and transition code.

Method: documentation only; no commands were run.
