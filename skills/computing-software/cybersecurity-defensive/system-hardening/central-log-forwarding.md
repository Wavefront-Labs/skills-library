---
id: computing-software.cybersecurity-defensive.system-hardening.central-log-forwarding
name: central-log-forwarding
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [audit-log-management, log-forwarding, rsyslog, windows-event-forwarding, tls-syslog, log-pipeline, siem-ingestion]
level: practitioner
status: draft
description: "Forward host logs centrally and reliably: rsyslog over TLS with disk-assisted queues, Windows Event Forwarding subscriptions, agent-based shipping and monitoring for silent sources."
sources: ["rsyslog documentation - Encrypting syslog traffic with TLS and queues", "Microsoft Learn - Use Windows Event Forwarding to help with intrusion detection", "NIST SP 800-92 Guide to Computer Security Log Management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Central log forwarding

**Goal:** security logs leave the host quickly, encrypted, without loss during outages, and missing sources are noticed.

## Linux: rsyslog over TLS
`/etc/rsyslog.d/90-forward.conf`:
```
global(DefaultNetstreamDriver="gtls" DefaultNetstreamDriverCAFile="/etc/pki/rsyslog/ca.pem")
action(type="omfwd" target="logs.corp.example" port="6514" protocol="tcp"
       StreamDriver="gtls" StreamDriverMode="1" StreamDriverAuthMode="x509/name"
       StreamDriverPermittedPeers="logs.corp.example"
       queue.type="LinkedList" queue.filename="fwdq" queue.maxDiskSpace="1g"
       queue.saveOnShutdown="on" action.resumeRetryCount="-1")
```
Disk-assisted queue keeps logs during collector outages. Include journald via `imjournal` and auditd via audisp syslog plugin or a dedicated agent.

## Windows: Windows Event Forwarding (WEF)
1. Collector: `wecutil qc`; create source-initiated subscription (XML) selecting events (e.g. Security 4624/4625/4672/4688/4720/4728/4732, PowerShell 4104, Sysmon).
2. GPO on sources: Computer Configuration > Administrative Templates > Windows Components > Event Forwarding > Configure target Subscription Manager = `Server=http://wec.corp.example:5985/wsman/SubscriptionManager/WEC,Refresh=60`.
3. Add `NETWORK SERVICE` to Event Log Readers (or grant channel access) so WinRM can read the Security log.
4. Forward from the collector to the SIEM with an agent (Splunk UF, AMA, Elastic Agent, Winlogbeat).
Kerberos-authenticated HTTP is encrypted by WinRM; use HTTPS for non-domain sources.

## Agents
Splunk UF, Elastic Agent, Azure Monitor Agent with DCRs, Fluent Bit, Vector - pick one per platform; manage config centrally.

## Reliability
- Monitor last-seen per source in the SIEM; alert when a critical source is silent beyond its expected interval (e.g. DC silent 15 min).
- Use TCP/RELP or agent acknowledgements, not UDP syslog, for security logs.
- Normalise time to UTC with timezone in records.

## Verify
- [ ] Test event (`logger -p auth.warning test-forward`; `eventcreate /T WARNING /ID 999 /L APPLICATION /D test`) reaches the SIEM within a minute.
- [ ] Silent-source alert fires when a test host's forwarder is stopped.
