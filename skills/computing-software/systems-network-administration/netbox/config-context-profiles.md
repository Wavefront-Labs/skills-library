---
id: computing-software.systems-network-administration.netbox.config-context-profiles
name: config-context-profiles
category: computing-software
field: systems-network-administration
product: netbox
tags: [context-profile, json-schema, schema-validation]
level: advanced
status: docs-checked
description: "Group contexts under a profile that enforces a JSON schema."
sources: ["https://netboxlabs.com/docs/netbox/features/context-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Config context profiles

Goal: stop malformed context data from being saved.

A config context profile is an organizational grouping for related config contexts. It may optionally enforce a JSON schema describing the shape of their data.

**Behaviour.** When a profile is assigned to a config context, NetBox validates the context's data against the profile's schema. Invalid data is rejected at save time.

**Authoring the schema**

- Write it directly in NetBox, or
- Populate it from an external data source so schemas live alongside code or configuration in a repository.

**Pattern**

1. Create the profile, for example for NTP and syslog settings.
2. Add a JSON schema requiring the expected keys and types, such as arrays of strings for `syslog-servers`.
3. Assign the profile to each related config context.
4. Save; NetBox rejects data that violates the schema.

The context itself may still hold any JSON, as long as it satisfies the profile if one is set.

**Checklist**

1. One profile per data family.
2. Schema kept in a synced data source if possible.
3. Assign the profile to every related context.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Context Data feature page (Profiles & Schema Validation section, page read in full). Removed the unconfirmed rationale paragraph.
