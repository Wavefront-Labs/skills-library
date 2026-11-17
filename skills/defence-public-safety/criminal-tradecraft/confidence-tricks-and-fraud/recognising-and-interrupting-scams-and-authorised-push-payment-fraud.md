---
id: defence-public-safety.criminal-tradecraft.confidence-tricks-and-fraud.recognising-and-interrupting-scams-and-authorised-push-payment-fraud
name: recognising-and-interrupting-scams-and-authorised-push-payment-fraud
category: defence-public-safety
field: criminal-tradecraft
product: confidence-tricks-and-fraud
tags: [criminal-tradecraft, confidence-tricks-and-fraud, confidence-trick, con-artist, scam, fraud-prevention, fraud-investigator, authorised-push-payment, app-fraud, impersonation-scam, bank-impersonation, safe-account-scam, romance-scam, investment-scam, pig-butchering, crypto-scam, business-email-compromise, bec, invoice-redirection, ceo-fraud, courier-fraud, elder-fraud, vulnerable-customer, banking-protocol, confirmation-of-payee, money-mule, social-engineering, red-flags, scam-intervention, action-fraud, report-fraud, ic3, scamwatch, reportcyber, reimbursement, defensive]
level: practitioner
status: draft
description: "Fraud-prevention method for bank, branch and business staff: the shared anatomy of scams, red flags by typology, how to intervene with a victim mid-payment, and where to report and recover."
sources: ["UK Finance annual fraud reports and Take Five guidance (public)", "UK Payment Systems Regulator APP reimbursement policy, Oct 2024 (public)", "FBI IC3 annual reports; Australian Scamwatch/NASC (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recognising and interrupting scams and authorised push payment fraud

**Goal:** for a fraud analyst, bank or branch staff member, finance team or adviser to
vulnerable people — spot a confidence scheme while the money can still be stopped, intervene
in a way that works on a victim who has been coached, and get it reported and traced quickly.

## 1. The shared anatomy (recognise this, not the story)
Nearly every con has this shape:
1. **Contact with a borrowed identity or relationship** — bank, police, HMRC/IRS, a supplier,
   a boss, a romantic partner, a grandchild, a delivery firm.
2. **A pretext that creates emotion** — fear (your account is compromised), greed (guaranteed
   returns), love, urgency or secrecy.
3. **Isolation** — "don't tell the branch staff", "this is a confidential investigation",
   "your family wouldn't understand".
4. **A payment the victim makes themselves** — transfer to a "safe account", gift cards, crypto,
   cash handed to a courier, buying gold. Because the customer authorises it, normal unauthorised-fraud
   controls do not catch it.
5. **Repeat extraction** until the victim runs out or is stopped.
If you see 3 and 4 together, treat it as a scam until proved otherwise.

## 2. Red flags by typology
| Typology | What you see |
|---|---|
| Bank/police impersonation, "safe account" | Customer moving large sums to a new payee in their own name at another bank; on the phone during the transaction; told staff may be "in on it" |
| Courier/cash collection | Older customer withdrawing unusual cash, asking for it in specific notes, cagey about purpose |
| Investment / crypto ("pig butchering") | Contact met online; returns shown on a platform the victim can't withdraw from; "tax" or "fee" demanded before withdrawal |
| Romance | Partner never met or video-called; repeated emergencies; moving to crypto or gift cards |
| Invoice redirection / BEC | Supplier email announcing **new bank details**; urgent CEO request for a confidential payment; lookalike domain |
| Purchase scams | Prices well below market; bank transfer insisted on instead of card/platform payment |
| Recovery scams | Someone offering to recover earlier losses for a fee — a known second-wave scam |
Also watch for **money mules**: accounts receiving many unrelated credits and forwarding them out
fast — often young people recruited by "easy money" posts.

## 3. Intervening with a customer mid-scam
- **Ask open questions, privately and away from their phone:** "Who asked you to make this
  payment?" "How did you first hear about this investment?" "Has anyone told you what to say to us?"
- Coached victims give **scripted answers** ("it's for home improvements", "a family gift"). Gently
  test details; inconsistency is the signal.
- Say plainly: **"Your bank or the police will never ask you to move money to keep it safe, or to
  lie to us."**
- Use **delay**: hold the payment, ask them to call a trusted person, or ring the bank back on the
  number on their card (from a different phone — some scams keep the line open).
- **UK:** the **Banking Protocol** lets branch staff call police (999) for an immediate response when
  a customer is being defrauded in branch. Check whether your country has an equivalent.
- Record what was said and done; it matters for reimbursement.

## 4. Business controls (BEC / invoice fraud)
- **Call-back verification** of any bank-detail change using a number already on file, never one
  from the email.
- Dual authorisation over a threshold; payee name checks (**Confirmation of Payee** in the UK, similar
  services elsewhere).
- DMARC on your domain; flag external emails and lookalike domains.
See `computing-software.digital-privacy-hygiene.phishing-awareness.spotting-and-handling-phishing`.

## 5. Report, trace and recover
1. **Speed matters:** the sending bank should request a recall/freeze from the receiving bank within
   hours; funds are usually split onward fast.
2. Report: UK **Action Fraud / Report Fraud** (rebranding in progress in 2025–26 — check the current
   name), US **IC3** (and FTC), Australia **ReportCyber** and **Scamwatch**; elsewhere the national police
   cybercrime/fraud portal.
3. **UK reimbursement:** since 7 Oct 2024 PSPs must reimburse most APP-scam victims on Faster Payments,
   capped at £85,000 per claim, with exceptions for gross negligence. *(Uncertain: cap and excess rules
   have been revised before — verify current PSR terms.)* Other countries' schemes differ.
4. Flag the account as vulnerable and warn about recovery scams; victims are re-targeted.
For tracing proceeds, see
`defence-public-safety.criminal-investigation.financial-crime-investigation.tracing-money-flows-for-a-fraud-or-laundering-case`.

## Verify
- [ ] You can name the five-step anatomy and spot isolation + self-authorised payment.
- [ ] Staff have open-question prompts and know coached victims give scripted answers.
- [ ] A hold/delay and escalation path (e.g. Banking Protocol) is documented.
- [ ] Bank-detail changes require call-back to a number on file.
- [ ] Recall requests go out within hours; reporting channel for your country is listed.
- [ ] Victims are warned about recovery scams.
