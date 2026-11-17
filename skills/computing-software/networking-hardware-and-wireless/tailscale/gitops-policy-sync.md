---
id: computing-software.networking-hardware-and-wireless.tailscale.gitops-policy-sync
name: gitops-policy-sync
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [gitops, policy-hujson, sync-acls-action]
level: advanced
status: docs-checked
description: "Use the Sync Tailscale ACLs action to test on pull requests and apply on merge."
sources: ["https://tailscale.com/kb/1306"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GitOps for the tailnet policy file

Goal: version-control and test policy changes.

**Prerequisites**

- A private GitHub repository for the policy file, since it contains personally identifiable information such as user emails.
- A federated identity, OAuth client or API access token (Trust credentials or Keys page).
- Working knowledge of commits and pull requests.

**Behaviour of the published action**

- On pull requests targeting `main`, the Test step (`action: test`) sends the policy to Tailscale to check validity and that all `tests` pass.
- On pushes (merges) to `main`, the Deploy step (`action: apply`) re-runs validity and tests and then updates the policy.
- Status shows in the Actions tab under the workflow in `.github/workflows/tailscale.yml`.
- You are not required to use this action; you can write your own or use another CI/CD tool.

**Inputs**

- `action` (required): `test` or `apply`.
- A credential (required): `oauth-client-id` with `audience`, or `oauth-client-id` with `oauth-secret`, or `api-key`.
- `policy-file` (optional): defaults to `policy.hujson` in the repository root.
- `tailnet` (required): your organization from General settings.

Start by copying the current policy from Access controls into `policy.hujson`.

**Checklist**

1. Private repo.
2. Test on PR, apply on merge.
3. Keep `tests` in the policy.

## Checked

2026-11-03. Read GitOps for the policy file (kb/1306) and confirmed prerequisites, test and apply steps, inputs and the default `policy.hujson` path. Nothing else was removed.

Method: documentation only; no commands were run.
