---
id: computing-software.software-engineering.r.r-lm-glm-formulas
name: r-lm-glm-formulas
category: computing-software
field: software-engineering
product: r
tags: [r, r-stats-models, lm-glm-formulas]
level: practitioner
status: docs-checked
description: "Fit and read lm and glm models, specify formulas and make predictions with newdata."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.glm.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/contrast.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/relevel.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/nobs.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/anova.lm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lm, glm, formulas and predict
- `predict.glm(type = "response")` gives predicted probabilities for a binomial model; the default is the link scale (`?predict.glm`).
- Factors use treatment contrasts by default (`?contr.treatment`); `relevel()` sets the reference level (`?relevel`).
- The default `na.action` is `na.omit`, which drops incomplete rows; compare `nobs(m)` with `nrow(d)` (`?nobs`).
Verify: `predict(m)` on training data matches `fitted(m)`.

## Checked

Date: 2026-11-02. Confirmed on: ?predict.glm (type = "response"), ?contrast (contr.treatment), ?relevel, ?nobs, ?anova.lm (na.action default). Removed as not confirmed on those pages: Formula operator expansion, broom lines, and the confint/plot method list (not read on these pages).

Method: documentation only; no commands were run.
