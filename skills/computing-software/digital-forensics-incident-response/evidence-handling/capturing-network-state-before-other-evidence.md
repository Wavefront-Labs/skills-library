---
id: computing-software.digital-forensics-incident-response.evidence-handling.capturing-network-state-before-other-evidence
name: capturing-network-state-before-other-evidence
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [network-state-capture, order-of-volatility, volatile-data, live-response, dfir]
level: practitioner
status: docs-checked
description: "Capture live network state early: where RFC 3227 puts routing and ARP data in the order of volatility, and Get-NetTCPConnection for Windows connections."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-nettcpconnection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing network state before other evidence

**Goal:** network state changes in seconds, so capture it before slower evidence work disturbs the host.

## Order of volatility
RFC 3227 section 2.1 says to proceed from the volatile to the less volatile and gives this example order for a typical system:
1. registers, cache
2. routing table, ARP cache, process table, kernel statistics, memory
3. temporary file systems
4. disk
5. remote logging and monitoring data relevant to the system
6. physical configuration, network topology
7. archival media

So routing table and ARP cache sit in the same tier as the process table and memory; capture them alongside memory, ahead of disk.

## Windows connections
`Get-NetTCPConnection` gets current TCP connections and their properties: local and remote address and port, state, owning process. Its parameters include `-State`, `-OwningProcess` and `-CreationTime`, so you can filter on those. Example from the page: `Get-NetTCPConnection -State Established`.
```powershell
Get-NetTCPConnection | Export-Csv tcp.csv -NoTypeInformation
```
Run from trusted binaries and write output to external storage, not the suspect disk.

## Other operating systems and tools
Use the platform's documented equivalents (for example the manual pages of `ss`, `ip`, `netstat`, `arp` and `route` on your system) and record exactly which commands you ran.

## Practice
- Hash each output file; note the collection time (UTC) and the command in the collection log.
- Live output records state at a known time even if a later memory acquisition fails.

## Verify
Every listed remote address can be mapped to an owning process where the tool provides one, and the outputs are hashed and logged.

## Checked
Confirmed against RFC 3227 section 2.1 (order of volatility list) and the Get-NetTCPConnection page (description, parameter names, `-State Established` example). Removed unconfirmed content: the cmd, Linux and macOS command lists, `CreationTime` meaning, `netstat -b` notes, Velociraptor artifact name, memory `netscan`, rootkit claims, and the NIST SP 800-86 source (no claims relied on it). Corrected the original claim that connections should precede memory: RFC 3227 lists memory in the same tier.

Method: docs-only read of cited pages, 2026-11-09
