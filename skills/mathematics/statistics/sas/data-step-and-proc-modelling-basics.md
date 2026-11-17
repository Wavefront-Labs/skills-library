---
id: mathematics.statistics.sas.data-step-and-proc-modelling-basics
name: data-step-and-proc-modelling-basics
category: mathematics
field: statistics
product: sas
tags: [statistics, sas, sas-programming, data-step, proc, proc-sql, proc-means, proc-freq, proc-glm, proc-logistic, proc-mixed, proc-reg, ods, ods-output, macro, macro-variables, sas-log, merge, by-group, retain, lag, missing-values, clinical-reporting, sas-studio, sas-viya]
level: practitioner
status: draft
description: "Core SAS for analysts: DATA step logic (PDV, BY-group merges, RETAIN), PROC MEANS/FREQ/LOGISTIC/MIXED, ODS OUTPUT for results, simple macros, and reading the log."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DATA step and PROC modelling basics in SAS

**Goal:** prepare data and fit standard models in SAS with code that gives the same
result on rerun, and know where SAS silently does something you didn't intend.

## 1. Read the log every run
SAS keeps going after many problems. After each submit, search the log for
`ERROR`, `WARNING`, and these NOTEs, which signal real bugs:
- `NOTE: MERGE statement has more than one data set with repeats of BY values` —
  many-to-many merge; results are almost certainly wrong.
- `NOTE: Missing values were generated as a result of performing an operation on missing values`.
- `NOTE: Numeric values have been converted to character` (or vice versa) — implicit conversion.
- `NOTE: Variable x is uninitialized` — usually a typo.
Treat these as failures in production code.

## 2. The DATA step mental model
SAS executes the DATA step **once per input row**, building each row in the Program
Data Vector (PDV), then writes it at the end of the step (implicit OUTPUT).
- Variables are reset to missing at each iteration **unless RETAINed** (or read by SET).
- `RETAIN total 0; total + amount;` — the sum statement retains automatically.
- `LAG(x)` returns the value from the last time *that LAG call executed* — calling it
  inside an IF gives surprising results; compute it unconditionally first.
```sas
data work.visits;
  set raw.visits;
  by patid visitdt;              /* requires sorted data */
  if first.patid then nvisit = 0;
  nvisit + 1;
  days_since = visitdt - lag(visitdt);
  if first.patid then days_since = .;
run;
```

## 3. Missing values
Numeric missing `.` sorts **lower than any number**: `if x < 5` is TRUE for missing.
Write `if not missing(x) and x < 5`. Character missing is blank. Summary functions
(`sum()`, `mean()`) skip missing; `+` propagates them.

## 4. Merging
```sas
proc sort data=a; by id; run;
proc sort data=b; by id; run;
data both;
  merge a(in=ina) b(in=inb);
  by id;
  if ina;                        /* left join */
run;
```
Same-named non-BY variables: the right-hand data set overwrites the left. Rename first.
For complex joins, `PROC SQL` is clearer and warns less loudly — check row counts.

## 5. Descriptives and models
```sas
proc means data=both n nmiss mean std median q1 q3 maxdec=2; class arm; var age; run;
proc freq data=both; tables arm*event / chisq relrisk nocol nopercent; run;

proc logistic data=both;
  class arm (ref='Placebo') sex / param=ref;
  model event(event='1') = arm age sex;
  oddsratio arm;
run;

proc mixed data=long method=reml;
  class patid arm visit;
  model chg = arm visit arm*visit base / solution ddfm=kr;
  repeated visit / subject=patid type=un;
  lsmeans arm*visit / diff cl;
run;
```
Gotchas: in PROC LOGISTIC always set `event='1'` — by default SAS models the
**lowest-ordered** response value. With `CLASS`, SAS's default parameterisation is
`effect` coding; use `param=ref` with an explicit `ref=` for treatment contrasts.

## 6. Capture results with ODS
Find table names with `ods trace on;` then capture them:
```sas
ods output ParameterEstimates=pe OddsRatios=ors;
proc logistic ... ; run;
```
Build reporting tables from these data sets, never by retyping output.

## 7. Minimal macros
```sas
%let outcome = event;
%macro fit(var);
  proc logistic data=both; model &outcome.(event='1') = &var.; run;
%mend;
%fit(age) %fit(sex)
```
Use `options mprint;` to see generated code in the log. Keep macro logic small; most
repetition is better handled with BY-group processing.

## Gotchas
- Dates are days since 1 Jan 1960; always apply a format (`format visitdt date9.;`).
- `PROC SORT NODUPKEY` silently drops rows — log the count before and after.
- WORK library vanishes at session end; write durable outputs to a permanent libref.
- Uncertain: defaults described (effect coding, lowest-ordered event) are long-standing
  SAS 9.4 behaviour; verify against your SAS/Viya release documentation.

## Verify
- [ ] Log is free of ERROR, WARNING, uninitialised, conversion and repeats-of-BY notes.
- [ ] Row counts checked before/after merges and NODUPKEY.
- [ ] Missing values handled explicitly in comparisons.
- [ ] Logistic models state `event=` and reference levels.
- [ ] Results captured with ODS OUTPUT, not copied.
