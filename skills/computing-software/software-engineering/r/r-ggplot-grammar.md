---
id: computing-software.software-engineering.r.r-ggplot-grammar
name: r-ggplot-grammar
category: computing-software
field: software-engineering
product: r
tags: [r, r-ggplot2, ggplot-grammar]
level: practitioner
status: draft
description: "Build plots with aes mappings versus constants, stat layers, scales and facet_wrap."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aesthetics, geoms, scales and facets
- Map variables inside `aes()`, set constants outside (`geom_point(colour = "red")`).
- `geom_col()` plots given heights; `geom_bar()` counts; `position = "dodge"`, `"fill"` or `"stack"`.
- Scales: `scale_x_log10()`, `scale_fill_viridis_d()`, `scale_y_continuous(labels = scales::label_percent())`; zoom with `coord_cartesian(ylim = )` because scale limits drop data.
- `facet_wrap(~ g, scales = "free_y")`, `facet_grid(r ~ c)`.
- Inside functions use `.data[[var]]` or `{{ var }}` for column names.
Verify: `ggsave("p.png", p, width = 6, height = 4, dpi = 300)` and view the file.
