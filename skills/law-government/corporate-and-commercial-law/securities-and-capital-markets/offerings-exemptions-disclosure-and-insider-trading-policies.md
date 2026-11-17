---
id: law-government.corporate-and-commercial-law.securities-and-capital-markets.offerings-exemptions-disclosure-and-insider-trading-policies
name: offerings-exemptions-disclosure-and-insider-trading-policies
category: law-government
field: corporate-and-commercial-law
product: securities-and-capital-markets
tags: [securities-and-capital-markets, corporate-and-commercial-law, securities-law, capital-markets, securities-offering, ipo, registration-statement, s-1, prospectus, securities-act-1933, exchange-act-1934, private-placement, regulation-d, rule-506b, rule-506c, accredited-investor, reg-s, rule-144a, regulation-a, crowdfunding, prospectus-regulation, uk-listing-rules, mar, market-abuse-regulation, periodic-reporting, 10-k, 10-q, 8-k, materiality, rule-10b-5, insider-trading, insider-trading-policy, blackout-period, 10b5-1-plan, section-16, due-diligence-defence, comfort-letter]
level: advanced
status: docs-checked
description: "Securities-law essentials: registered vs exempt offerings, private placements, prospectus disclosure and liability, periodic reporting, and insider-trading policies and blackout windows."
sources: ["17 CFR 230.506 (https://www.law.cornell.edu/cfr/text/17/230.506)", "17 CFR 230.503 (https://www.law.cornell.edu/cfr/text/17/230.503)", "17 CFR 240.10b5-1 (https://www.law.cornell.edu/cfr/text/17/240.10b5-1)", "15 U.S.C. 77k (https://www.law.cornell.edu/uscode/text/15/77k)", "15 U.S.C. 78p (https://www.law.cornell.edu/uscode/text/15/78p)", "17 CFR 243.100 (https://www.law.cornell.edu/cfr/text/17/243.100)", "FCA PS25/9 (https://www.fca.org.uk/publications/policy-statements/ps25-9-new-rules-public-offers-admissions-trading-regime)", "SEC, Additional Form 8-K Disclosure Requirements, Release 33-8400 (https://www.sec.gov/files/rules/final/33-8400.pdf)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offerings, disclosure and insider-trading policies

**Goal:** raise capital and keep a company's disclosure lawful — every offer of securities
either registered/approved or exempt, disclosure accurate and complete, and insiders
trading only within a policy. US federal securities law is the textbook model; the UK
and EU prospectus and market abuse regimes are noted. State "blue sky" laws and local
rules add requirements.

## 1. The first question: is it a security, and is the offer exempt?
- Equity, debt, convertible notes, SAFEs and many investment contracts are securities
  (US *Howey* test for investment contracts — relevant to tokens).
- **US Securities Act §5:** every offer and sale must be registered or exempt.
- Common exemptions:
  - **Rule 506(b):** unlimited raise; accredited investors plus up to 35 sophisticated
    non-accredited (who must get specified disclosure); **no general solicitation**.
  - **Rule 506(c):** general solicitation allowed, but all purchasers accredited and the
    issuer takes reasonable steps to **verify** status.
  - **Regulation S** (offshore), **Rule 144A** (resales to QIBs), **Regulation A** and
    **Regulation Crowdfunding** (with dollar caps — check current limits).
  - File **Form D** within 15 days after first sale for Reg D offerings; check state notice filings.
- Securities sold in exempt offerings are **restricted**: resale needs an exemption (e.g. Rule 144 holding periods).
- UK/EU: a prospectus is generally required for public offers unless an exemption applies;
  check the current exemptions. The UK Public Offers and Admissions to Trading Regulations
  2024 regime replaced the UK Prospectus Regulation, with the FCA's new rules in force from
  19 January 2026 (FCA PS25/9).

## 2. Disclosure documents
- Registration statement/prospectus: business, risk factors (specific, not generic), MD&A,
  financial statements, management, compensation, use of proceeds, dilution.
- **Liability:** Securities Act §11 (15 U.S.C. 77k): signers, directors, underwriters and
  named experts may be liable for a material misstatement or omission in a registration
  statement; the issuer has no due-diligence defence, while the others can prove a
  reasonable investigation. Also check §12(a)(2) and Rule 10b-5.
- **Due diligence** by underwriters and counsel builds the defence: management interviews,
  document review, auditor **comfort letters**, legal opinions and negative assurance
  letters. Keep a diligence memo.
- Private placements: no prospectus required, but anti-fraud rules apply — a private
  placement memorandum reduces risk.

## 3. Periodic reporting (US public companies)
10-K (annual), 10-Q (quarterly), 8-K (current events within four business days for
listed triggers, e.g. material agreements, executive changes, cybersecurity incidents
determined material), proxy statements. Disclosure controls and SOX certifications by CEO/CFO.
Regulation FD (17 CFR 243.100): when an issuer discloses material non-public information
to specified persons such as broker-dealers, investment advisers and security holders, it
must make public disclosure simultaneously (intentional) or promptly (non-intentional).

## 4. Insider-trading policy
- **Rule 10b-5** prohibits trading on material non-public information (MNPI) in breach of a
  duty; tipping too. UK and EU market-abuse rules differ; check the current text.
- Policy contents: covered persons (directors, officers, employees, family), **blackout
  periods** around earnings, **pre-clearance** for insiders, prohibitions on hedging/pledging,
  event-specific blackouts.
- **Rule 10b5-1 plans** give an affirmative defence for pre-planned trades (17 CFR
  240.10b5-1(c)). For directors and officers the cooling-off period is the later of 90 days
  after adoption or two business days after the 10-Q or 10-K for the quarter of adoption,
  capped at 120 days; for other persons it is 30 days. Directors and officers must certify
  no awareness of material non-public information and good faith, and a person other than
  the issuer is limited in adopting successive single-trade plans within 12 months.
- Section 16 (15 U.S.C. 78p): directors, officers and holders of more than 10 percent of a
  registered equity security must report, and short-swing profits (purchase and sale within
  less than six months) are recoverable by the issuer.

## Gotchas
- General solicitation (a social media post about the raise) destroys a 506(b) exemption.
- Integration: separate offerings can be combined, losing exemptions — check integration safe harbours.
- Gun-jumping: publicity before or during a registered offering.

## Verify
- [ ] Each offering mapped to a specific exemption with conditions satisfied and Form D filed.
- [ ] Disclosure documents backed by a diligence file.
- [ ] Insider-trading policy covers blackouts, pre-clearance, 10b5-1 plans and hedging.
- [ ] Current-report triggers monitored with a disclosure committee.

## Checked
Checked 2026-10-24. Jurisdictions: United States federal securities law and the UK (FCA). Sources read 2026-10-24: 17 CFR 230.506 (35-purchaser limit and non-accredited knowledge test in 506(b); accredited-only and reasonable verification in 506(c)); 17 CFR 230.503(a)(1) (Form D within 15 calendar days after first sale); 17 CFR 240.10b5-1 (cooling-off periods, certification, single-trade limit); 15 U.S.C. 77k; 15 U.S.C. 78p; 17 CFR 243.100; the FCA search result (POATRs regime in force 19 January 2026) and SEC release 33-8400 as shown in search results (four business days for Form 8-K). Removed unconfirmed statements on EU and UK prospectus exemption numbers, materiality case law, MAR details, blackout windows, the insider-trading-policy exhibit rule and the Rule 10b-5 scienter note. General information, not legal advice.
Method: documentation only; no commands were run.
