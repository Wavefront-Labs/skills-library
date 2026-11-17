---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-file-filter-profiles
name: fortigate-file-filter-profiles
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [file-filter, fortios, file-type-block, file-filter-profile, archive-block, password-protected]
level: practitioner
status: draft
description: "Block or log specific file types in FortiGate file filter profiles across HTTP, FTP, SMTP and other protocols."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: stop executables and risky archives crossing the firewall by file type, regardless of extension.

```
config file-filter profile
    edit "ff-std"
        set feature-set proxy
        config rules
            edit "block-exec"
                set protocol http ftp smtp
                set action block
                set direction any
                set file-type "exe" "msi"
            next
            edit "log-archives"
                set protocol http
                set action log-only
                set password-protected yes
                set file-type "zip" "rar"
            next
        end
    next
end
config firewall policy
    edit 10
        set file-filter-profile "ff-std"
    next
end
```
Detection is by file signature (magic bytes) and not only extension.

Gotchas
- HTTPS requires deep inspection to see file types.
- Rules evaluate in order; first match wins.
- `password-protected yes` matches only encrypted archives that FortiOS can recognise (confirm per format).
- A policy needs `utm-status enable` and the correct inspection mode; flow-mode support depends on protocol.

## Verify
```
show file-filter profile ff-std
```
Download a harmless sample file of the blocked type in a lab; the log subtype `file-filter` shows the action and file name.
