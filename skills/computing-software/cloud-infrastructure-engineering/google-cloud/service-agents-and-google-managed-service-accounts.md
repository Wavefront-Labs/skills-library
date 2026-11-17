---
id: computing-software.cloud-infrastructure-engineering.google-cloud.service-agents-and-google-managed-service-accounts
name: service-agents-and-google-managed-service-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-agents, google-managed-service-accounts, service-identity, gcp-sa, cmek-service-agent, iam]
level: practitioner
status: docs-checked
description: "Identify GCP service agents (service-PROJECT_NUMBER@gcp-sa-*), create them on demand with gcloud workload-identity, grant them CMEK roles, and know their default roles."
sources: ["https://cloud.google.com/iam/docs/service-agents", "https://cloud.google.com/iam/docs/create-service-agents", "https://cloud.google.com/kms/docs/cmek"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service agents and Google-managed service accounts

Service agents are Google-owned accounts that let a service access your resources, e.g.
`service-<PROJECT_NUMBER>@gcp-sa-pubsub.iam.gserviceaccount.com` (Pub/Sub, `roles/pubsub.serviceAgent`),
`service-<PROJECT_NUMBER>@compute-system.iam.gserviceaccount.com` (Compute Engine, `roles/compute.serviceAgent`),
`service-<PROJECT_NUMBER>@container-engine-robot.iam.gserviceaccount.com` (GKE, `roles/container.serviceAgent`),
`service-<PROJECT_NUMBER>@gs-project-accounts.iam.gserviceaccount.com` (Cloud Storage; no default role) and
`<PROJECT_NUMBER>@cloudservices.gserviceaccount.com` (Google APIs service agent; `roles/editor`).
If an API needs a service agent, Google Cloud creates it some time after you enable and use the API,
and grants its role automatically. Email formats and creation timing can change, so take them from the
service agents reference rather than memory.

## Find and create
```bash
PN=$(gcloud projects describe <P> --format="value(projectNumber)")
gcloud projects get-iam-policy <P> --flatten=bindings[].members \
  --filter="bindings.members~gcp-sa-|cloudservices|compute-system" --format="table(bindings.members,bindings.role)"
# policies-as-code: create the agents before the service is used
gcloud workload-identity service-agents generate --service=<ENDPOINT, e.g. aiplatform.googleapis.com> \
  --location=global --project=<PROJECT_NUMBER>
```
`--project`, `--folder` or `--organization` takes the numeric ID of the one resource you create for.
Agents created this way are **not** granted their roles automatically: grant the roles listed in the
response (the service agents reference gives each agent's default role). Needs Workload Identity API
Admin (`roles/workloadidentity.admin`) or `workloadidentity.serviceAgents.create`.

## Common grants you must make
| Need | Agent | Role on |
|---|---|---|
| CMEK for Cloud Storage | `service-$PN@gs-project-accounts.iam.gserviceaccount.com` | `roles/cloudkms.cryptoKeyEncrypterDecrypter` on the key |

For other services find the agent and the role it needs in that service's CMEK or Shared VPC page.

## Repair
If someone removed an agent's default role (authoritative Terraform is a likely cause), the service
can fail. Re-grant the role shown in the service agents reference for that agent.

## Gotchas
- Do not grant a service agent role to any principal except service agents; these roles can contain
  powerful permissions that change without notice. Pick a predefined or custom role instead.
- Do not let authoritative IAM resources remove the Google APIs service agent's `roles/editor`.

## Verify
- [ ] Every enabled service's agent holds the default role listed for it in the reference.

## Checked
2026-10-31. Confirmed against the IAM "Service agents" and "Create service agents" pages and the Cloud KMS
CMEK page: the agent emails and roles above, automatic role grant, the `gcloud workload-identity
service-agents generate` command, no automatic roles for agents created on request, and the CMEK role.
Removed: `gcloud beta services identity create`, the Shared VPC, Pub/Sub OIDC and Cloud Build grant rows,
the "disable and re-enable the API" repair and the domain-restricted-sharing exception advice, none of
which the pages state.
Method: documentation only; no commands were run.
