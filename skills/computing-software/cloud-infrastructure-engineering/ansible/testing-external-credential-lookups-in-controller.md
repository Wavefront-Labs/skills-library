---
id: computing-software.cloud-infrastructure-engineering.ansible.testing-external-credential-lookups-in-controller
name: testing-external-credential-lookups-in-controller
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, credential-test, lookup-test, external-secret-management, hashicorp-vault, cyberark, credential-plugins, api]
level: advanced
status: docs-checked
description: "Test controller external credential lookups (Vault, CyberArk, Azure Key Vault) before jobs depend on them: the /test/ API endpoints, status codes and limits."
sources: ["https://github.com/ansible/awx/blob/devel/awx/api/views/__init__.py", "https://github.com/ansible/awx/blob/devel/awx/api/urls/credential.py", "https://github.com/ansible/awx/blob/devel/awx/api/urls/credential_type.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing external credential lookups in controller

Goal: prove a credential whose value comes from an external secret store resolves *before* a scheduled job finds out it does not.

## What can be tested
The AWX API describes the test endpoint as covering credentials that connect to external secret management systems: CyberArk AIM, CyberArk Conjur, HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Centrify Vault, Thycotic DevOps Secrets Vault and the GitHub App Installation Access Token lookup. It does not support standard credential types such as Machine, SCM and Cloud. Calling it on a non-external credential returns an error ("Credential is not testable.").

## Test an existing source credential
```bash
curl -s -X POST -H "Authorization: Bearer $CONTROLLER_TOKEN" -H "Content-Type: application/json" \
  https://controller.example.com/api/v2/credentials/<SOURCE_CRED_ID>/test/ \
  -d '{"metadata": {"<field>": "<value>"}}'
```
- The credential's saved inputs are used; `inputs` in the body override them, except values equal to `$encrypted$`, which are ignored so the stored secret is kept. `metadata` is merged on top, and its field names depend on the lookup plugin (path, key, version and so on).
- Result: HTTP 202 when the plugin backend call succeeds; HTTP 400 with the backend's error text in `detail` when it fails.
- You need the `use` permission on the credential.

## Test before saving
`POST /api/v2/credential_types/<TYPE_ID>/test/` with `{"inputs": {...connection fields...}, "metadata": {...}}` tests a complete set of inputs for an external credential type (non-external types are rejected with "Credential type is not testable.").

## Gotchas
- The test runs in the API service on the controller (using the task environment settings), not on an execution node or container group. A lookup that works in the test can still fail in a job if that node cannot reach the secret store.
- Connection timeouts are reported as the underlying connect-timeout message in `detail`.

## Verify
- [ ] The test call returns 202 for each source and metadata pair used by production templates.
- [ ] A canary job using the target credential succeeds on each instance group that will use it.

## Checked
2026-11-09. Checked against the AWX source: `CredentialExternalTest` and `CredentialTypeExternalTest` views (supported systems list, non-external rejection, input and metadata merge, `$encrypted$` handling, 202 and 400 responses), and the URL routes under `/api/v2/credentials/<pk>/test/` and `/api/v2/credential_types/<pk>/test/`.
Removed as unsupported: UI Test button walk-through, example Vault metadata keys and KV v1/v2 advice, Vault policy and token TTL troubleshooting table, the "nothing is cached" claim, hourly monitoring suggestion, and the Use-permission-on-both-credentials rule.
Method: documentation only; no commands were run.
