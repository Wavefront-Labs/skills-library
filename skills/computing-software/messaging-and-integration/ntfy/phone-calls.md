---
id: computing-software.messaging-and-integration.ntfy.phone-calls
name: phone-calls
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, phone-call, x-call, twilio, alerts]
level: practitioner
status: docs-checked
description: "Trigger an ntfy voice call with the X-Call header; requirements for verified numbers, auth, and the Twilio server keys."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phone calls

Header `X-Call` (alias `Call`): a number with `+` and country code, or `yes` for your first verified number.

```
curl -u :tk_... -H "Call: +12223334444" -d "Reactor meltdown imminent" ntfy.sh/alerts
```

## Requirements

- The number must be verified in the web app.
- Authenticated users only. On ntfy.sh this requires a Pro plan.
- The voice is English only.
- Follow the Twilio Acceptable Use Policy.
- JSON publishing uses the `call` field.

## Self-hosted keys

```yaml
twilio-account: "..."
twilio-auth-token: "..."
twilio-phone-number: "..."
twilio-verify-service: "..."
twilio-call-format: "..."   # optional TwiML Go template
```

Phone call limits default to none except for tiers that define a call limit.

## Gotchas

- Twilio is the call provider; calls are enabled by configuring the Twilio options above.
- There are no anonymous phone calls: numbers must be verified in the web app by an authenticated user.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Phone calls: X-Call, verification, authenticated only, Pro on ntfy.sh, English only, Twilio AUP, limits) and config page (Phone calls: the five twilio keys). Removed: the Verify step; reworded the gotchas to what the pages state.
Method: documentation only; no commands were run.
