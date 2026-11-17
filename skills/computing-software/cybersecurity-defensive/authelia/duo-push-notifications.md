---
id: computing-software.cybersecurity-defensive.authelia.duo-push-notifications
name: duo-push-notifications
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, duo, push-notification, mfa, second-factor, self-enrollment]
level: intro
status: docs-checked
description: "Add Duo push as an Authelia second factor with the duo_api section, hostname, integration and secret keys, and optional self-enrollment."
sources:
  - https://www.authelia.com/configuration/second-factor/duo/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia supports Duo mobile push as a second factor. Define the `duo_api` section only if you want it; leaving the section out means Duo is not used.

```yaml
duo_api:
  disable: false
  hostname: 'api-123456789.example.com'
  integration_key: '<DUO_INTEGRATION_KEY>'
  secret_key: '<DUO_SECRET_KEY>'
  enable_self_enrollment: false
```

Fields:

- `hostname`: the Duo API hostname, taken from the Duo admin dashboard.
- `integration_key`: a non-secret identifier, similar to a client ID, also from the dashboard.
- `secret_key`: the secret that proves your application is legitimate. The docs strongly recommend defining it as a secret rather than inline, especially for containerized deployments.
- `disable`: becomes automatically true when hostname, integration key and secret key are all empty or undefined.
- `enable_self_enrollment`: lets users enrol a device in Duo from within the Authelia portal.

Copy these three values from the Duo dashboard. The Duo push endpoint has its own rate limiter, `second_factor_duo`; the rate-limit page's example configuration shows 10 requests per 1 minute and 15 per 2 minutes.

Check: log in as a user with a registered Duo device and confirm a push arrives and approval completes the login.

## Checked

2026-11-08. Read the full Authelia Duo / Mobile Push page. Confirmed the duo_api options, the auto-disable rule and self-enrolment. The second_factor_duo bucket figures come from the rate-limit page example configuration and are labelled as such. Removed the unsourced _FILE environment variable instruction.

Method: documentation only; no commands were run.
