---
id: computing-software.messaging-and-integration.ntfy.tiers-payments
name: tiers-payments
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, tiers, payments, stripe, user-limits]
level: advanced
status: docs-checked
description: "Give ntfy users per-user limits with tiers via ntfy tier and change-tier, and the Stripe keys for payments."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiers and payments

Tiers change limits per user (messages, email, calls, attachments, reservations).

```
ntfy tier add pro                     # add tier with code "pro", using the defaults
ntfy tier change --name="Pro" pro     # update the name of an existing tier
ntfy tier del starter                 # delete an existing tier
ntfy user change-tier phil pro        # switch user "phil" to tier "pro"
```

The page's full example sets `--name`, `--message-limit`, `--message-expiry-duration`, `--email-limit`, `--call-limit`, `--reservation-limit`, `--attachment-file-size-limit`, `--attachment-total-size-limit`, `--attachment-expiry-duration`, `--attachment-bandwidth-limit` and `--stripe-price-id`. No tiers are predefined; newly created users have no tier, so all limits come from `server.yml` until a tier overrides some of them.

## Related config

- `enable-signup`, `enable-login` (both default `false`) let users sign up and log in via the web app or API.
- `enable-reservations` (default `false`) lets users reserve topics if their tier allows it.

## Payments

```yaml
stripe-secret-key: "..."
stripe-webhook-key: "..."
billing-contact: "..."
```

`stripe-secret-key` enables payments in the web app; `stripe-webhook-key` validates incoming Stripe webhooks; `billing-contact` is shown in the Upgrade dialog (optional). Also define a Stripe webhook for `customer.subscription.updated` and `customer.subscription.deleted` pointing to `https://ntfy.example.com/v1/account/billing/webhook`. The page says the integration is tailored to ntfy.sh and Stripe.

## Gotchas

- Phone calls have no limit by default except tiers that define a call limit.

## Checked

2026-11-04. Confirmed against the ntfy config page (Tiers, Payments, config options table: enable-signup/login/reservations defaults) and publish page (call limit). Corrected: replaced placeholder ntfy tier lines with the documented commands. Removed: the access-control gotcha and the Verify step.
Method: documentation only; no commands were run.
