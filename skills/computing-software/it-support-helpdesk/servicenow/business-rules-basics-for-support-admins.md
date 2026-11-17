---
id: computing-software.it-support-helpdesk.servicenow.business-rules-basics-for-support-admins
name: business-rules-basics-for-support-admins
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, servicenow-business-rules, business-rules, server-side-scripting, before-after-async, support-admin]
level: practitioner
status: gated
description: "Read and write simple ServiceNow business rules safely as a support admin: when they run, before vs after vs async, conditions, current and previous, and debugging."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-api-reference/page/script/business-rules/concept/c_BusinessRules.html"
  - "https://developer.servicenow.com/dev.do#!/learn/learning-plans/zurich/new_to_servicenow/app_dev_business_rules"
  - "https://www.servicenow.com/docs/bundle/zurich-api-reference/page/script/business-rules/reference/r_BusinessRulesBestPractices.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# business-rules-basics-for-support-admins

Business rules (`sys_script`) are server-side logic that runs when records are queried,
inserted, updated or deleted. Many "the ticket changed by itself" mysteries are one.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## When they run
| When | Use for | Note |
|---|---|---|
| before | Set or validate fields on the record being saved | No `current.update()` needed |
| after | Update other records based on this change | Runs after DB write |
| async | Slow work (integrations, heavy queries) | Runs later in a scheduler worker |
| display | Pass data to client scripts via `g_scratchpad` | Runs on form load |
Order field controls sequence among rules on the same table and timing.

## Anatomy
- Table, When, Insert/Update/Delete/Query checkboxes.
- **Condition builder** (Filter conditions) and/or a script condition, e.g.
  `current.priority.changesTo(1)`.
- Script with `current` (the record) and `previous` (values before the update).

```javascript
// before update on incident: stamp when priority is raised to P1
(function executeRule(current, previous) {
  if (current.priority == 1 && previous.priority != 1) {
    current.u_p1_raised_at = new GlideDateTime();
  }
})(current, previous);
```

## Safety rules
- Never `current.update()` in a before rule (it's saved anyway) and avoid it in after
  rules (recursion, double notifications).
- Filter early with conditions so the script doesn't run on every update.
- Build in a sub-production instance, capture in an update set, test, then promote.
- Prefer no-code options first (UI policy, data policy, assignment rules, Flow Designer).

## Debugging "field changed by itself"
1. Record history / audit shows who changed the field (`system` = automation).
2. **Debug Business Rule** (System Diagnostics > Session Debug) shows rules executed on
   your next save.
3. Search `sys_script` for the field name in the script and conditions.
4. Check flows, workflows, data lookups and assignment rules too.

## Verify
After deploying a rule, session debug shows it running only when its condition is true,
and no duplicate notifications or recursion appear in the logs.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (developer.servicenow.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
