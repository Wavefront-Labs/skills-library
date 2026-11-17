---
id: computing-software.digital-privacy-hygiene.password-hygiene.knowledge-based-authentication-quizzes
name: knowledge-based-authentication-quizzes
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, knowledge-based-authentication, kba, identity-verification, credit-report, credit-freeze, security-questions, identity-theft, nist-800-63b]
level: practitioner
status: draft
description: "Understand dynamic KBA quizzes ('which of these addresses have you lived at?') built from credit and public records, why criminals pass them, and how to reduce exposure."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.consumer.ftc.gov/articles/what-know-about-credit-freezes-and-fraud-alerts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Knowledge-based authentication quizzes

**Goal:** many government, tax and credit sites verify identity with multiple-choice
questions generated from your credit file and public records. Fraudsters with your data
pass them; know how to limit the damage.

## How they work
"Which of these was your car loan lender?", "Which street have you lived on?". Answers come
from credit bureaus and data brokers. NIST SP 800-63B does not permit knowledge-based
verification as an authenticator, and NIST identity proofing guidance has moved away from
it, but it's still common.

## Why it fails
The same records are sold by data brokers and leaked in breaches (credit header data,
past addresses). Answers are often guessable by elimination.

## What you can do
1. **Credit freeze** at all three US bureaus (Equifax, Experian, TransUnion) and others in
   your country; some KBA vendors can't pull a frozen file, which blocks new-account fraud
   that depends on KBA. Thaw temporarily when you apply for credit.
2. **Create your own accounts first** on high-risk sites (IRS/tax authority, social
   security, credit bureaus, government ID portals) with strong MFA, so an impostor can't
   create one in your name. Many such sites now use document + selfie verification instead.
3. **Get an IP PIN** (US IRS Identity Protection PIN) to block fraudulent tax returns.
4. **Data broker opt-outs** reduce what attackers can buy.
5. Review your **credit reports** (annualcreditreport.com in the US) for addresses or
   accounts you don't recognise; they become KBA answers for impostors.

## Verify
- [ ] Credit frozen at all bureaus; PINs/passwords stored in the vault.
- [ ] Accounts claimed on tax and benefits portals with MFA.
