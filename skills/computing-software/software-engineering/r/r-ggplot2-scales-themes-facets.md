---
id: computing-software.software-engineering.r.r-ggplot2-scales-themes-facets
name: r-ggplot2-scales-themes-facets
category: computing-software
field: software-engineering
product: r
tags: [r, ggplot2-scales-themes-facets]
level: practitioner
status: draft
description: "Customise ggplot2 plots: scale_* functions, theme(), facet_wrap/grid, coord_*, labs and ggsave sizing."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ggplot2 polish
- `scale_x_log10(labels = scales::label_comma())`, `scale_fill_viridis_d()`, `scale_colour_manual(values = ...)`; `coord_cartesian(ylim=)` zooms without dropping data (unlike `ylim()`).
- `facet_wrap(~ g, scales = "free_y", ncol = 2)`; `theme_minimal(base_size = 12) + theme(legend.position = "bottom")`.
- `labs(title=, x=, y=, caption=)`; patchwork `p1 + p2`.
- `ggsave("p.png", width = 6, height = 4, dpi = 300)`.
Verify: file dimensions match the requested pixels.
