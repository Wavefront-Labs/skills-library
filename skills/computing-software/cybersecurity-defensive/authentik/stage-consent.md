---
id: computing-software.cybersecurity-defensive.authentik.stage-consent
name: stage-consent
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, consent-stage, authorization-flow, consent-header, stored-consent]
level: practitioner
status: docs-checked
description: "Configure the authentik Consent stage: consent modes and expiry, the default explicit-consent flow, and customizing the consent text with consent_header."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/consent/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: ask users to approve sharing profile data with an application in an authorization flow.

The built-in `default-provider-authorization-explicit-consent` flow already contains a Consent stage, so you normally add nothing.

## Options
**Mode**: **Always require consent**, **Consent given lasts indefinitely**, or **Consent expires**; **Consent expires in** sets the offset for the last mode. authentik stores the user, application and granted permissions; users can review past approvals in User Settings.

## Add to a custom authorization flow
1. **Flows and Stages > Stages**: create a **Consent Stage**, choose Mode and expiry.
2. Open the authorization flow > **Stage Bindings** and add the stage.

## Custom consent text
Bind an expression policy to the Consent stage binding (expand the binding under **Stage Bindings**):
```python
request.context["flow_plan"].context["consent_header"] = (
    "Are you OK with your IdP provider sharing your user identification data "
    "with the application?"
)
return True
```
The `consent_header` key is read from the flow context before the stage runs.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/consent/.
Removed as not confirmed by that page: consent_permissions and automatic consent_header claims.
Method: documentation only; no commands were run.
