---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.host-naming-conventions-and-tag-compliance-reporting
name: host-naming-conventions-and-tag-compliance-reporting
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, tagging-naming, hostname-conventions, tag-compliance-report, naming-standard]
level: practitioner
status: draft
description: "Define host naming conventions that map cleanly to inventory groups, and report tag compliance across clouds with AWS Config, Azure Policy and inventory-driven checks."
sources: ["AWS tagging best practices (https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)", "AWS Config required-tags rule (https://docs.aws.amazon.com/config/latest/developerguide/required-tags.html)", "Azure naming and tagging (https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Host naming conventions and tag compliance

## Host naming
Pattern example: `<env>-<app>-<role>-<site><nn>` → `prd-pay-db-fra01`.
- Fixed-position, lowercase, dashes only (DNS-safe, Ansible group-safe after dash→underscore).
- No meaning that changes (owner names, IPs, OS versions).
- Make inventory grouping derivable:
```yaml
# constructed inventory
plugin: ansible.builtin.constructed
groups:
  env_prd: inventory_hostname is match('^prd-')
keyed_groups:
  - key: inventory_hostname.split('-')[1]
    prefix: app
  - key: inventory_hostname.split('-')[2]
    prefix: role
```
- For cloud instances, prefer **tags** as the source of truth (`Environment`, `App`, `Role`) and derive names from them; names are for humans and DNS.

## Tag compliance reporting
AWS:
```bash
aws configservice put-config-rule --config-rule '{"ConfigRuleName":"required-tags","Source":{"Owner":"AWS","SourceIdentifier":"REQUIRED_TAGS"},"InputParameters":"{\"tag1Key\":\"Owner\",\"tag2Key\":\"CostCenter\",\"tag3Key\":\"Environment\"}"}'
aws configservice get-compliance-details-by-config-rule --config-rule-name required-tags --compliance-types NON_COMPLIANT
aws resourcegroupstaggingapi get-resources --tag-filters Key=Owner --query 'length(ResourceTagMappingList)'
```
Azure: built-in policy "Require a tag on resources" in audit mode, compliance via `az policy state list --filter "complianceState eq 'NonCompliant'"`.
Inventory-driven (any platform):
```bash
ansible-inventory -i aws_ec2.yml --list | jq -r '._meta.hostvars | to_entries[] | select(.value.tags.Owner == null) | .key'
```

## Reporting cadence
Weekly report per owner/team with non-compliant counts and trend; feed backfill automation for safe tags; block creation without tags via policy in IaC (default_tags, SCP/Azure deny) once compliance is high.

## Verify
- [ ] Non-compliant resource count trends down and every host name parses into env/app/role groups.
