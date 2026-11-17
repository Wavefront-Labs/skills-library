---
id: computing-software.cybersecurity-defensive.keycloak.authz-resource-server-enforcement-mode
name: authz-resource-server-enforcement-mode
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, authorization-services, resource-server, enforcement-mode, decision-strategy]
level: practitioner
status: docs-checked
description: "Enable Keycloak Authorization Services on a confidential client and choose enforcing mode, decision strategy and remote resource management."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/authorization_services/topics/resource-server-enable-authorization.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authz resource server enforcement mode
An OIDC client can become a resource server: in the client's *Capability Config* toggle *Authorization Enabled* to On and save. An *Authorization* tab appears with sub-tabs *Settings*, *Resources*, *Authorization Scopes*, *Policies*, *Permissions*, *Evaluate* (simulate authorization requests and see how permissions and policies evaluate) and *Export Settings* (JSON file).

Resource server settings:
- **Policy Enforcement Mode**: `Enforcing` (default; requests are denied even when no policy is associated with a resource), `Permissive` (requests are allowed when no policy is associated), `Disabled` (no policy is evaluated and all resources are accessible).
- **Decision Strategy**: how the engine combines the outcomes of all evaluated permissions. `Affirmative`: at least one permission must be positive. `Unanimous`: all permissions must be positive.
- **Remote Resource Management**: if false, resources can be managed only from the administration console.

## Checked
2026-11-03. Confirmed against authorization_services/topics/resource-server-enable-authorization.adoc. Removed (not on the page): the "confidential client" requirement, the terminology paragraph, the Permissive-mode and export-to-version-control gotchas, and the Verify step.
Method: documentation only; no commands were run.
