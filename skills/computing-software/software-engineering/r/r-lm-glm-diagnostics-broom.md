---
id: computing-software.software-engineering.r.r-lm-glm-diagnostics-broom
name: r-lm-glm-diagnostics-broom
category: computing-software
field: software-engineering
product: r
tags: [r, lm-glm-diagnostics-broom]
level: advanced
status: draft
description: "Fit and check R models: lm/glm formulas, summary, residual plots, anova, predict with intervals, broom tidy/glance/augment."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modelling
- `fit <- lm(y ~ x1 * x2 + factor(g), data = df)`; `glm(y ~ x, family = binomial)`; `summary(fit)`, `anova(fit1, fit2)`, `confint(fit)`.
- Diagnostics: `plot(fit)`, `car::vif`, `influence.measures`, `performance::check_model` (confirm package).
- `predict(fit, newdata, interval = "prediction")`; for glm `type = "response"`.
- broom: `tidy(fit, conf.int = TRUE)`, `glance(fit)`, `augment(fit)`.
Verify: coefficients match a hand calculation on a toy set.
