---
id: computing-software.cloud-infrastructure-engineering.google-cloud.privileged-access-manager-just-in-time-access
name: privileged-access-manager-just-in-time-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, privileged-access-manager, pam-entitlements, just-in-time-access, temporary-elevation, break-glass]
level: practitioner
status: docs-checked
description: "Set up Privileged Access Manager entitlements for just-in-time, approved, time-bound IAM elevation, request and approve grants with gcloud, and audit them."
sources: ["https://cloud.google.com/iam/docs/pam-overview", "https://cloud.google.com/iam/docs/pam-create-entitlements", "https://cloud.google.com/sdk/gcloud/reference/pam"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privileged Access Manager (just-in-time access)

PAM replaces standing admin grants with **entitlements**: who may request which roles on a
resource, for how long, and whether approval is needed. A grant adds a conditional IAM binding
that expires automatically.

## Setup
```bash
# enable the Privileged Access Manager API and complete the setup steps in the PAM guide first
cat > ent.yaml <<'EOF'
eligibleUsers:
- principals: [group:sre-oncall@example.com]
privilegedAccess:
  gcpIamAccess:
    resourceType: cloudresourcemanager.googleapis.com/Project
    resource: //cloudresourcemanager.googleapis.com/projects/<P>
    roleBindings:
    - role: roles/compute.admin
    - role: roles/container.admin
maxRequestDuration: 14400s
requesterJustificationConfig: {unstructured: {}}
approvalWorkflow:
  manualApprovals:
    requireApproverJustification: true
    steps:
    - approvers: [{principals: [group:sre-leads@example.com]}]
additionalNotificationTargets: {adminEmailRecipients: [secops@example.com]}
EOF
gcloud pam entitlements create prod-admin --entitlement-file=ent.yaml --location=global --project=<P>
```

## Request, approve, end
```bash
gcloud pam grants create --entitlement=prod-admin --requested-duration=3600s \
  --justification="INC-4821 node pool stuck" --location=global --project=<P>
gcloud pam grants search --entitlement=prod-admin --caller-relationship=<CALLER_RELATIONSHIP> --location=global --project=<P>   # see `gcloud pam grants search --help` for the values
gcloud pam grants approve <GRANT> --reason="ok" --entitlement=prod-admin --location=global --project=<P>
gcloud pam grants revoke <GRANT> --reason="done" --entitlement=prod-admin --location=global --project=<P>
```

## Gotchas
- The PAM overview says a grant adds the listed roles until the end of the grant duration, after which PAM revokes them.
- Remove the standing grants PAM replaces, or it adds nothing.

## Verify
- [ ] Audit logs show the grant request, approval and the role removal at expiry.
- [ ] `gcloud projects get-iam-policy <P>` shows no standing compute.admin for the SRE group.

## Checked

- Date: 2026-10-27
- Confirmed against the PAM overview and create-entitlements guide (entitlement YAML: `privilegedAccess.gcpIamAccess` with `resourceType`, `resource`, `roleBindings`; `maxRequestDuration`, `eligibleUsers`, `approvalWorkflow.manualApprovals` with `requireApproverJustification` and `steps`, `requesterJustificationConfig.unstructured`, `additionalNotificationTargets.adminEmailRecipients`) and the gcloud references for `pam entitlements create` (`--entitlement-file`, `--location`), `pam grants create` (`--entitlement`, `--requested-duration`, `--justification`), `grants approve` (`--reason`), `grants revoke` and `grants search` (`--caller-relationship`).
- Removed: auto-granted service agent role claim, `can-approve` value (only `had-created` is shown on the page read), self-approval, Terraform overwrite, folder/org setup and audit-event-name claims, and the `gcloud services enable` line (setup is now deferred to the guide).

Method: documentation only; no commands were run.
