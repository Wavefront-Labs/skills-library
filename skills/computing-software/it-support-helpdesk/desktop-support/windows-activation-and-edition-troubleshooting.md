---
id: computing-software.it-support-helpdesk.desktop-support.windows-activation-and-edition-troubleshooting
name: windows-activation-and-edition-troubleshooting
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-activation, slmgr, kms, mak, digital-licence, subscription-activation, edition-upgrade, oa3, windows-editions, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Diagnose 'Windows isn't activated' and wrong-edition problems: slmgr /dlv, KMS vs MAK vs digital licence vs Enterprise subscription activation, and edition upgrade keys."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/get-started/activation-slmgr-vbs-options"
  - "https://learn.microsoft.com/en-us/windows-server/get-started/kms-client-activation-keys"
  - "https://learn.microsoft.com/en-us/windows/deployment/windows-subscription-activation"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/licensing-and-activation/troubleshoot-activation-error-codes"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# windows-activation-and-edition-troubleshooting

Goal: know which activation channel a PC is using, why it fails, and how to
get it onto the right edition without reinstalling.

## First look
```cmd
slmgr /dlv          :: detailed licence information for the installed OS
slmgr /xpr          :: activation expiry
slmgr /dlv all      :: every installed product, with activation IDs
```
`slmgr /dlv <Activation ID>` and `/xpr <Activation ID>` target one edition.
`slmgr.vbs` is not intended to manage older systems from a newer one.

## By channel
- **KMS** (client has a generic volume licence key, GVLK): needs to reach the
  KMS host, TCP port 1688 by default. `slmgr /skms <name>[:port]` points the
  client at a host, `slmgr /ato` retries activation (with a GVLK it makes a
  KMS attempt). The client renewal interval defaults to 7 days.
  - `0xC004F074`: no KMS could be contacted. Troubleshoot the network path
    and make sure nothing blocks TCP 1688.
  - `0xC004F038`: the KMS count is insufficient. A KMS host needs a count of
    at least 25 for Windows clients (5 for Windows Server).
- **MAK**: `slmgr /ipk <MAK>` then `slmgr /ato`. `0xC004C003` means the
  activation server determined the key is blocked.
- **Active Directory-based activation**: `slmgr` has its own AD activation
  options; see the slmgr reference.
- **Windows Enterprise subscription activation** (Enterprise E3 or E5): a
  device with a Windows Pro licence steps up to Enterprise when a user with
  the subscription signs in. Devices must run a supported Pro or Enterprise
  edition, be Microsoft Entra joined or hybrid joined (workgroup or
  Entra-registered devices are not supported), and renew about every 30 days
  over the internet. If a device stays offline until its subscription
  expires it reverts to Pro; it renews once reconnected.

## Gotchas
- `slmgr /rearm` resets activation timers and is also called by
  `sysprep /generalize`; it is not a fix for activation errors.
- For other error codes use Microsoft's activation error-code article.

## Verify
`slmgr /xpr` and `slmgr /dlv` show the expected activation state; Settings,
System, Activation shows the expected edition.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn slmgr options, KMS client activation keys, activation error-code and Windows subscription activation pages, as published October 2026. Confirmed: /dlv, /xpr, /ato, /ipk, /skms and /rearm behaviour, KMS port 1688, default 7-day renewal, error codes 0xC004F074, 0xC004F038 (count of 25 for clients, 5 for server) and 0xC004C003 (key blocked), subscription activation requirements, 30-day renewal and revert-to-Pro behaviour. Removed: KMS 180-day expiry, SRV record lookup, firmware key query via wmic, OEM/digital licence and hardware-change steps, changepk and Home-to-Pro paths, downgrade statement, VDI CMID note, dsregcmd advice, 'key exhausted' wording.

Method: documentation only; no commands were run.
