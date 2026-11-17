---
id: computing-software.software-engineering.r.r-htests-pvalues
name: r-htests-pvalues
category: computing-software
field: software-engineering
product: r
tags: [r, r-stats-models, htests-pvalues]
level: practitioner
status: docs-checked
description: "Choose t.test, wilcox.test, chisq.test or fisher.test and adjust p-values."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/pairwise.t.test.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/shapiro.test.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/chisq.test.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html", "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/qqnorm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hypothesis tests and multiple comparisons
- `t.test` uses the Welch modification of the degrees of freedom by default (`var.equal = FALSE`); `paired = TRUE` gives a paired test (`?t.test`).
- `wilcox.test` is the Wilcoxon rank sum and signed rank test (`?wilcox.test`).
- `p.adjust(p, method = ...)` accepts `"holm"`, `"hochberg"`, `"hommel"`, `"bonferroni"`, `"BH"` (alias `"fdr"`) and `"BY"`; `pairwise.t.test` takes a `p.adjust.method`.
- `shapiro.test` is the Shapiro-Wilk normality test; `qqnorm` draws a normal Q-Q plot.
Verify: Simulate under the null and check the rejection rate.

## Checked

Date: 2026-11-02. Confirmed on: ?t.test (Welch, paired), ?p.adjust (method names, fdr alias), ?pairwise.t.test, ?shapiro.test, ?qqnorm, ?wilcox.test. Removed as not confirmed on those pages: The chisq.test small-expected-count warning and fisher.test advice, and the effect-size recommendation (not stated on these pages).

Method: documentation only; no commands were run.
