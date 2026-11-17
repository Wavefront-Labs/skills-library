---
id: computing-software.cloud-infrastructure-engineering.google-cloud.service-account-key-rotation-and-disabling-key-creation
name: service-account-key-rotation-and-disabling-key-creation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-account-keys, service-account-key-rotation, disable-key-creation, disableserviceaccountkeycreation, disableserviceaccountkeyupload, key-expiry, key-rotation-automation, user-managed-keys, key-inventory, iam-disable-key]
level: practitioner
status: docs-checked
description: "Block user-managed SA keys org-wide with the key-creation constraints, inventory and expire existing keys, and rotate unavoidable ones with a create-disable-delete cycle."
sources: ["https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys", "https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts", "https://cloud.google.com/iam/docs/keys-create-delete", "https://cloud.google.com/sdk/gcloud/reference/iam/service-accounts/keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service account key rotation and disabling key creation

**Goal:** zero long-lived JSON keys in the organisation except an explicit allowlist, each of
which is inventoried, expiring and rotated on a schedule.

## 1. Prevent new keys (org policy)
Google's guide lists `iam.disableServiceAccountKeyCreation` and `iam.disableServiceAccountKeyUpload` as legacy
managed constraints and recommends the equivalent managed constraints `iam.managed.disableServiceAccountKeyCreation` and
`iam.managed.disableServiceAccountKeyUpload`. The legacy form is shown here; check the managed form's policy syntax on the
*Restricting service accounts* page before switching.
```bash
for c in iam.disableServiceAccountKeyCreation iam.disableServiceAccountKeyUpload; do
cat > p.yaml <<EOF
name: organizations/<ORG_ID>/policies/$c
spec: { rules: [ { enforce: true } ] }
EOF
gcloud org-policies set-policy p.yaml; done
```
Exceptions: set the same policy with `enforce: false` on the specific project (or use a
tag-conditioned rule) that genuinely needs a key — third-party SaaS that cannot do WIF. Record
the reason in the policy YAML in git.

Also `iam.serviceAccountKeyExpiryHours` (a list constraint) limits how long new keys stay valid. Allowed values on the
constraints page: 1h, 8h, 24h, 168h, 336h, 720h, 1440h, 2160h. It cannot merge with a parent policy (set
`inheritFromParent: false`) and it is not retroactive, so existing keys keep their expiry. It is the backstop for allowed projects.

## 2. Inventory what exists
```bash
gcloud asset search-all-resources --scope=organizations/<ORG_ID> \
  --asset-types=iam.googleapis.com/ServiceAccountKey
# per SA
gcloud iam service-accounts keys list --iam-account=<SA_EMAIL> --managed-by=user \
  --format='table(name.basename(),validAfterTime,validBeforeTime,disabled)'
```
`--managed-by=user` limits the list to user-managed keys (the flag defaults to `any`). A service account can have at most 10 keys.

## 3. Rotation cycle (for the keys you must keep)
```bash
SA=svc@<PROJECT_ID>.iam.gserviceaccount.com
gcloud iam service-accounts keys create new.json --iam-account=$SA        # 1. create (expires per policy)
# 2. deploy new.json to the consumer (vault/secret store), confirm it authenticates
gcloud iam service-accounts keys disable <OLD_KEY_ID> --iam-account=$SA   # 3. disable, wait a soak period
gcloud iam service-accounts keys delete <OLD_KEY_ID> --iam-account=$SA    # 4. delete
```
Disable-before-delete is the rollback: a disabled key can be re-enabled with `keys enable`; a deleted
one cannot. Soak 24-72 h watching the consumer's error rate. Automate with Cloud Scheduler →
function that performs steps 1-3 and writes the new key into Secret Manager, with the
consumer reading from Secret Manager (then the "key" is effectively a Secret Manager secret
and rotation is invisible to it).

## 4. Detect key misuse
- Alert on service account key creation in the organisation audit log sink (any key creation is a policy exception).
- Leaked key: `keys disable` immediately (not delete, you may need forensic data), then rotate.

## Gotchas
- By default service account keys never expire (IAM docs); `keys create` has only `--iam-account` and `--key-file-type`, so the expiry org policy is the only enforcement.
- Prefer not to create keys from Terraform; the private key would land in state.

## Verify
- [ ] `gcloud org-policies describe iam.disableServiceAccountKeyCreation --organization=<ORG_ID> --effective` shows `enforce: true`.
- [ ] Asset inventory lists only allowlisted keys, all with an expiry no longer than the policy allows.
- [ ] A rotation run leaves the consumer healthy and the old key in `disabled: true` before deletion.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud reference for `iam service-accounts keys` (create, list `--managed-by` default `any`, disable, enable, delete), `org-policies describe --effective`, the Restricting service accounts page (legacy and managed key-creation and key-upload constraints), the constraints list (`iam.serviceAccountKeyExpiryHours` allowed values, no merge with parent, not retroactive) and the IAM key page (10-key limit, keys never expire by default).
- Removed unconfirmed claims: Recommender insight type and 90-day unused-key insight, audit-log field names and method name, system keys undeletable, disabled-SA key behaviour, `FAILED_PRECONDITION` text, the 10-year default and the 90-day verify target. Terraform state advice shortened to a recommendation.

Method: documentation only; no commands were run.
