---
id: computing-software.cybersecurity-defensive.identity-access-management.orphaned-and-dormant-accounts
name: orphaned-and-dormant-accounts
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [identity-lifecycle, orphaned-accounts, dormant-accounts, stale-accounts, inactive-accounts, account-reconciliation, lastlogontimestamp, entra-inactive-users]
level: practitioner
status: draft
description: "Find and clean up orphaned and dormant accounts across AD, Entra ID and SaaS: queries, reconciliation with HR, safe disablement and exceptions."
sources: ["CIS Control 5.3 (disable dormant accounts after 45 days)", "NIST SP 800-53 AC-2(3)", "Microsoft Learn - Manage inactive user accounts in Microsoft Entra ID"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Orphaned and dormant accounts

**Goal:** no enabled account exists without an owner and a recent need, because forgotten
accounts are a favourite attacker foothold.

## Definitions
- **Orphaned**: no matching active person or owner (leaver missed, test account, vendor gone).
- **Dormant**: owner exists but no sign-in for N days (CIS suggests 45 days).

## Find them
Active Directory (lastLogonTimestamp replicates with up to ~14 days lag, fine for 45-90 days):
```powershell
Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly |
  Where-Object Enabled | Select Name,SamAccountName,LastLogonDate
Get-ADUser -Filter {Enabled -eq $true -and PasswordNeverExpires -eq $true} -Properties PasswordLastSet
```
Entra ID (Graph, `signInActivity` needs P1):
```
GET https://graph.microsoft.com/v1.0/users?$filter=signInActivity/lastSignInDateTime le 2026-07-18T00:00:00Z&$select=displayName,userPrincipalName,signInActivity
```
Check `lastSuccessfulSignInDateTime` and non-interactive sign-ins before deciding.
SaaS: export users with last-login from each admin console or via SSPM tools.

## Reconcile with HR
Match accounts to HR employee IDs/contractor records. Unmatched accounts are orphan candidates;
match service accounts to an owner register.

## Clean up safely
1. Notify owner/manager (for dormant) with a deadline.
2. **Disable** first (and move to a quarantine OU / tag), remove from privileged groups.
3. Delete after 30-90 days if nobody complains.
4. Exceptions (seasonal workers, break-glass, rarely used service accounts) documented with owner and review date.

## Gotchas
- Service accounts show no interactive sign-in but are used: check non-interactive/service principal sign-ins and Kerberos events before disabling.
- Break-glass accounts are dormant by design: exclude, but monitor any use.
- Disabled accounts still members of groups can be re-enabled by anyone with rights: remove privileged memberships.

## Verify
- [ ] Monthly report: enabled accounts with no sign-in in 90 days trending to zero (minus documented exceptions).
- [ ] Every enabled account maps to a person or registered owner.
