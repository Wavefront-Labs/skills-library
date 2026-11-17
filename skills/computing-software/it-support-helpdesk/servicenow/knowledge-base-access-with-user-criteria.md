---
id: computing-software.it-support-helpdesk.servicenow.knowledge-base-access-with-user-criteria
name: knowledge-base-access-with-user-criteria
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, knowledge-user-criteria, knowledge-management, user-criteria, can-read, can-contribute]
level: practitioner
status: gated
description: "Control who can read and contribute to ServiceNow knowledge bases and articles with user criteria, and debug why a user can or cannot see an article."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/knowledge-management/concept/user-access-knowledge.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/knowledge-management/concept/c_KnowledgeManagement.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/users-and-groups/concept/c_UserCriteria.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# knowledge-base-access-with-user-criteria

User criteria (`user_criteria`) are reusable rules: users, groups, roles, companies,
departments, locations, or a script. Knowledge uses them at two levels.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Where they apply
| Level | Can Read | Cannot Read | Can Contribute | Cannot Contribute |
|---|---|---|---|---|
| Knowledge base | Who sees the KB | Explicit exclusion | Who can create/edit | Exclusion |
| Article | Narrow further within the KB | Exclusion | n/a | n/a |
Rules: **Cannot** always wins over **Can**. If a KB has no Can Read criteria, everyone
(including guests on public portals, depending on settings) can read it. Article-level
criteria only restrict further; they can't grant access the KB denies.

## Typical design
- **IT internal KB**: Can Read = itil role; Can Contribute = itil.
- **Employee KB**: Can Read = all internal users (criteria "Employees", not empty);
  Can Contribute = knowledge authors group.
- **Region/company KB**: Can Read = company = X or location in region.
- Sensitive articles (HR, security procedures) go in a separate KB rather than relying on
  article-level exclusions in a broad KB.

## Debugging "user can't see article"
1. Article state is **Published** and within Valid to date.
2. KB Can Read / Cannot Read criteria: does the user match? Check group and role
   membership and the company/location on their user record.
3. Article-level criteria.
4. Portal: is the KB attached to that portal's knowledge configuration?
5. Impersonate the user (with care, logged) and search; or use the user criteria
   diagnostics if available in your release.
Criteria results are cached per session; after a group change the user may need to log
out and back in.

## Pitfalls
- Scripted criteria that are slow run on every search; prefer declarative ones.
- Empty Can Read on a KB created for IT exposes internal workarounds to all users.

## Verify
Test with one user in and one out of each criteria; both see exactly what's intended in
the portal and in search.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
