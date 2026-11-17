---
id: computing-software.software-engineering.r.r-ggplot-themes-export
name: r-ggplot-themes-export
category: computing-software
field: software-engineering
product: r
tags: [r, r-ggplot2, ggplot-themes-export]
level: practitioner
status: draft
description: "Apply theme_*, adjust text and legends, and save publication graphics."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Themes, labels, legends and saving
- `theme_minimal(base_size = 12)`, then `theme(legend.position = "bottom", axis.text.x = element_text(angle = 45, hjust = 1))`.
- `labs(title =, subtitle =, caption =, x =, y =, colour =)`; `guides(colour = guide_legend(nrow = 2))`.
- `ggsave()` infers the device from the extension; for vector output use `.pdf` or `.svg`.
- Combine plots with patchwork: `p1 + p2 + plot_layout(ncol = 1)`.
Verify: open the file at the intended print size.
