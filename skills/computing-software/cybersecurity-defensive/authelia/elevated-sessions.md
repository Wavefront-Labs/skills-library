---
id: computing-software.cybersecurity-defensive.authelia.elevated-sessions
name: elevated-sessions
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, elevated-session, identity-validation, one-time-code, sensitive-actions, second-factor]
level: advanced
status: docs-checked
description: "Configure Authelia elevated sessions with a one-time code, lifespans, characters and the require_second_factor and skip_second_factor options."
sources:
  - https://www.authelia.com/configuration/identity-validation/elevated-session/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Actions that may adjust the security characteristics of a user's account need an elevated session, so users are identified adequately first. Elevation is anchored to the user's remote IP and lasts a finite time. Users cannot revoke an active elevation manually, but they can revoke the one-time code so no new elevation is created from it.

```yaml
identity_validation:
  elevated_session:
    code_lifespan: '5 minutes'
    elevation_lifespan: '10 minutes'
    characters: 8
    require_second_factor: false
    skip_second_factor: false
```

- `code_lifespan` is the lifespan of the randomly generated one-time code (default 5 minutes).
- `elevation_lifespan` is how long the elevation lasts after the code is validated (default 10 minutes).
- `characters` is the code length (default 8), maximum currently 20. The docs recommend 8 to 12 and strongly discourage going below 8.
- `require_second_factor` makes second factor a prerequisite, but the code is still needed unless `skip_second_factor` is also on. It only affects users with a second factor registered.
- `skip_second_factor` treats second-factor sessions as elevated; one-factor users with a registered method are offered the choice of code or second factor.

With both options enabled, second factor is necessary and sufficient for users who have one, while users without one still use the code. Enabling either option also exposes second factor registration in user settings even if no rule uses `two_factor`.

The code endpoints are rate limited by `session_elevation_start` and `session_elevation_finish`.

Check: trigger a protected action as a one-factor user and confirm a one-time code is generated and delivered.

## Checked

2026-11-08. Read the full Authelia Elevated Session page. Confirmed the option defaults, the characters maximum and recommendation, the behaviour of require_second_factor and skip_second_factor and their combination table, and the user settings effect; confirmed the session_elevation limiters on the rate-limit page. Removed the claim that the code is emailed and the credential-management example, which the page does not state.

Method: documentation only; no commands were run.
