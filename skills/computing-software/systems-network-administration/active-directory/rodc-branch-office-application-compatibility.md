---
id: computing-software.systems-network-administration.active-directory.rodc-branch-office-application-compatibility
name: rodc-branch-office-application-compatibility
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, rodc-branch-office, rodc-app-compatibility, writable-dc, ldap-referrals]
level: advanced
status: gated
description: "Check whether branch applications work with an RODC: write operations that need a writable DC, LDAP referrals, and how to test before deploying."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/rodc/install-a-windows-server-2012-active-directory-read-only-domain-controller--rodc---level-200-
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RODC application compatibility in branch offices

Apps written assuming every DC is writable can fail or slow down at an RODC site. Test them before you ship the
RODC.

## What an RODC does with writes
- **LDAP writes**: the RODC returns a referral to a writable DC, so apps that do not follow referrals fail (gated: unconfirmed, source is paywalled or blocked).
- **Password changes and logon attribute updates**: forwarded to a writable DC (gated: unconfirmed, source is paywalled or blocked).
- **DNS dynamic updates**: client gets a referral (see rodc-dns-and-update-referrals).
- **Accounts not cached on the RODC**: accounts that are not allowed to cache passwords and cannot reach a writable DC cannot access resources or functionality provided by Active Directory.

## Apps that commonly break
- Apps that bind to "the local DC" and write user attributes (provisioning tools, older HR connectors).
- Apps that locate a DC without requesting a writable one and then write.

## Test method
1. Build the RODC in a lab site. Put the app server in that site only (subnet mapping).
2. Run the app's full workflow and capture its LDAP traffic to see referrals.
3. Check that write targets resolve to a writable DC (the DC locator can be asked for a writable DC).
4. Unplug the WAN link and repeat: logons of cached accounts must work; anything else is documented as
   WAN-dependent.

## Fixes
- Configure the app to use a writable DC explicitly.
- Add the app's service account to the Allowed RODC Password Replication Group (the Install an RODC article describes the Allowed and Denied RODC Password Replication Groups).
- If the app must write locally, the branch needs a writable DC; RODC is the wrong choice.

## Verify
- [ ] Every branch app's workflow is tested with WAN up and down and the results are written down.

## Checked
Checked 2026-10-27 against Microsoft Learn (Install an RODC, Windows Server 2012 article).
- Confirmed: accounts that cannot cache passwords on the RODC and cannot reach a writable DC cannot use AD resources; Allowed and Denied RODC Password Replication Groups.
- Gated: referral and forwarding behaviour for writes, passwords and logon attributes. Reason: only previous-versions RODC pages cover them and they could not be read.
- Removed: the ERROR_DS_REFERRAL name, Exchange guidance, event logging level, DsGetDcName flag and nltest syntax, none confirmed.

Method: documentation only; no commands were run.
