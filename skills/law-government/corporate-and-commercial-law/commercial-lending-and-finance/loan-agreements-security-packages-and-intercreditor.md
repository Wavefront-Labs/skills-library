---
id: law-government.corporate-and-commercial-law.commercial-lending-and-finance.loan-agreements-security-packages-and-intercreditor
name: loan-agreements-security-packages-and-intercreditor
category: law-government
field: corporate-and-commercial-law
product: commercial-lending-and-finance
tags: [commercial-lending-and-finance, corporate-and-commercial-law, commercial-lending, banking-and-finance, leveraged-finance, credit-agreement, facility-agreement, loan-agreement, lma, lsta, term-loan, revolving-credit-facility, rcf, covenants, financial-covenants, leverage-ratio, interest-cover, negative-pledge, events-of-default, cross-default, mac-clause, security-package, security-interest, ucc-article-9, ucc-1, perfection, debenture, fixed-charge, floating-charge, guarantees, upstream-guarantee, corporate-benefit, financial-assistance, intercreditor-agreement, subordination, first-lien-second-lien, conditions-precedent, sofr, sonia]
level: advanced
status: docs-checked
description: "Documenting commercial debt finance: term sheet to credit agreement, key covenants and events of default, security and perfection, guarantees, intercreditor terms and conditions precedent."
sources: ["UCC 9-307 (https://www.law.cornell.edu/ucc/9/9-307)", "Companies Act 2006 s859A (https://www.legislation.gov.uk/ukpga/2006/46/section/859A)", "Companies Act 2006 s859H (https://www.legislation.gov.uk/ukpga/2006/46/section/859H)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loan agreements, security packages and intercreditor terms

**Goal:** document a loan so the lender is protected and the borrower can still run its
business, with security that is actually enforceable. Market templates — LMA (UK/Europe)
and LSTA (US) — are the baseline; secured-transactions law is local (US UCC Article 9;
English law charges; civil-law pledges and mortgages).

## 1. Term sheet to first draft
Key commercial terms: facilities (term loan, revolving credit, letters of credit), amount,
purpose, tenor and amortisation, pricing (margin over **SOFR**/**SONIA** or other
risk-free rate, fees), security and guarantors, covenants, conditions precedent, governing
law. The term sheet becomes the drafting checklist.

## 2. Credit agreement architecture
Definitions (where much of the negotiation lives: EBITDA add-backs, permitted debt,
permitted liens) → facilities and drawdown mechanics → interest, fees, payments →
prepayments (voluntary and mandatory: asset sales, excess cash flow, debt issuance,
change of control) → representations → information undertakings → financial covenants →
general undertakings → events of default → agency, assignment, amendments and waivers.

## 3. Covenants and defaults
- **Financial covenants:** leverage (debt/EBITDA), interest cover, fixed-charge cover,
  minimum liquidity. Maintenance (tested quarterly) vs incurrence (tested when taking an
  action — typical of high-yield and covenant-lite loans). Model them on the borrower's
  projections with headroom — and check equity cure rights.
- **Negative covenants:** negative pledge, restrictions on debt, disposals, distributions,
  investments, mergers — each with baskets.
- **Events of default:** non-payment (short grace), covenant breach, misrepresentation,
  cross-default (threshold amount), insolvency, judgments, change of control, material
  adverse change (rarely called; litigated uncertainty).
- **Amendment thresholds:** majority vs all-lender ("sacred rights") matters; loose drafting
  has enabled liability-management transactions (see workout skill).

## 4. Security and perfection
- **US (UCC Article 9):** security agreement granting security interest (attachment) +
  perfection, typically by filing a **UCC-1 financing statement** where the debtor is located
  (UCC 9-307: a registered organization is located in its state of organization; an
  individual at the principal residence); control agreements for deposit accounts;
  possession for certificated securities; separate filings for real property (mortgages),
  federally registered IP (USPTO/Copyright Office recordings).
- **English law:** debenture with fixed and floating charges; register at Companies House
  within **21 days** beginning with the day after creation (Companies Act 2006 s859A), or the
  charge is void against a liquidator, administrator and creditors (s859H). Fixed vs floating characterisation depends on control in practice.
- Search existing liens first; get payoff letters and releases for existing debt.

## 5. Guarantees
Upstream and cross-stream guarantees from subsidiaries raise **corporate benefit** and
fraudulent-transfer issues; use savings clauses limiting guarantee amounts. Financial
assistance rules in some jurisdictions may restrict a target guaranteeing debt used to buy it;
check local law. Guarantee wording should exclude defences that discharge guarantors when
the underlying deal changes.

## 6. Intercreditor
Where there are multiple lender classes: ranking of payment and security, standstill on
enforcement by junior creditors, turnover of recoveries received out of order, release
mechanics on enforcement sales, voting in insolvency, purchase options for juniors. US
first-lien/second-lien intercreditors also address waiver of bankruptcy rights (DIP
financing, adequate protection).

## 7. Conditions precedent
Constitutional documents and board approvals, legal opinions (capacity and enforceability),
security documents signed and filings ready, KYC, financial statements, payoff letters,
fees paid. Run a **CP checklist** with the agent.

## Gotchas
- Check the debtor's exact registered name and location before filing a UCC-1.
- Missing the 21-day Companies House window.
- EBITDA definitions with uncapped add-backs make financial covenants meaningless.

## Verify
- [ ] Covenant levels tested against the borrower's model with headroom.
- [ ] Lien searches done; all security perfected by the right method and deadline.
- [ ] Guarantee limitations and corporate approvals in place for each guarantor.
- [ ] CP checklist complete before funding.

## Checked
Checked 2026-10-24. Jurisdictions: United States (UCC Article 9) and England and Wales (Companies Act 2006). Sources read 2026-10-24: UCC 9-307 (debtor location); CA 2006 s859A(4) (21 days beginning with the day after creation) and s859H(3) (void against liquidator, administrator and creditor; money secured becomes payable). Removed unconfirmed statements on covenant headroom percentages, UCC-1 name-error effects and UK financial-assistance abolition. General information, not legal advice.
Method: documentation only; no commands were run.
