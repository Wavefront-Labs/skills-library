---
id: computing-software.systems-network-administration.active-directory.kerberos-armoring-fast-and-claims
name: kerberos-armoring-fast-and-claims
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, authentication-policies, kerberos-armoring, fast-armoring, claims, compound-authentication, kdc-support-for-claims, dynamic-access-control, kerberos, gpo]
level: advanced
status: gated
description: "Enable Kerberos armoring (FAST) and claims: KDC and client GPO settings, Supported vs Always provide claims vs Fail unarmored, and checking armored tickets."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/authentication-policies-and-authentication-policy-silos
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4768
  - https://www.rfc-editor.org/rfc/rfc6113
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kerberos armoring (FAST) and claims

**FAST** is Kerberos armoring, built on the pre-authentication framework in RFC 6113: the AS exchange is wrapped in the computer's TGT. An authentication policy that restricts where a user may sign in relies on armored requests so the domain controller can check the device's identity. Windows Server 2012 domain controllers and Windows 8 clients support armoring.

## Settings
DC side (GPO on the Domain Controllers OU): *Administrative Templates > System > KDC > KDC support for claims, compound authentication and Kerberos armoring* (gated: unconfirmed, source is paywalled or blocked), with the options Supported, Always provide claims and Fail unarmored authentication requests (gated: unconfirmed, source is paywalled or blocked).

Client side: *System > Kerberos > Kerberos client support for claims, compound authentication and Kerberos armoring* = Enabled (gated: unconfirmed, source is paywalled or blocked).

The exact policy names and option semantics could not be read in a Microsoft source; confirm them in the Group Policy settings reference before relying on them.

## Roll out
1. Enable the KDC and client armoring settings on all 2012+ DCs and Windows 8+ clients (gated: unconfirmed, source is paywalled or blocked).
2. Verify armored requests: on DCs, event 4768 reports the pre-authentication type; type 138 (PA-ENCRYPTED-CHALLENGE) is a logon using Kerberos armoring (FAST).
3. Only if required by policy, enforce armoring after an inventory of clients that cannot do it (for example Windows 7 and Windows Vista).

## Gotchas
- Computers that do not support armoring, such as Windows 7 and Windows Vista, fail sign-in when the user's authentication policy requires armored requests.

## Verify
- [ ] Security events 4768 on DCs show pre-auth type 138 for Windows clients.
- [ ] Silo/DAC conditions evaluate as expected (authentication policy audit logs).

## Checked
Checked 2026-10-27 against Microsoft Learn (authentication policies and silos overview; event 4768 reference) and RFC 6113.
- Confirmed: armored AS-REQ behaviour with authentication policies; Windows 8 and Windows Server 2012 as the first armoring-capable versions; event 4768 pre-authentication type 138 is PA-ENCRYPTED-CHALLENGE, a logon using Kerberos armoring; FAST is defined within RFC 6113.
- Gated: the KDC and client Group Policy names and their option semantics.
- Removed: the FAST name expansion, the large-ticket warning setting, Java GSS and compound-authentication remarks, none confirmed.

Method: documentation only; no commands were run.
