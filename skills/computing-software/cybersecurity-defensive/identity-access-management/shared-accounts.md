---
id: computing-software.cybersecurity-defensive.identity-access-management.shared-accounts
name: shared-accounts
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [shared-accounts, generic-accounts, service-accounts, password-vaulting, accountability, check-out-check-in, identity-lifecycle]
level: practitioner
status: draft
description: "Control shared and generic accounts: eliminate where possible, vault with check-out and rotation, tie use to named individuals, restrict interactive logon and monitor."
sources: ["https://www.cisecurity.org/controls/v8", "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/implementing-least-privilege-administrative-models"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared and generic accounts

Shared accounts (kiosk, "admin", "support", vendor logins, root) break accountability and survive
staff departures because nobody changes the password.

## Approach
1. **Inventory:** accounts with no owner, generic names, used from multiple hosts/users (login source diversity in IdP/AD logs), local admin/root.
2. **Eliminate:** replace with named accounts plus delegation (sudo, RBAC, group-based admin) wherever the system supports it.
3. **Unavoidable ones** (root, built-in Administrator, appliance admin, SaaS owner account, break-glass):
   - Store in a PAM vault; check-out with named user, reason/ticket, optional approval.
   - Automatic rotation after each check-in (or daily).
   - Session recording via the PAM proxy where feasible.
4. **Kiosk/shared devices:** use shared device modes (Windows shared PC / assigned access, iOS shared iPad, Android dedicated) with per-user sign-in or locked single-app mode, not a shared credential.
5. **Restrict:** deny interactive/network logon for generic accounts where not needed (GPO user rights), restrict source hosts.
6. **Monitor:** alert on use outside check-out windows (vault vs. logon events correlation).

## Gotchas
- Built-in Administrator (RID 500) bypasses lockout; rename is cosmetic; use LAPS for rotation.
- Shared mailboxes do not need a sign-in: block sign-in for their user objects.
- Break-glass accounts are shared by design: two accounts, FIDO2 keys in a safe, alert on any sign-in.

## Verify
- [ ] Every remaining shared account has an owner and is vaulted.
- [ ] Logons without matching vault check-out generate alerts.
