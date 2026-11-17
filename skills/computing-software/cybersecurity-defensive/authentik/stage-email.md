---
id: computing-software.cybersecurity-defensive.authentik.stage-email
name: stage-email
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, email-stage, recovery-flow, custom-templates, account-recovery, smtp]
level: practitioner
status: docs-checked
description: "Configure the authentik Email stage: SMTP options, recovery rate limiting, overriding the recipient, activate-on-success, custom Django templates in Docker or Kubernetes."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/email/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: send a tokenized verification or recovery email from a flow. Failed deliveries are retried by the background worker.

## Options
**Use global connection settings** (or stage-specific **SMTP Host/Port/Username/Password**, **Use TLS** = STARTTLS, **Use SSL** = SMTPS, **Timeout**), **From address**, **Account Recovery Max Attempts** and **Account Recovery Cache Timeout** (rate limit recovery emails only), **Token expiry**, **Subject**, **Template**, and **Activate user on success**.

**Activate user on success** sets `is_active` True when the user returns with a valid token, letting an inactive user self-reactivate in recovery. Disabling it does not stop an inactive user getting a recovery email or changing the password.

## Override the recipient
Default is `pending_user`. Set `email` in the plan context from an expression policy before the stage:
```python
request.context["flow_plan"].context["email"] = request.context["prompt_data"]["email"]
return True
```
Or from an attribute: `request.context["pending_user"].attributes.get("otherEmail")`.

## Enumeration behavior
With Identification's **Pretend user exists**, an unknown identifier gets the same **Email sent.** challenge but no email or token. An existing inactive user is not a placeholder and does receive a recovery email; block that with a Deny stage (the response then differs and discloses state).

## Custom templates
- Docker Compose: put templates in a `custom-templates` directory next to the Compose file; they become selectable in the stage.
- Kubernetes: create a ConfigMap (for example `authentik-templates`) with `my-template.html`, then in Helm values add `volumes` (configMap) and `volumeMounts` with `mountPath: /templates` for the worker.
- A matching `.txt` file next to the `.html` makes multipart mail.
- If the template is not listed, check the worker logs.

Templates are Django templates extending `email/base.html`; variables are `url`, `user`, `expires`. Each `{% ... %}` tag must stay on one line or it will not parse.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/email/.
Nothing was removed.
Method: documentation only; no commands were run.
