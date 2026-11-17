---
id: computing-software.cybersecurity-defensive.splunk.splunk-roles-and-index-access
name: splunk-roles-and-index-access
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, splunk-rbac, authorize-conf, srchindexesallowed, capabilities, saml-groups, least-privilege]
level: practitioner
status: draft
description: "Design Splunk roles in authorize.conf: index access, capabilities, search filters and quotas, mapped from SAML/LDAP groups with least privilege."
sources: ["Splunk Docs - Securing Splunk Enterprise (About configuring role-based user access)", "Splunk Docs - authorize.conf spec", "Splunk Docs - Configure SAML SSO"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splunk roles and index access (RBAC)

**Goal:** every analyst and app sees only the indexes and capabilities they need, and
access follows identity-provider groups rather than local accounts.

## Design pattern
1. One role per **data domain** (`idx_network`, `idx_endpoint`, `idx_hr_restricted`) that
   grants only `srchIndexesAllowed`.
2. One role per **job function** (`soc_analyst`, `detection_engineer`, `splunk_admin`) that
   grants capabilities and inherits the needed data roles.
3. Map IdP groups to job roles (SAML `[roleMap_SAML]` or LDAP group mapping). No local users
   except a break-glass admin.

## authorize.conf
```
[role_idx_endpoint]
srchIndexesAllowed = edr;sysmon;wineventlog
srchIndexesDefault = edr

[role_soc_analyst]
importRoles = user;idx_endpoint;idx_network
srchJobsQuota = 6
rtSrchJobsQuota = 0
srchDiskQuota = 500
srchMaxTime = 3600
```
- Restrict rows inside an index with `srchFilter` (e.g. `srchFilter = NOT sourcetype=hr:payroll`)
  but prefer separate indexes: filters from inherited roles are combined with OR, so
  inheritance can silently widen access.
- High-risk capabilities: `rtsearch`, `edit_*`, `admin_all_objects`, `run_custom_command`,
  `rest_properties_set`. Grant only to admin roles.
- Remove `delete_by_keyword` from everyone except a dedicated `can_delete` role used under change control.

## SAML mapping (authentication.conf)
```
[roleMap_SAML]
soc_analyst = SG-Splunk-SOC
splunk_admin = SG-Splunk-Admins
```

## Gotchas
- `importRoles` merges allowed indexes and capabilities upward; check effective rights with
  `| rest /services/authorization/roles splunk_server=local | table title imported_roles srchIndexesAllowed`.
- Wildcards in `srchIndexesAllowed` (`*`) grant future indexes too.
- In SHC, define roles in an app pushed from the deployer, not through the UI on one member.
- Internal indexes (`_internal`, `_audit`) expose search strings and user activity; limit them.

## Verify
- [ ] Log in as a test member of each IdP group and confirm `| eventcount summarize=false index=*` lists only expected indexes.
- [ ] No non-admin role holds `admin_all_objects` or `edit_roles`.
- [ ] `_audit` shows role changes and someone reviews them.
