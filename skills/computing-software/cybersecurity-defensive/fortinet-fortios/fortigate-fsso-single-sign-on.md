---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-fsso-single-sign-on
name: fortigate-fsso-single-sign-on
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fsso, fortios, fortinet-single-sign-on, collector-agent, polling-mode, ad-groups, fsso-user-list]
level: practitioner
status: draft
description: "Set up FSSO so FortiGate learns logged-on AD users from a Collector Agent and applies group policy."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: transparent user-based policy without prompting.

On the FortiGate:
```
config user fsso
    edit "ad-collector"
        set server "192.0.2.30"
        set password <COLLECTOR-PASSWORD>
        set ldap-server "AD-CORP"
        set port 8000
    next
end
config user group
    edit "FSSO-ENG"
        set group-type fsso-service
        set member "ad-collector"
    next
end
```
Install the FSSO Collector Agent on a Windows server (or use the polling mode and the agentless FSSO, depending on release). It reads domain controller security events and sends logon info to the FortiGate. In the collector, select the AD groups to send (these appear in the FortiGate FSSO group list as `ad-collector\Domain Users` style names).

Gotchas
- The collector password must match, and TCP 8000 must be open.
- Stale logon entries: shorten `workstation check` intervals or enable the DC agent mode.
- NAT between users and the FortiGate breaks IP-based mapping.
- Terminal servers need the TS agent.

## Verify
```
diagnose debug authd fsso list
diagnose debug authd fsso server-status
```
The list shows logged-on users with IP and groups; the server status shows `connected`.
