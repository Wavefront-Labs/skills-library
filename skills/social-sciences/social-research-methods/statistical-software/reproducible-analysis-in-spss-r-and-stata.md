---
id: social-sciences.social-research-methods.statistical-software.reproducible-analysis-in-spss-r-and-stata
name: reproducible-analysis-in-spss-r-and-stata
category: social-sciences
field: social-research-methods
product: statistical-software
tags: [statistical-software, spss, spss-syntax, pasw, r, rstudio, tidyverse, haven, labelled-data, renv, quarto, rmarkdown, stata, do-files, log-files, reproducibility, reproducible-research, codebook, value-labels, missing-values, user-missing, data-cleaning, recoding, project-structure, version-control, git, survey-data, sav-files, dta-files]
level: practitioner
status: draft
description: "Run social-research analysis reproducibly in SPSS, R or Stata: script everything, keep raw data read-only, handle labels and user-missing codes, and move .sav/.dta data between tools safely."
sources: ["IBM SPSS Statistics Command Syntax Reference", "haven package documentation (tidyverse)", "Stata User's Guide, chapters on do-files and logs", "Long, The Workflow of Data Analysis Using Stata (Stata Press 2009)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statistical packages for social research — reproducible workflows

**Goal:** anyone (including you in a year) can rerun the analysis from raw data to every
table with one command, whichever of SPSS, R or Stata your team uses.

## 1. Same project layout in every tool
```
project/
  data/raw/        # as received; read-only, never overwritten
  data/derived/    # produced only by scripts
  code/01_clean.*  02_construct.*  03_analyse.*  00_master.*
  output/tables/  output/figures/  logs/
  docs/codebook.*
```
`00_master` runs the others in order. Put the project under git; keep identifiable data
out of the repository (add `data/` to `.gitignore` if it holds personal data).

## 2. SPSS — use syntax, not menus
- Every dialog has a **Paste** button: paste, then run from the syntax window. Save `.sps` files.
- Start each script with file handles so paths live in one place:
  `FILE HANDLE raw /NAME='data/raw'.` then `GET FILE='raw/survey.sav'.` (Relative paths
  resolve against SPSS's working directory; set it with `CD 'project'.`)
- Missing values: declare **user-missing** codes (`MISSING VALUES q1 TO q20 (-9, -8).`) so
  "refused" and "don't know" are excluded from statistics but preserved.
- `RECODE ... INTO` new variables; never recode in place on raw variables.
- Output: export tables with `OUTPUT EXPORT` or OMS to capture results programmatically.
- `SET SEED` before any random sampling or bootstrapping.

## 3. R — tidyverse plus labelled data
- Read SPSS/Stata files with `haven::read_sav()` / `read_dta()`. Value labels arrive as
  `haven_labelled`; user-missing codes are converted to `NA` unless you pass
  `user_na = TRUE`. Convert with `as_factor()` deliberately, at a known step.
- Pin package versions with **renv** (`renv::init()`, `renv::snapshot()`); record
  `sessionInfo()` in outputs.
- Write reports in **Quarto** or R Markdown so numbers in text come from code.
- Survey-weighted analysis: `survey`/`srvyr`; multilevel: `lme4`; tables: `modelsummary`, `gtsummary`.
- Use `here::here()` for paths instead of `setwd()`.

## 4. Stata — do-files and logs
- Every do-file opens with `version 18` (or your version) for command stability, `clear all`,
  `set more off`, and `log using "logs/01_clean.log", replace text`.
- `label define` / `label values` for value labels; use extended missing codes `.a .b .c`
  for refusal / don't know / not applicable.
- `assert` to test assumptions (`assert inrange(age, 16, 99) | missing(age)`).
- See social-sciences.economics.stata.do-file-pipelines-estimation-and-tables for a fuller Stata pipeline.

## 5. Moving data between tools
- `.sav` ↔ `.dta`: haven reads and writes both; check that value labels, variable labels and
  user-missing definitions survived (`haven::print_labels()`, Stata `labelbook`).
- Avoid CSV as the interchange format for labelled survey data — labels and missing
  definitions are lost.
- Long string variables and dates are the usual casualties; check types after conversion.

## 6. Codebook
Generate rather than hand-write: SPSS `CODEBOOK` command, R `codebookr`/`labelled::look_for()`,
Stata `codebook, compact`. Include source question text, valid values, missing codes, and
derived-variable formulas.

## Gotchas
- SPSS **weights** (`WEIGHT BY`) are frequency weights: significance tests treat the
  weighted total as the sample size. Use Complex Samples, R `survey`, or Stata `svy` for
  inference with sampling weights.
- Excel as an intermediate step silently reformats IDs (leading zeros) and dates.
- Default R factor order is alphabetical; set reference categories explicitly.

## Verify
- [ ] Deleting `data/derived` and `output` then running the master script reproduces everything.
- [ ] Raw data never written to by any script.
- [ ] Random seeds set; package/software versions recorded.
- [ ] Labels and missing codes checked after any format conversion.
- [ ] Generated codebook matches the derived data.

*Draft: command names reflect recent versions; minor syntax may differ in older SPSS/Stata releases.*
