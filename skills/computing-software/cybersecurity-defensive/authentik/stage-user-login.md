---
id: computing-software.cybersecurity-defensive.authentik.stage-user-login
name: stage-user-login
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, user-login-stage, session-duration, network-binding, remember-me, geoip-binding]
level: practitioner
status: docs-checked
description: "Configure the authentik User Login stage: session duration, network and GeoIP binding, remember me offset, remember device and terminating other sessions."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/user_login/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: attach the pending user to a new session, usually the last stage of authentication, enrolment and recovery flows (after Password, Authenticator Validation or User Write).

## Options
- **Session duration**: `seconds=0` keeps the session until the browser session ends, though some browsers can retain it longer.
- **Network binding** (ASN, network, IP) and **GeoIP binding** (continent, country, city): authentik terminates sessions that later violate the binding. The logout event then includes `binding` (with `reason` such as `network.missing`, `new_value`, `previous_value`), `asn`, `geo`, `ip` and `logout_reason` "Session binding broken".
- **Terminate other sessions**: revokes the user's other sessions; OAuth refresh tokens are not affected.
- **Remember me offset**: extends the session when the user ticks **Remember me on this device**; `seconds=0` hides the option.
- **Remember device**: sets a longer-lived cookie that lets later flows and policies tell known from unknown devices. A sign-in from an IP that already has an authenticated session for the user also counts as known.

## Duration syntax
`hours=1,minutes=30,seconds=0`. Valid keys: microseconds, milliseconds, seconds, minutes, hours, days, weeks. Floats are accepted.

## Use
The known/unknown device classification can drive notification rules, for example alerting on logins from unknown devices (see the notification rule expression policy examples).

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/user_login/.
Nothing was removed.
Method: documentation only; no commands were run.
