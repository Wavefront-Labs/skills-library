---
id: computing-software.digital-privacy-hygiene.password-managers.family-and-team-vault-administration
name: family-and-team-vault-administration
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, bitwarden-organizations, 1password-families, collections, groups, offboarding, break-glass, organiser-recovery, least-privilege, shared-vault-admin, admin-recovery]
level: practitioner
status: draft
description: "Administer a Bitwarden/1Password family or team plan: collections and least-privilege groups, offboarding that actually revokes access, and a break-glass plan if the admin is unreachable."
sources:
  - "https://bitwarden.com/help/about-organizations/"
  - "https://support.1password.com/families/"
  - "https://bitwarden.com/help/user-types-access-control/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Family and team vault administration

**Goal:** run a shared Bitwarden Organization or 1Password Families/Teams plan so
each person sees only what they need, leaving removes their access immediately
and completely, and the whole plan survives the admin being unreachable.

## 1. Structure before you invite anyone
- **Collections (Bitwarden) / Vaults (1Password)**: create one per real grouping
  — "Household bills," "Kids' streaming," "Shared work tools" — rather than one
  flat shared vault everyone sees entirely. Assign each person/group only the
  collections relevant to them (least privilege, not convenience).
- **Groups**: for a team plan, put people in groups (e.g. "Engineering,"
  "Finance") and assign collection access to the group, not to individuals one
  by one — a new hire or role change then becomes a group membership change, not
  N separate permission edits.
- Decide the **Manager vs. can-edit vs. read-only** access level per collection
  deliberately: a shared streaming password rarely needs edit access for every
  member; a shared infrastructure credential often does need an audit trail of
  who changed it.

## 2. Roles and the admin bottleneck
- Bitwarden Organizations have **Owner**, **Admin**, **Manager**, **User** roles;
  1Password has **Owner**, **Administrator**, **Member**, plus per-vault roles.
  A plan with exactly one Owner and no second Admin has a single point of
  failure — if that person loses access or is unreachable, nobody can add,
  remove or recover anyone else.
- Set **at least two** people at Owner/Admin level on any plan that matters,
  even a household one (e.g. both partners), specifically so account
  administration itself doesn't depend on one person.

## 3. Offboarding — the step most plans get wrong
Removing someone from the organisation/family plan revokes their access to
shared collections, but does **not** retroactively change any password they
already saw while they had access, nor does it log them out of sessions already
open on their device using items they copied or memorised. On offboarding:
1. Remove the person from the organisation/plan (revokes ongoing shared access).
2. **Rotate every credential they had Manager/edit access to**, or at minimum
   every one in a collection sensitive enough to matter (shared infrastructure
   logins, financial accounts) — not just the ones you suspect they wrote down.
3. Check for any **personal items they created inside a shared collection**
   that should move to their personal vault or be deleted, since those don't
   automatically follow them out.
4. If they had their own master password/account under the family plan (not
   just added to collections), confirm the account itself is actually removed,
   not just unlinked from collections — an org member removed from all
   collections may still exist as an account on the plan with billing/seat
   implications and, depending on the product, residual access to anything
   they'd already synced locally before removal.

## 4. Break-glass: admin unreachable or incapacitated
- Bitwarden: configure **Account Recovery** (Enterprise/Teams org policy) so a
  designated admin can reset a member's master password without destroying
  their vault — this is different from Emergency Access between individuals and
  needs to be set up in advance per member, not improvised after the fact.
- 1Password Families: the account's **organiser(s)** can initiate recovery for a
  family member who's locked out; ensure at least one organiser's own recovery
  (their own account's Emergency Kit) isn't itself a single point of failure.
- Document, outside the vault itself, who the Owners/Admins are and how to reach
  them — the plan's own continuity shouldn't depend on information that's only
  stored inside the system it's meant to recover.

## Gotchas
- A flat "everyone sees everything" shared vault is the most common setup
  mistake — it works until an offboarding or a compromised member's device
  exposes the entire household's/team's credentials at once.
- Removing a person from the plan is not the same as rotating what they could
  see; skipping rotation is the actual security gap in most "we offboarded them"
  assumptions.
- Uncertain: exact feature names and availability (Account Recovery, organiser
  recovery specifics) differ by plan tier and change between releases — verify
  against the current plan tier before relying on a specific mechanism.

## Verify
- [ ] Collections/vaults split by real need-to-know, not one shared bucket.
- [ ] At least two people hold Owner/Admin-level access on any plan that matters.
- [ ] Offboarding checklist includes credential rotation, not just removal from
      the organisation.
- [ ] A break-glass/account-recovery mechanism is configured and documented
      before it's needed, not improvised during a lockout.
