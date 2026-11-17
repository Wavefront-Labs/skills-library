---
id: computing-software.systems-network-administration.zabbix.trigger-dependencies
name: trigger-dependencies
category: computing-software
field: systems-network-administration
product: zabbix
tags: [trigger-dependency, root-cause, notification-suppression, router, dependency, trigger, dependencies]
level: practitioner
status: draft
description: "Suppress downstream notifications by making one trigger depend on another, and know the template and prototype rules."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/triggers/dependencies
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Zabbix has no host dependencies, but a trigger can depend on one or more other triggers. Classic case: a server behind a router. Make the server-down trigger depend on the router-down trigger, and while the router trigger is in Problem the server trigger does not change state, so no actions or notifications fire for it.

While the parent is in Problem, the dependent is not re-evaluated until the parent returns to OK, goes from Problem to Unknown, is closed manually or by correlation, is resolved by an item that is not part of the dependent trigger, or is disabled (or its item or host is). After that, the dependent trigger is updated only when it next receives a new metric, so the update may not be immediate.

Constraints:
- Dependencies can be added from any host trigger to any other host trigger, and from one template to another. If template A has a trigger depending on one in template B, template A can be linked only together with template B.
- A template trigger can depend on a host trigger. Linking creates a host trigger depending on the same trigger, so all hosts of the template depend on one router.
- A host trigger cannot depend on a template trigger.
- A trigger prototype can depend on another prototype in the same LLD rule or a real trigger, but not on a prototype from another rule or a trigger created from a prototype.

Configure it on the trigger's Dependencies tab.
