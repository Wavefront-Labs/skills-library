---
id: computing-software.devops-ci-cd.argo-workflows.webhook-clients
name: webhook-clients
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [webhooks, webhook-clients-secret, github-webhook, submit-workflow-template-role, signature-verification]
level: practitioner
status: docs-checked
description: "Accept signed webhooks (for example GitHub) at the events endpoint with a role, service account, binding and the webhook-clients secret."
sources: ["https://argo-workflows.readthedocs.io/en/latest/webhooks/", "https://argo-workflows.readthedocs.io/en/latest/access-token/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook client setup
Most clients send events with a standard Authorization header. Clients that rely on signature verification as proof of origin (GitHub, for example) need extra configuration in the namespace that receives the event:

1. A Role allowed to get workflow templates and create workflows (example: submit-workflow-template-role.yaml in the quick-start webhooks manifests).
2. A ServiceAccount for the client (example github.com-sa.yaml).
3. A RoleBinding from account to role (github.com-rolebinding.yaml).
4. A Secret named `argo-workflows-webhook-clients` listing the service accounts.

That secret tells Argo two things per account: which webhook type the account may be used for (such as `github`) and the secret value the webhook is configured with in the sender's settings page.

Request bodies for webhooks are limited to 2MB.

Use one service account per client. That lets you secure workflows correctly and revoke one client without affecting others.

## Checked
2026-11-08. Confirmed against the Argo Workflows Webhooks and Access Token pages: the role, service account, binding and `argo-workflows-webhook-clients` secret, the webhook type and secret it holds, the 2MB body limit, and one service account per client with independent revocation. Removed the uncited claim about exposing the Argo Server via Ingress or load balancer.
Method: documentation only; no commands were run.
