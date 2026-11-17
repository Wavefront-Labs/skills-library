---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-antivirus-profiles
name: fortigate-antivirus-profiles
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [antivirus-profile, fortios, av-scan, flow-mode, proxy-mode, sandbox, content-disarm]
level: practitioner
status: draft
description: "Configure FortiGate antivirus profiles with scan mode, protocols, block actions, and sandbox or CDR options."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: block known malware per protocol and handle unknown files.

```
config antivirus profile
    edit "av-std"
        set feature-set proxy
        config http
            set av-scan block
        end
        config smtp
            set av-scan block
        end
        config ftp
            set av-scan block
        end
        set mobile-malware-db enable
    next
end
```
`feature-set flow` uses the flow-based engine (faster, fewer features); `proxy` buffers files for full scanning and supports CDR, grayware and more. Add FortiSandbox integration (`config antivirus profile` -> `set analytics-db enable` or the sandbox settings) for unknown files (confirm option names per release).

Use inside a policy by `set av-profile "av-std"`. For HTTPS, the policy must also use a deep-inspection SSL profile.

Gotchas
- Oversize files bypass scanning by default (`config firewall profile-protocol-options` oversize limit); decide whether to block oversize.
- Archives with passwords cannot be scanned: set `archive-block encrypted` in the protocol options.
- Policy mode mismatch: a flow-mode policy cannot use proxy-only options.

## Verify
```
diagnose antivirus database
execute update-now
```
Download the harmless EICAR test file from an approved vendor test page in a lab; the AV log and a replacement block page confirm detection.
