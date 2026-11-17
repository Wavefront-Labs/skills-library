---
id: business-finance.auditing.audit-analytics.journal-entry-testing
name: journal-entry-testing
category: business-finance
field: auditing
product: audit-analytics
tags: [audit-analytics, auditing, journal-entry-testing, jet, je-testing, management-override, full-population-testing, caats, data-analytics, completeness-check, trial-balance-rollforward, gl-extract, risk-criteria, weekend-postings, round-amounts, manual-journals, benfords-law, duplicate-entries, pandas, python, sql, idea, acl, excel, isa-240, as-2401]
level: advanced
status: docs-checked
description: "Test the whole journal-entry population for management override: extract and prove completeness against the trial balance, apply risk filters, and follow up the entries they surface."
sources: ["https://pcaobus.org/oversight/standards/auditing-standards/details/AS2401", "https://pcaobus.org/resources/staff-publications/audit-focus/audit-focus-journal-entries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Journal-entry testing — analyse every entry, then look hard at a few

**Goal:** respond to the presumed risk of management override (ISA 240 / PCAOB AS 2401.58)
by analysing **all** journal entries for the period, selecting the risky ones by criteria
you can explain, and obtaining support for them.

## 1. Get the data and prove it's complete (most of the work)
- Request a GL detail extract for the full period plus post-close entries: entry ID,
  line number, account, amount (or debit/credit), posting date, effective date, user who
  posted, approver, source/journal type (manual vs system), description.
- **Completeness:** opening TB + sum of all entries by account = closing TB, for every
  account. Any account that doesn't roll forward means missing data — fix it before testing.
- **Integrity:** each entry ID nets to zero; no blank users or dates; record counts and
  hash totals match what the client's system reports.
- Note the extraction method; ideally watch it run, so the client can't filter it.

## 2. Understand the normal before hunting the abnormal
Profile the population: entries per month, per user, per source; manual vs automated
share; typical posting times. Talk to finance about the close process and who should post
what. Your filters only mean something against that baseline.

## 3. Apply risk criteria
Common filters (pick those relevant to the fraud risks you identified in planning):
- Manual entries to revenue, reserves, accruals, or to accounts rarely used.
- Entries posted **after period close** or near year-end with effective dates in the period.
- Posted by senior management, or by users who don't normally post journals.
- Posted and approved by the same user, or with no approver.
- **Round amounts** (e.g. ending 000) and amounts just below approval limits.
- Unusual pairings (debit revenue / credit cash; debit expense / credit equity).
- Weekend, holiday or late-night postings.
- Blank, vague or keyword descriptions ("adjust", "per CFO", "reclass", "plug").
- Duplicates (same amount, account and date).
- Benford's-law first-digit deviations — a weak signal on its own, useful only for large,
  naturally-occurring populations.

Score entries on how many criteria they hit and focus on the combinations, not single
flags (thousands of entries are posted on weekends by batch jobs).

## 4. Example in Python (pandas)
```python
import pandas as pd
je = pd.read_csv("gl_detail.csv", parse_dates=["posting_date", "effective_date"])
# completeness: each entry balances
assert je.groupby("entry_id")["amount"].sum().round(2).eq(0).all()
manual = je["source"].eq("MANUAL")
flags = pd.DataFrame({
    "post_close": je["posting_date"] > "<CLOSE_DATE>",
    "weekend": je["posting_date"].dt.dayofweek >= 5,
    "round": (je["amount"].abs() % 1000).eq(0) & je["amount"].abs().ge(10000),
    "self_approved": je["posted_by"].eq(je["approved_by"]),
    "senior_user": je["posted_by"].isin(["<SENIOR_USER_IDS>"]),
})
je["score"] = flags.sum(axis=1)
hits = je[manual & (je["score"] >= 2)].groupby("entry_id").first()
```
IDEA, ACL/Galvanize or SQL do the same; the logic matters more than the tool.

## 5. Follow up selected entries
For each: obtain supporting documentation, understand the business reason, check the
approval, and confirm the accounting is appropriate. Ask the person who posted it, not
just their manager. Unsupported or poorly explained entries escalate to the engagement
leader and may indicate a fraud risk response is needed.

## Gotchas
- Skipping the TB rollforward: testing an incomplete population gives false comfort.
- Filters so broad they produce 5,000 hits, then picking 25 at random — that isn't targeted testing.
- Ignoring top-side / consolidation adjustments made outside the ledger (spreadsheets).
- Amount sign conventions differ between systems (debit/credit columns vs signed amounts).
- Effective date vs posting date confusion hides backdated entries.
- Data protection: GL descriptions can contain personal data; store extracts securely.

## Verify
- [ ] TB rollforward reconciles for every account; entries balance.
- [ ] Criteria are linked to identified fraud risks and documented with rationale.
- [ ] Selected entries were supported, explained and assessed for appropriateness.
- [ ] Top-side and post-close adjustments were included.
- [ ] Scripts/queries saved so the test is re-performable.

Related: business-finance.auditing.financial-statement-audit.materiality-and-audit-risk-planning.

## Checked

Date checked: 2026-10-25. Jurisdiction: International (ISA 240) and US public companies (PCAOB).
Source read: PCAOB AS 2401 and PCAOB Audit Focus on journal entries (via search results): the auditor must select journal entries and other adjustments from the general ledger and examine support, which is the management-override response described here (AS 2401.58). The ISA 240 reference is the matching international requirement.
The Python block is illustrative and was not run in this review.

Method: documentation only; no commands were run.
