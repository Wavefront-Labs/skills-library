---
id: mathematics.statistics.r.reproducible-statistical-analysis-in-r
name: reproducible-statistical-analysis-in-r
category: mathematics
field: statistics
product: r
tags: [statistics, r, r-language, rstats, rstudio, positron, tidyverse, dplyr, tidyr, readr, ggplot2, broom, renv, quarto, rmarkdown, here, reproducibility, project-structure, lm, glm, model-fitting, data-wrangling, tidy-data, set-seed, sessioninfo]
level: practitioner
status: docs-checked
description: "Run a statistical analysis in R that someone else can rerun: project layout, renv, tidyverse import and wrangling, model fitting with broom, ggplot2, and a Quarto report."
sources: ["https://rstudio.github.io/renv/articles/renv.html", "https://dplyr.tidyverse.org/reference/mutate-joins.html", "https://readr.tidyverse.org/reference/read_delim.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible statistical analysis in R

**Goal:** an R analysis where a colleague can clone the folder, run one command, and
get the same numbers and figures.

## 1. Project layout
```
<PROJECT_ROOT>/
  analysis.Rproj      # RStudio/Positron project — sets the working directory
  data-raw/           # read-only originals, never edited
  data/               # cleaned outputs written by scripts
  R/                  # functions
  analysis.qmd        # the report
  renv.lock
```
- Never use `setwd()`; use the project plus `here::here("data-raw", "file.csv")`.
- Never edit raw data by hand; every change is code.
- Start each session clean: do not restore a saved workspace (RStudio has an option for this in Global Options).

## 2. Pin package versions with renv
```r
install.packages("renv"); renv::init()   # once
renv::snapshot()                         # after adding packages
renv::restore()                          # on a new machine
```
Commit `renv.lock` and the project `.Rprofile` to git; `renv/library` is the per-project package library, not something to commit.

## 3. Import and wrangle (tidyverse)
```r
library(tidyverse)
raw <- read_csv(here::here("data-raw", "trial.csv"),
                col_types = cols(id = col_character(), dose = col_double(),
                                 site = col_factor(), .default = col_guess()))
df <- raw |>
  filter(!is.na(outcome)) |>
  mutate(dose_c = dose - mean(dose), site = fct_relevel(site, "A")) |>
  group_by(site) |> mutate(n_site = n()) |> ungroup()
```
- Specify `col_types` for anything important — readr guesses types from `guess_max` rows (default `min(1000, n_max)`), which can
  turn IDs with leading zeros into numbers. Check `problems(raw)`.
- Tidy data: one row per observation, one column per variable — `pivot_longer()` /
  `pivot_wider()` to get there.
- `count(df, site, arm)` and `summary()` after every major step; silent row loss in
  joins is the commonest bug. Use `left_join(..., relationship = "many-to-one")`
  to make R error on unexpected duplicates.

## 4. Fit and extract models
```r
fit <- glm(event ~ arm + dose_c + site, family = binomial, data = df)
broom::tidy(fit, conf.int = TRUE, exponentiate = TRUE)  # ORs with 95% CI
broom::glance(fit)    # AIC, deviance, n
broom::augment(fit)   # fitted values and residuals per row
```
`broom` turns models into data frames, so results flow into tables and plots without
copy-paste. `summary(fit)` is for reading, not for reporting.
For mixed models use `lme4` + `broom.mixed`; for marginal effects, `marginaleffects`.

## 5. Plot with ggplot2
```r
ggplot(df, aes(dose, outcome, colour = arm)) +
  geom_point(alpha = 0.5) + geom_smooth(method = "lm") +
  labs(x = "Dose (mg)", y = "Outcome score", colour = NULL) + theme_minimal()
ggsave("fig-dose.png", width = 6, height = 4, dpi = 300)
```
Always label axes with units; set `width/height` explicitly so figures are identical across machines.

## 6. Report with Quarto
Put the analysis in `analysis.qmd`; inline numbers with `` `r round(est, 2)` `` so
text never disagrees with results. Render: `quarto render analysis.qmd`. End with
`sessionInfo()` (or `sessioninfo::session_info()`).

## 7. Randomness
Call `set.seed()` once at the top for bootstraps, simulations and splits. Note: R
3.6.0 changed the default `sample()` algorithm, so very old seeds give different draws
(`RNGkind(sample.kind = "Rounding")` reproduces the old behaviour).

## Gotchas
- Factor level order sets the reference level in models — make it explicit.
- `NA` propagates: `mean(x)` returns NA unless `na.rm = TRUE`; decide deliberately.
- The native pipe `|>` and magrittr's `%>%` behave differently in places; don't mix carelessly in shared code.

## Checked
2026-11-01. Confirmed against the renv introduction (renv.lock, .Rprofile, renv/library, init/snapshot/restore), dplyr join reference (`relationship = "many-to-one"`), readr `read_delim` (`guess_max = min(1000, n_max)`) and the R `Random` help (`sample.kind = "Rounding"` was the default before R 3.6.0). Removed: version-gate claims for dplyr, the native pipe and `stringsAsFactors`, and the RStudio menu path (not confirmed).

Method: documentation only; no commands were run.

## Verify
- [ ] Fresh R session + `renv::restore()` + `quarto render` reproduces every number.
- [ ] No `setwd()`, no absolute paths, raw data untouched.
- [ ] Row counts checked after filters and joins.
- [ ] Model results come from `broom` output, not retyped.
- [ ] Seed set; `sessionInfo()` included in the report.
