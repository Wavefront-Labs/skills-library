---
id: computing-software.systems-network-administration.windows-server.iscsi-chap-authentication
name: iscsi-chap-authentication
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iscsi, iscsi-chap, chap, mutual-chap, reverse-chap, iscsi-security, set-iscsiservertarget]
level: practitioner
status: docs-checked
description: "Secure iSCSI with one-way and mutual CHAP on Windows targets and initiators: secrets, Set-IscsiServerTarget, Connect-IscsiTarget and common auth failures."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/iscsitarget/set-iscsiservertarget
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/connect-iscsitarget
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/set-iscsichapsecret
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iSCSI CHAP authentication

CHAP proves the initiator to the target (one-way); mutual CHAP also proves the target to
the initiator. It does not encrypt traffic; keep iSCSI on an isolated network or add IPsec.

## Secret rules
- Use a different secret for each direction. The required secret length is not stated in the cmdlet references; check the initiator and target documentation or error text for the limits.

## Target side (iSCSI Target Server)
```powershell
$cred = New-Object PSCredential('sql01-chap', (ConvertTo-SecureString '<SECRET>' -AsPlainText -Force))
Set-IscsiServerTarget -TargetName SQL01 -EnableChap $true -Chap $cred
# mutual CHAP: target authenticates back to the initiator
$rev = New-Object PSCredential('san01-rchap', (ConvertTo-SecureString '<other secret>' -AsPlainText -Force))
Set-IscsiServerTarget -TargetName SQL01 -EnableReverseChap $true -ReverseChap $rev
```

## Initiator side
```powershell
# one-way
Connect-IscsiTarget -NodeAddress <iqn> -TargetPortalAddress 10.10.10.5 -AuthenticationType ONEWAYCHAP `
  -ChapUsername sql01-chap -ChapSecret '<secret>' -IsPersistent $true
# mutual: set the initiator's own secret first
Set-IscsiChapSecret -ChapSecret '<other secret>'
Connect-IscsiTarget -NodeAddress <iqn> -TargetPortalAddress 10.10.10.5 -AuthenticationType MUTUALCHAP `
  -ChapUsername sql01-chap -ChapSecret '<secret>' -IsPersistent $true
```
`-AuthenticationType` must be uppercase (NONE, ONEWAYCHAP or MUTUALCHAP). `Set-IscsiChapSecret` sets the initiator's own CHAP secret for mutual CHAP.

## Failures
- Authentication failure at login: secret mismatch or wrong username on either side.
- After rotating a secret, remove the persistent login (`Unregister-IscsiSession`) and connect again with `-IsPersistent $true`.

## Verify
- [ ] `Get-IscsiServerTarget SQL01 | Format-List *` shows CHAP and reverse CHAP enabled.
- [ ] `Get-IscsiSession | Format-List AuthenticationType,IsConnected,IsPersistent`.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Set-IscsiServerTarget: -EnableChap, -Chap (PSCredential), -EnableReverseChap, -ReverseChap; Connect-IscsiTarget: -AuthenticationType NONE|ONEWAYCHAP|MUTUALCHAP (uppercase required), -ChapUsername, -ChapSecret, -IsPersistent; Set-IscsiChapSecret sets the initiator's CHAP secret.
- Removed unconfirmed details: the 12 to 16 character secret rule, the 0xEFFF0009 error code, case sensitivity of usernames and the array-specific reverse-username remark.

Method: documentation only; no commands were run.
