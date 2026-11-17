---
id: computing-software.cloud-infrastructure-engineering.google-cloud.network-firewall-policies-with-gcloud-and-service-account-targets
name: network-firewall-policies-with-gcloud-and-service-account-targets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-firewall, gcloud-compute-firewall-policies, firewall-policy-rules-gcloud, regional-network-firewall-policy, global-network-firewall-policy, target-service-accounts, service-account-firewall-targets, secure-tags]
level: practitioner
status: docs-checked
description: "Manage global and regional network firewall policies with gcloud, target rules by secure tags or service accounts instead of network tags, and order them with hierarchical policies."
sources: ["https://cloud.google.com/firewall/docs/use-network-firewall-policies", "https://cloud.google.com/firewall/docs/firewalls", "https://cloud.google.com/firewall/docs/tags-firewalls-overview", "https://cloud.google.com/firewall/docs/firewall-policies-rule-eval-order", "https://cloud.google.com/sdk/gcloud/reference/compute/network-firewall-policies/rules/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network firewall policies with gcloud and SA targets

## 1. Evaluation order
Default (`AFTER_CLASSIC_FIREWALL`): hierarchical policies (org, then folders), regional system policies, VPC firewall rules, global
network firewall policy, regional network firewall policy, implied actions. `BEFORE_CLASSIC_FIREWALL`, set with the network's
`--network-firewall-policy-enforcement-order`, evaluates global and regional network policies before the VPC rules. `goto_next`
continues to the next step; `allow` and `deny` stop evaluation.

## 2. Global network firewall policy
```bash
gcloud compute network-firewall-policies create prod-fw --global --description="prod VPC"
gcloud compute network-firewall-policies rules create 1000 --firewall-policy=prod-fw --global-firewall-policy \
  --direction=INGRESS --action=allow --layer4-configs=tcp:443 \
  --src-ip-ranges=35.191.0.0/16,130.211.0.0/22 --target-secure-tags=WEB_TAG_VALUE --enable-logging
gcloud compute network-firewall-policies rules create 1100 --firewall-policy=prod-fw --global-firewall-policy \
  --direction=INGRESS --action=allow --layer4-configs=tcp:5432 \
  --src-secure-tags=APP_TAG_VALUE --target-secure-tags=DB_TAG_VALUE
gcloud compute network-firewall-policies associations create --firewall-policy=prod-fw \
  --network=prod --name=prod-assoc --global-firewall-policy
```
## 3. Regional policy
Same commands, but the flag differs by command: `network-firewall-policies create`, `describe` and `import-rules` take `--region=REGION`
instead of `--global`, while `rules create`/`update` and `associations create` take `--firewall-policy-region=REGION` instead of
`--global-firewall-policy`. Use regional policies for region-specific rules or regional admin delegation.

## 4. Targeting
| Target | Security | Notes |
|---|---|---|
| Secure tags (Resource Manager tags) | IAM-controlled (`roles/resourcemanager.tagUser` to bind or use) | policy rules only; VPC firewall rules do not support them |
| Service accounts | tied to the VM's attached service account | VPC rules: `--target-service-accounts` / `--source-service-accounts`; policy rules: `--target-service-accounts`; cannot be combined with network tags in one VPC rule |
| Network tags | any IAM principal who can edit an instance can change them | VPC rules only; policy rules cannot use them; avoid for security boundaries |
VPC rule example: `gcloud compute firewall-rules create allow-app-db --network=prod --allow=tcp:5432 --source-service-accounts=app@PROJECT_ID.iam.gserviceaccount.com --target-service-accounts=db@PROJECT_ID.iam.gserviceaccount.com`.

## Gotchas
- Secure tag keys must be created with `--purpose=GCE_FIREWALL` and purpose-data (`network` or `organization=auto`); neither can be changed later.
- A policy not associated with the network does nothing — check associations.
- Leave gaps (100s) between priority numbers for later inserts.

## Verify
- [ ] `gcloud compute network-firewall-policies get-effective-firewalls --network=prod` (or the per-VM `instances network-interfaces get-effective-firewalls`) shows the expected rules.
- [ ] Firewall rules logging shows hits on 1000/1100 and denies elsewhere.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: regional policy rules and associations use `--firewall-policy-region`, not `--region` (rules create/update and associations create synopses); `network-firewall-policies create`, `describe` and `import-rules` do use `--region`/`--global`.
- Found wrong: evaluation order was stated loosely; the rule evaluation page gives the full default order and the BEFORE_CLASSIC_FIREWALL alternative.
- Confirmed (secure tags overview and firewalls page): secure tags only in policy rules, VPC rules do not support them, network tags unusable in policy rules, tagUser role, GCE_FIREWALL purpose; network tags and service accounts cannot be used in the same VPC rule; any IAM principal who can edit an instance can change its network tags.
- Confirmed (gcloud reference): `rules create` flags (--layer4-configs, --src-ip-ranges, --src-secure-tags, --target-secure-tags, --target-service-accounts, --enable-logging), `associations create` flags, `get-effective-firewalls --network`.
- Removed: the stop-plus-actAs claim, the cross-peering claim for tags and the per-policy priority statement (no confirming documentation read). Replaced the unverified secure tag name format in examples with placeholders.

Method: documentation only; no commands were run.
