---
id: computing-software.cybersecurity-defensive.keycloak.admin-events-auditing
name: admin-events-auditing
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, admin-events, audit, include-representation, admin-api]
level: practitioner
status: docs-checked
description: "Record Keycloak admin events with Include representation JSON to audit actions made through the Admin Console and REST API."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/events/admin.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admin events auditing
Keycloak can record all actions an administrator performs in the Admin Console. The console works by calling the Keycloak REST interface, and Keycloak audits those REST invocations.

Enable in *Realm settings* > *Events* tab > *Admin events settings* tab:
1. Toggle *Save events* ON; the *Include representation* switch then appears.
2. Toggle *Include representation* ON to include the JSON documents sent through the admin REST API, so you can see what the administrators did.
3. Click *Save*.

*Clear admin events* removes the stored actions from the database. View them under *Events* > *Admin events* tab.

Size limit: with Include representation ON a lot of data can be stored. Cap the representation length with `--spi-events-store--jpa--max-field-length`, useful to respect underlying storage limits:
```
kc.sh --spi-events-store--jpa--max-field-length=2500
```

## Checked
2026-11-03. Confirmed against server_admin/topics/events/admin.adoc: procedure, Include representation meaning and the max-field-length option. Removed: the column list, operation names, SIEM and sensitive-data advice, the "no retroactive history" gotcha and the invented Verify step, none of which are on the page.
Method: documentation only; no commands were run.
