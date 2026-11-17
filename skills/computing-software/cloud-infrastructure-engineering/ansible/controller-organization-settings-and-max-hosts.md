---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-organization-settings-and-max-hosts
name: controller-organization-settings-and-max-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, org-settings, org-max-hosts, organizations, galaxy-credentials, default-environment, subscription-hosts, multi-tenancy]
level: practitioner
status: docs-checked
description: "Configure controller organizations for multi-tenancy: max hosts cap, default execution environment, ordered Galaxy credentials, instance groups, notifications."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-controller-create-organization.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-content-sourcing.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/organization.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller organization settings and max hosts

Goal: each tenant organization gets its own limits and defaults so one team cannot consume the
shared host quota, the Galaxy access or another team's execution capacity.

## Settings per organization
| Setting | Effect |
|---|---|
| **Max hosts** | Cap on hosts in the organization. Default 0 means no limit. Adding a host once the cap is reached or exceeded fails with "You have already reached the maximum number of N hosts allowed for your organization. Contact your System Administrator for assistance." |
| **Execution environment** | Default EE members of the organization can use to run automation |
| **Instance groups** | Where the organization's jobs run; with more than one, list order sets execution precedence |
| **Galaxy credentials** (credentials of `kind=galaxy`) | Content sources for collections in `requirements.yml` during project updates; the ordered list sets precedence for sync and lookup |
| Notification templates | Organization-level started, success, error and approvals notifications |

## As code
```yaml
- ansible.controller.organization:
    name: NetOps
    description: Network automation tenant
    max_hosts: 1500
    default_environment: ee-network-2.4
    galaxy_credentials:
      - Automation Hub Published
      - Automation Hub Certified
    instance_groups: [netops-exec]
    notification_templates_error: [pagerduty-oncall]
    state: present
```
(`awx.awx.organization` takes the same parameters.) Galaxy credentials are exposed in the API at
`/api/v2/organizations/N/galaxy_credentials/`, an ordered list.

## Notes
- The default organization is created automatically; with a self-support licence only the default organization is available and it cannot be deleted.
- After upgrades, pre-existing global Galaxy settings were migrated into credentials attached to every organization; the controller continues to fetch roles from public Galaxy even if galaxy.ansible.com is not first in the list.
- Choose a max hosts value from the tenant's expected host count plus headroom; confirm the figure against your own subscription terms.

## Verify
- [ ] Adding a host beyond the cap shows the max hosts error.
- [ ] A project update in the organization installs collections from the first Galaxy credential in the list.

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (creating an organization, content sourcing from collections), ansible/awx devel organization.py.
- Confirmed: Max hosts default and error text, execution environment, instance group ordering, Galaxy credentials kind and ordering, API endpoint, default organization and self-support limits, module parameters including notification templates.
- Removed unconfirmed claims: only superusers can change max hosts, inventory syncs erroring when over the cap, "first match wins" wording, how hosts are counted for the cap or subscription (unique hostnames, smart inventories, host metrics view), a +10% sizing rule, new organizations needing Galaxy credentials to avoid sync failure, lowering the cap not deleting hosts, org admin limits, the `-vvv` verification, `infra.aap_configuration` equivalent.

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
