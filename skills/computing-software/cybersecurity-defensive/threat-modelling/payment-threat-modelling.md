---
id: computing-software.cybersecurity-defensive.threat-modelling.payment-threat-modelling
name: payment-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [payment-threat-modelling, pci-dss, cardholder-data, e-skimming, payment-fraud, tokenisation]
level: advanced
status: draft
description: "Threat model a payment flow: cardholder data scope, checkout page skimming, price and amount tampering, refund and webhook abuse, and PCI DSS v4 scope reduction."
sources: ["https://www.pcisecuritystandards.org/document_library/", "https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html", "https://owasp.org/www-project-automated-threats-to-web-applications/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Payment flow threat modelling

## Model the flow
DFD from customer browser/app through checkout page, your backend, payment service provider (PSP) hosted
fields or redirect, PSP webhook back to you, order fulfilment, refunds, and finance reconciliation. Mark where
**primary account numbers (PAN)** are present; that defines PCI DSS scope.

## Scope decisions first
- Redirect or iframe hosted payment page: PAN never touches your servers (SAQ A style), but the page that loads
  the iframe still matters.
- Direct post / JavaScript that builds the form: your page is in scope for skimming (SAQ A-EP style).
- Server receives PAN: full scope; use PSP tokenisation immediately and never store CVV.

## Threats
1. **E-skimming (Magecart)**: injected JavaScript on the checkout page captures card fields. PCI DSS v4
   requirements 6.4.3 (inventory and authorise every payment page script, integrity check) and 11.6.1
   (detect unauthorised changes to payment page headers and content). Controls: CSP, SRI, script inventory,
   change monitoring.
2. **Amount/price tampering**: client sends price or currency; attacker pays 1 cent. Control: server computes
   totals from catalogue; the payment intent amount is created server-side.
3. **Webhook forgery and replay**: fake "payment succeeded" callback. Control: verify PSP signature, check
   timestamp, re-fetch the payment status from the PSP API before fulfilling, idempotency on event ID.
4. **Race conditions**: double-spend of gift cards or vouchers, parallel refund requests. Control: database
   transactions with row locks, idempotency keys.
5. **Refund abuse**: refund to a different card or exceeding the original amount; insider refunds. Control:
   refund only to original instrument, cap at captured amount, dual approval above thresholds.
6. **Card testing / carding**: bots validating stolen cards via small authorisations. Control: rate limits per
   IP/device/account, CAPTCHA on anomalies, PSP fraud tools, 3-D Secure.
7. **Credential and account takeover** leading to purchases with stored cards. Control: MFA or step-up on
   adding cards and changing addresses.
8. **Logging PAN**: card numbers in logs, analytics or error tracking. Control: masking, DLP scans of logs.

## Gotchas
- "We use Stripe so PCI does not apply" is wrong; scope shrinks, it does not disappear.
- Test in the PSP sandbox with negative cases (declines, duplicate webhooks, delayed webhooks).

## Verify
Server rejects client-supplied amounts, webhook handler fails closed on bad signature, payment page script
inventory exists with integrity monitoring, and log searches for PAN patterns return nothing.
