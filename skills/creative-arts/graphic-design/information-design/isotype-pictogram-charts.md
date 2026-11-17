---
id: creative-arts.graphic-design.information-design.isotype-pictogram-charts
name: isotype-pictogram-charts
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, isotype, pictogram-charts, unit-chart, icon-array, otto-neurath, pictogram]
level: practitioner
status: draft
description: "Build Isotype-style pictogram charts: one icon equals a fixed quantity, count by repetition not size, use partial icons for remainders, and keep icons consistent."
sources:
  - https://helpx.adobe.com/illustrator/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Isotype and pictogram counts

**Goal:** a chart where quantity is read by counting repeated, identical symbols rather than comparing areas.

## Principle
Isotype (International System Of TYpographic Picture Education) was developed from the 1920s-30s by Otto Neurath with Marie Neurath and the artist Gerd Arntz. Its core rule for charts: **to show more, use more symbols, not larger ones.** Enlarging an icon scales area and misleads.

## Build rules
1. **Choose one unit per icon** (for example 1 icon = 1 million people) and state it in a key next to the chart.
2. **Same size, same spacing, same orientation** for every icon; align in rows from a common baseline.
3. **Partial values:** show a cut icon (left part) for remainders; if the data cannot be rounded sensibly, state the rounding rule.
4. **Rows, not clouds:** one row per category, items sorted by value, row labels at left; compare totals by row length.
5. **Icon choice:** a simple, unambiguous silhouette at small size; different categories get different icons or colours, not both unless needed. Never let a decorative style obscure the count.
6. **Colour:** one hue for the main measure; a second only for a highlighted category or a subdivision; check contrast and colour-blind safety.

## In Illustrator
- Make the icon a **symbol** or a single object, then use **Object > Transform > Move** with Copy and **Cmd/Ctrl+D** to repeat precisely, or build a **Blend** (Object > Blend > Make) with specified steps.
- Mask the last icon with a rectangle (Pathfinder or clipping mask) for a partial value.
- Keep numeric values in a table so the chart can be regenerated.

## Honesty and limits
- Icon charts become hard to read above roughly 20-30 icons per row; raise the unit value instead.
- Add direct number labels at the end of each row.

## Self-check
Count icons per row and multiply by the unit: it must match the data. Check that partial icons are cut by the correct fraction.
