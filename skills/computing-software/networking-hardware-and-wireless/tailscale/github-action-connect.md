---
id: computing-software.networking-hardware-and-wireless.tailscale.github-action-connect
name: github-action-connect
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [github-action, workload-identity, ci-tag]
level: practitioner
status: docs-checked
description: "Prerequisites and identity options for the Tailscale GitHub Action."
sources: ["https://tailscale.com/kb/1276"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailscale GitHub Action

Goal: let CI steps reach tailnet nodes such as a test database.

**Prerequisites**

- Tailscale Owner, Admin or Network admin permissions, and admin access to the GitHub repository.
- At least one configured tag for the ephemeral nodes, for example `tag:ci`; the access you grant that tag applies to the workflow.
- One credential: a federated identity client ID plus audience, or an OAuth client ID plus secret, or a reusable, ephemeral, tagged (and pre-approved if applicable) auth key.
- A runner image version of at least 2.237.1, needed for Node.js 24.

**Recommended auth.** Workload identity federation. The federated identity needs the `auth_keys` scope (Auth Keys > Write in the admin console). At run time the action exchanges a GitHub JWT identity token for an ephemeral node.

**Lifecycle**

- Ephemeral nodes created with a federated identity are pre-approved on tailnets with device approval.
- The action logs the node out right after the workflow completes, and the control server removes it automatically.

**Secrets.** Create repository secrets such as `TS_OAUTH_CLIENT_ID` and `TS_AUDIENCE` and reference them in the workflow.

**Checklist**

1. Tag created and granted least access.
2. Federated identity configured.
3. Secrets stored in GitHub.
4. Runner version checked.

## Checked

2026-11-03. Read Tailscale GitHub Action (kb/1276) and confirmed prerequisites, runner image 2.237.1, the `auth_keys` scope and ephemeral node lifecycle. Nothing else was removed.

Method: documentation only; no commands were run.
