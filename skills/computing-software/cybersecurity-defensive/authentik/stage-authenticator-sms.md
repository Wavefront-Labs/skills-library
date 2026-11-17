---
id: computing-software.cybersecurity-defensive.authentik.stage-authenticator-sms
name: stage-authenticator-sms
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, sms-authenticator, twilio, generic-provider, verify-only, phone-number]
level: practitioner
status: docs-checked
description: "Set up the authentik SMS authenticator stage with Twilio or a generic HTTP provider, customize the message or payload with mappings, and restrict phone numbers via a Prompt stage."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_sms/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: enrol a phone number so OTP codes can be sent by SMS.

## Options
Provider (**Twilio** or **Generic**), **From number**, **Account SID / External API URL**, **Auth / token**, **Auth password**, **Auth type** (Basic or Bearer, generic only), **Verify only**, **Mapping**, **Authenticator type name**, **Configuration flow**.

**Verify only** verifies number ownership at enrolment and stores a hash, so the number cannot be used by the Authenticator Validation stage. To use SMS at login allow the **SMS** device class there. The stage cannot be deleted while authenticators created through it exist; delete those first.

## Twilio
In the Twilio console: **Explore Products > Messaging > Services**, create a messaging service (verification-oriented use case), add a sender, then copy **Account SID** and **Auth token** into the stage. Custom message through a property mapping returning a `message` key:
```python
return {
    "message": f"This is a custom message for {request.http_request.brand.branding_title} SMS authentication. The code is {token}."
}
```
Variables: `device.phone_number`, `stage.from_number`, `request.http_request.brand`.

## Generic provider
authentik POSTs to the API URL with `From`, `To`, `Body` (the token) and `Message` (full text). Any response status of 400 or higher counts as a failed send and blocks the user. A webhook mapping can reshape the payload:
```python
return {
    "from": stage.from_number,
    "to": device.phone_number,
    "body": f"foo bar baz {token}",
}
```

## Limit allowed numbers
Add a required text prompt with field key `phone` in a Prompt stage bound before the SMS stage (the SMS stage reads `prompt_data` instead of asking again), and bind a validation policy to the Prompt stage:
```python
phone_number = regex_replace(request.context["prompt_data"]["phone"], r"\s+", "")

if phone_number.startswith("+1234"):
    return True
ak_message("Invalid phone number or missing region code")
return False
```

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_sms/.
Nothing was removed.
Method: documentation only; no commands were run.
