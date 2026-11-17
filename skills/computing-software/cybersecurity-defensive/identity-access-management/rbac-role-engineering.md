---
id: computing-software.cybersecurity-defensive.identity-access-management.rbac-role-engineering
name: rbac-role-engineering
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [identity-lifecycle, role-engineering, rbac, role-mining, abac, entitlement-management, least-privilege, separation-of-duties, access-packages]
level: advanced
status: draft
description: "Engineer RBAC roles from real entitlement data: role mining, business vs technical roles, separation-of-duties rules, and when ABAC fits better."
sources: ["NIST RBAC model (INCITS 359)", "NIST SP 800-162 Guide to Attribute Based Access Control", "CSF 2.0 PR.AA-05 (least privilege and separation of duties)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Role engineering for RBAC

**Goal:** a manageable set of roles that grant least privilege by job function, so access is
consistent, reviewable and quick to grant.

## Approach
1. **Collect entitlements**: export who has what from IdP groups, key applications and cloud IAM.
2. **Role mining (bottom-up)**: cluster users by common entitlements within departments/job codes;
   entitlements held by 80%+ of a job group are role candidates. IGA tools help; a pandas
   pivot of user x entitlement works for a first pass.
3. **Top-down validation**: business owners confirm the role makes sense for the job ("Accounts Payable Clerk"), remove accidental entitlements.
4. Define two layers:
   - **Business roles** (job functions) assigned to people, often automatically from HR attributes.
   - **Technical roles / permission sets** per application, bundled into business roles.
5. **Separation of duties (SoD)** rules: conflicting entitlements (create vendor + approve payment) that must not combine; enforce at request time and detect in reviews.
6. Exceptions handled through requestable access packages with approval and expiry.

## Role quality targets
- Roles cover most access for most people (e.g. 70-80% of entitlements by role, the rest by request).
- Role count well below user count; if there are as many roles as people, you have role explosion.
- Each role has an owner, description, and review schedule.

## When ABAC is better
Access depending on attributes that vary widely (region, data classification, project,
customer), for example "analysts can read records of their own region". Use attributes and
policies (cloud IAM conditions, ABAC in Azure storage, AWS tags with `aws:PrincipalTag`)
instead of creating a role per combination.

## Gotchas
- Mining from current access codifies existing over-privilege; clean up first or validate hard.
- Roles defined but not provisioned automatically drift from reality.
- Nested groups across systems hide effective access; flatten for review.

## Verify
- [ ] SoD conflict report shows zero unapproved conflicts.
- [ ] New joiners in pilot departments get full working access by role alone on day one.
