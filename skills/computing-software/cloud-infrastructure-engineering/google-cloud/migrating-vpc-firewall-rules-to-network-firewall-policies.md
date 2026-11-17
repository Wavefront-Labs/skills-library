---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-vpc-firewall-rules-to-network-firewall-policies
name: migrating-vpc-firewall-rules-to-network-firewall-policies
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-firewall, firewall-policy-migration, migrate-vpc-firewall-rules, network-firewall-policies, secure-tags, enforcement-order]
level: practitioner
status: docs-checked
description: "Migrate VPC firewall rules to global network firewall policies with the gcloud migration tool: network tags to secure tags, enforcement order, cutover and cleanup."
sources: ["https://cloud.google.com/firewall/docs/tags-firewalls-overview", "https://cloud.google.com/sdk/gcloud/reference/compute/network-firewall-policies", "https://cloud.google.com/sdk/gcloud/reference/compute/network-firewall-policies/rules/create", "https://cloud.google.com/firewall/docs/firewall-policies-rule-eval-order"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating VPC firewall rules to network firewall policies

Network firewall policies support secure tags (IAM-governed), FQDN, geolocation and threat intelligence match options, address
groups and Cloud NGFW features; VPC firewall rules do not. There is no `gcloud compute network-firewall-policies migrate`
command: the group offers `clone-rules`, `export-rules`, `import-rules`, `rules create` and similar, so VPC rules are
recreated in the policy by hand or by script.

## 1. Plan tags
Network tags cannot be used in policy rules, and VPC firewall rules do not support secure tags, so rules that target or
match network tags must be rewritten with **secure tags** (tag keys with purpose `GCE_FIREWALL` and a `network` or
`organization=auto` purpose-data). Record each network tag and the secure tag value that replaces it:
```bash
gcloud resource-manager tags keys create role --parent=organizations/ORG_ID --purpose=GCE_FIREWALL --purpose-data=network=NETWORK
gcloud resource-manager tags values create web --parent=tagKeys/TAG_KEY_ID
gcloud resource-manager tags bindings create --tag-value=tagValues/TAG_VALUE_ID --parent=FULL_RESOURCE_NAME_OF_VM
```
Purpose and purpose-data cannot be changed after the key is created. For new VMs, set the tags in instance templates with
`gcloud compute instance-templates create --resource-manager-tags=KEY=VALUE`.

## 2. Migrate
```bash
gcloud compute network-firewall-policies create prod-fw --global
gcloud compute network-firewall-policies rules create 1000 --firewall-policy=prod-fw --global-firewall-policy \
  --direction=INGRESS --action=allow --layer4-configs=tcp:443 --src-ip-ranges=SOURCE_RANGE \
  --target-secure-tags=TAG_VALUE
gcloud compute network-firewall-policies describe prod-fw --global
```
Recreate each VPC rule with the same priority, direction, action and ports. Rule priorities in different policies are
independent, so confirm the order after cutover. For ingress rules `--src-ip-ranges` or `--src-secure-tags` is required.

## 3. Associate and order
```bash
gcloud compute network-firewall-policies associations create --firewall-policy=prod-fw --network=prod \
  --name=prod-assoc --global-firewall-policy
gcloud compute networks update prod --network-firewall-policy-enforcement-order=BEFORE_CLASSIC_FIREWALL
```
Default order (`AFTER_CLASSIC_FIREWALL`): hierarchical policies, regional system policies, VPC firewall rules, global network
policy, regional network policy. Switching to `BEFORE_CLASSIC_FIREWALL` evaluates the network policies before the VPC rules. Test
the policy rules first, then delete the VPC rules.

## 4. Clean up
Enable firewall logging on the policy rules, watch Firewall Insights for rules with no hits,
delete VPC rules in batches, remove network tags no longer used.

## Gotchas
- Service-account targets are supported in policy rules (`--target-service-accounts`); network-tag rules must be rewritten with secure tags.
- Binding a secure tag value to a VM and using it in rules needs `roles/resourcemanager.tagUser`; creating keys and values needs `roles/resourcemanager.tagAdmin`.
- Instance templates and MIGs must carry secure tags (`--resource-manager-tags`) for new VMs.

## Verify
- [ ] Connectivity tests show traffic allowed or denied by the policy rules; no VPC firewall rules remain that you meant to replace.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `gcloud compute network-firewall-policies migrate` (reference page returns 404 and the command group lists clone-rules, export-rules, import-rules, get-effective-firewalls and others but no migrate) and `network-firewall-policies rules list` (the rules group has only create, delete, describe, update). Replaced with `rules create` and `describe`. The old migration page URL in sources also returned 404 and was replaced.
- Confirmed (secure tags overview): network tags cannot be used in policy rules, VPC firewall rules do not support secure tags, tag keys need purpose GCE_FIREWALL and purpose-data that cannot change after creation, roles/resourcemanager.tagAdmin and tagUser.
- Confirmed (gcloud reference): `resource-manager tags keys create --purpose --purpose-data`, `values create --parent=tagKeys/ID`, `bindings create --tag-value --parent`, `instance-templates create --resource-manager-tags`, `rules create` flags and the ingress source requirement.
- Confirmed (rule evaluation page): AFTER_CLASSIC_FIREWALL default order and BEFORE_CLASSIC_FIREWALL.
- Removed: the claim that outcomes are identical during overlap and the one-week observation period (not in documentation).

Method: documentation only; no commands were run.
