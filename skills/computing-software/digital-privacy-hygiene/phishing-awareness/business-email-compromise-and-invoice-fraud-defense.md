---
id: computing-software.digital-privacy-hygiene.phishing-awareness.business-email-compromise-and-invoice-fraud-defense
name: business-email-compromise-and-invoice-fraud-defense
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, bec, business-email-compromise, invoice-fraud, vendor-impersonation, wire-transfer-fraud, ceo-fraud, payment-redirection, out-of-band-verification, dual-control, dmarc, spf, dkim, email-spoofing]
level: practitioner
status: draft
description: "Stop business email compromise and invoice fraud: verify any payment-detail change out of band, dual-control wire transfers, and recognise the setup phase before the ask arrives."
sources:
  - "https://www.fbi.gov/how-we-can-help-you/scams-and-safety/common-fraud-schemes/business-email-compromise"
  - "https://www.ic3.gov/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business email compromise and invoice fraud defense

**Goal:** stop the specific fraud pattern that costs individuals and small
businesses more than almost any other scam category — a convincing email or
hijacked thread that redirects a real payment to an attacker's account — by
treating *any* change to payment details as something to verify out of band,
every time, with no exceptions for urgency or seniority.

## 1. The pattern, in order
1. **Reconnaissance**: the attacker studies a target's public info (company
   website, LinkedIn, out-of-office replies, press releases about a deal or
   executive travel) or compromises a real mailbox (vendor, client, or an
   employee) and reads real threads to learn vocabulary, invoice formats, and
   who approves payments.
2. **Setup**: either a **lookalike domain** email (`vendor-co.com` →
   `vendor-c0.com`) or, more dangerously, the attacker is inside the **real**
   mailbox (via a prior phishing hit) and replies from the genuine thread,
   making sender-address checks useless.
3. **The ask**: an invoice with "updated" bank details, a request to redirect an
   already-scheduled payment, or — the CEO-fraud variant — an urgent request
   from a spoofed or compromised executive account to wire funds or buy gift
   cards, deliberately timed for when the real person is known to be unreachable
   (travel, a meeting) so you can't easily check with them.
4. **Pressure**: urgency, secrecy ("don't mention this to anyone else yet" —
   a request for silence is itself a major red flag; legitimate finance
   processes don't ask you to bypass normal visibility), and a request to use an
   unusual payment rail (wire instead of the normal invoicing system, gift
   cards, cryptocurrency).

## 2. The one habit that stops almost all of it
**Any change to payment details, or any payment request outside the normal
process, gets verified through a channel you already had before this message
arrived — never through contact info in the email itself.** Call the vendor on
the number from a previous invoice or their public main line, not a number in
the "updated" signature. Message the executive on a phone number already in
your contacts, not one provided in the suspicious email. This single check
defeats the pattern regardless of how convincing the email/thread looks, because
it doesn't matter whether the sender address is real if the verification
doesn't trust anything the message supplied.

## 3. Dual control for anything that moves money
- No single person should be able to both **initiate and approve** a payment
  detail change or a wire transfer above a set threshold — require a second
  person, using the out-of-band check in section 2 as part of their approval,
  not just a rubber-stamp click.
- For a small business or sole operator without a natural second approver,
  build in a mandatory **cooling-off step**: any new or changed payee sits for
  24 hours (or until independently verified) before the first payment goes out.

## 4. Technical controls that help but don't replace the habit
- **DMARC/SPF/DKIM** on your own domain, set to reject/quarantine failures,
  stops attackers from spoofing *your* exact domain in mail sent to others —
  it does nothing to stop a lookalike domain or a genuinely compromised mailbox,
  which is why it's a floor, not the defense.
- Email client warnings for "external sender" or "first time this domain has
  emailed you" are useful nudges but are routinely missed under urgency
  pressure — train for the habit in section 2, don't rely on the banner alone.

## 5. If a payment already went out
Call the receiving bank and your own bank **immediately** — wire recalls have a
narrow window and get harder by the hour, not the day. Report to the FBI's IC3
(US) or your local equivalent, and to the bank, in parallel, not sequentially.
Preserve the original email headers for investigators rather than forwarding a
cleaned-up copy.

## Gotchas
- A compromised **real** vendor mailbox replying in an existing thread defeats
  "check the sender address" entirely — the out-of-band callback is what catches
  this, nothing in the email will.
- "Don't tell anyone, handle this quietly" attached to a payment request is
  itself diagnostic — treat it as a stop condition, not a compliment to your
  discretion.
- Uncertain: recovery odds and recall windows vary by bank, country and payment
  rail — act immediately rather than researching the odds first.

## Verify
- [ ] Every payment-detail change gets a callback on a number sourced before
      the message, not from the message.
- [ ] No single person can both change a payee and release a payment above your
      threshold without a second, independently-verifying person.
- [ ] You can name the four stages of the pattern (recon, setup, ask, pressure)
      and the specific phrase that signals "pressure for silence."
- [ ] You know who to call at your bank, right now, without looking it up under
      pressure, if a fraudulent transfer goes out.
