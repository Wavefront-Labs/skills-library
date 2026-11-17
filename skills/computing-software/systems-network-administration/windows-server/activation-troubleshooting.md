---
id: computing-software.systems-network-administration.windows-server.activation-troubleshooting
name: activation-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-activation, activation-errors, 0xc004f074, 0xc004f038, 0xc004c003, 0x8007232b, slmgr, sppsvc, kms, troubleshooting]
level: practitioner
status: docs-checked
description: "Fix Windows Server activation failures by error code: 0xC004F074 no KMS, 0x8007232B DNS, 0xC004F038 count, 0xC004C003 blocked key, plus slmgr diagnostics."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-error-codes
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-slmgr-vbs-options
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-troubleshoot-kms-general
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Activation troubleshooting

## Gather facts
```cmd
slmgr /dlv          detailed license information (add the Activation ID or `all` for other editions)
slmgr /dli          license information, and the KMS count on a KMS host
slmgr /xpr          expiry (meaningful for KMS clients; MAK and retail activation is perpetual)
nslookup -type=srv _vlmcs._tcp.<domain>
Test-NetConnection kms01 -Port 1688
```
Event log: Application log, event ID 12288 records each KMS activation attempt; Microsoft's 0xC004F074 guidance is
to troubleshoot each 12288 error. `slui.exe 0x2a <code>` displays the text for an error code.

## Codes
| Code | Meaning | Fix |
|---|---|---|
| **0xC004F074** | No KMS could be contacted (all hosts tried returned errors) | work through each Application event 12288; check DNS SRV, TCP 1688, host up; `slmgr /skms host:1688` to test directly |
| **0x8007232B** | DNS name does not exist | KMS client cannot find SRV records: make sure a KMS host is installed with DNS publishing on, or point the client with `slmgr /skms <host>`, or use a MAK |
| **0xC004F038** | KMS count insufficient | Server needs a count of 5 or more, client 25 or more; add machines to the pool; `slmgr /dli` on the host |
| **0xC004F06C** | request timestamp invalid | client clock too different from the KMS host (UTC time, time zone irrelevant); sync with NTP or AD |
| **0xC004C003** | product key blocked on the activation server | contact the Microsoft Licensing Activation Centers for a new MAK |
| **0xC004F050** | product key invalid | typo, beta key on a GA build, or hyphens pasted as em-dashes; install the correct key for the version |
| **0xC004F039** | KMS not enabled | no response to the KMS request; check the network and that TCP 1688 is not filtered |
| **0xC004F041** | KMS host not activated | activate the KMS host online or by phone |
| **0xC004C020** | MAK activation limit exceeded | request more activations |
| **0x80070005** | access denied | run elevated |

## Reset when stuck
```cmd
net stop sppsvc & net start sppsvc
slmgr /upk & slmgr /cpky   uninstall key and clear from registry, then reinstall correct key
```

## Verify
- [ ] `slmgr /dlv` shows License Status: Licensed.
- [ ] No new Application 12288 errors after the next renewal attempt.

## Checked

2026-10-27. Documentation release: Microsoft Learn activation error codes page (last updated 2026-02-12) and slmgr options page. Confirmed the meaning, cause and fix for each code listed, event ID 12288, /skms, /dli, /xpr and slui.exe 0x2a. Removed 0xC004F069, 0xC004F06B and 0xC004E016 (not on the page), the 4-hour skew figure, event IDs 12289 and 8198, the channel strings and the rearm advice because no fetched page covers them. The earlier source URL was replaced with the current page.

Method: documentation only; no commands were run.
