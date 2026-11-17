---
id: computing-software.networking-hardware-and-wireless.check-point.api-bulk-automation-and-install
name: api-bulk-automation-and-install
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, api-automation, bulk-objects, install-policy-api]
level: practitioner
status: draft
description: "Script bulk rule and object updates with the Check Point API: JSON batch import, task polling and safe publish."
sources:
  - https://sc1.checkpoint.com/documents/latest/APIs/
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CommandLineInterfaceReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk object changes and install via the API

```
mgmt_cli -r true show tasks --format json
mgmt_cli -r true show task task-id "01234567-89ab-cdef-0123-456789abcdef" --format json
mgmt_cli -r true add host --batch hosts.csv --format json
mgmt_cli -r true install-policy policy-package Standard access true targets.1 gw1 --format json
```
- The `--batch <csv>` option runs one command per CSV row; the header row holds parameter names (`name,ip-address`), and lists use dotted names (`tags.1`). It stops on the first error unless `-c`/ `--continue-on-error` (confirm).
- Long operations return a `task-id`; poll with `show task` until `status` is `succeeded`, `failed` or `partially succeeded`; `install-policy` also returns a task. Check `task-details[0].statusDescription` for the reason.
- Dry run: use `set session` with description, or `verify-policy policy-package Standard` before `install-policy`.
- Large rulebases: use `show access-rulebase ... limit 500 offset 500` to page, and `use-object-dictionary true` to cut size.
- Keep changes in one session per ticket; publish with `set session description "CHG1234"` first, so the audit trail links to the change.
- Gotcha: the API runs under SmartConsole concurrency rules; a session in SmartConsole holding the lock on an object makes the API call fail with "locked by another session".

Verify: `show task` reports `succeeded`; re-read the object (`show host name h2`) and review in the SmartConsole audit log.
