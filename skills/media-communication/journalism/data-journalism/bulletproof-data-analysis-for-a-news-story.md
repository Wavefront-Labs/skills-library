---
id: media-communication.journalism.data-journalism.bulletproof-data-analysis-for-a-news-story
name: bulletproof-data-analysis-for-a-news-story
category: media-communication
field: journalism
product: data-journalism
tags: [data-journalism, ddj, computer-assisted-reporting, car, data-analysis, data-cleaning, spreadsheet, excel, google-sheets, sql, python, pandas, r, openrefine, csv, data-dictionary, per-capita, rates, inflation-adjustment, bulletproofing, data-diary, visualisation-brief, charts, journalism, foi-data]
level: practitioner
status: draft
description: "Get a dataset to a publishable finding: acquire with documentation, keep a data diary, clean, interview the data, compute fair comparisons, bulletproof, and brief graphics and copy accurately."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulletproof data analysis for a news story

**Goal:** a numerical finding you can defend line by line to an editor, the data's
owner and a hostile reader — and a story and chart that don't overstate it.

## 1. Acquire with documentation
- Get the **data dictionary / record layout** and any methodology notes with the data.
  Without them you don't know what a column means.
- Prefer raw, row-level data in a native format (CSV, XLSX, database export) over
  summary PDFs. If only PDFs exist, Tabula or similar extract tables — then spot-check
  rows against the PDF.
- Record provenance: source, URL or request ID, date retrieved, file hash or copy saved
  read-only. **Never edit the original file.**

## 2. Keep a data diary
A plain text or notebook log of every step: what you did, why, and the result count.
Scripts (SQL, Python/pandas, R) are self-documenting and re-runnable; if working in a
spreadsheet, copy each step to a new tab and note it. The diary is what lets a colleague
reproduce your number — the core test of bulletproofing.

## 3. Interview the data
Before looking for the story, check:
- **Row count** matches what the source says it should be.
- **Ranges:** min/max of each numeric and date column — negative ages, dates in 1900 or
  the future reveal errors and placeholder values.
- **Nulls and blanks:** how many, and what blank means (zero? unknown? not applicable?).
- **Categories:** count distinct values; find spelling variants ("St.", "Street", "ST")
  and clean them with OpenRefine or explicit mappings in code.
- **Duplicates:** decide what a unique record is (one per person? per incident? per
  charge?) and test it.
- **Coverage gaps:** missing months, agencies that didn't report, changed definitions
  mid-series. Changing definitions are the most common source of fake trends.

## 4. Fair comparisons
- **Rates, not raw counts,** when populations differ (per 100,000 residents, per 1,000
  pupils). Use a population denominator from the same year and geography.
- **Inflation-adjust** money across years; say which index and base year.
- **Percent vs percentage points** — 10% to 15% is 5 points, a 50% increase.
- **Small numbers** swing wildly. Avoid ranking places with tiny counts; pool years or
  flag uncertainty.
- **Correlation isn't cause.** Copy says "areas with X also had Y", not "X caused Y",
  unless the methodology actually supports causation.
- Check the finding holds when you change reasonable choices (different year, excluding
  outliers). If it flips, it's not a story — or the fragility is the story.

## 5. Bulletproof
- Have a second person **re-run the analysis independently** from raw data.
- **Ask the data owner** to confirm your method and headline numbers before publication;
  they often know the quirks (and it's fair).
- Check every number in the copy, headline and chart against the diary.
- Publish a methodology note or box; share the cleaned data where licences allow.

## 6. Briefing graphics and copy
Give the graphics desk: the one-sentence finding, the exact table behind it, units,
source line, caveats, and which comparison matters. Bar charts start at zero; line charts
need consistent intervals; maps of raw counts mostly map population — use rates.

## Verify
- [ ] Original file saved untouched with provenance recorded.
- [ ] Data diary/script reproduces every published number from raw data.
- [ ] Row counts, ranges, nulls and duplicates checked and documented.
- [ ] Comparisons use rates/adjusted values where appropriate.
- [ ] Independent re-run and data-owner check done.
- [ ] Copy uses language no stronger than the analysis supports.
