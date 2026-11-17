---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.private-browsing-residue
name: private-browsing-residue
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [private-browsing, incognito, browser-forensics, memory-forensics, dns-cache, dfir]
level: advanced
status: draft
description: "Find residue of private and incognito browsing: memory, pagefile, DNS cache, session files, SRUM, and network logs, and what can and cannot be shown."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://volatility3.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private browsing residue

**Goal:** establish activity in Incognito/InPrivate/Private windows, which by design do not
write history to disk, by looking elsewhere.

## Where traces remain
| Source | What |
|---|---|
| RAM (live capture) | URLs, page content, form data in browser process memory; `strings`/YARA on dumped browser processes (Volatility `windows.memmap --dump --pid`) |
| pagefile.sys / hiberfil.sys | Fragments of URLs and content paged out |
| DNS client cache (live) | `ipconfig /displaydns` / `Get-DnsClientCache` domains resolved recently |
| Network logs | Proxy, DNS server, firewall logs: unaffected by private mode |
| SRUM | Per-application network bytes by hour (shows browser activity volume, not URLs) |
| Downloads | Files saved to disk remain, with Zone.Identifier `HostUrl`/`ReferrerUrl` |
| Firefox sessionstore | Private windows not persisted after close, but crash/recovery files may hold state while open |
| GPU/cache artefacts | Some versions leaked to disk caches or favicon DBs historically; version-dependent |
| Prefetch/BAM | Browser executed; Chrome command line `--incognito` visible in process events (4688/Sysmon) or jump list tasks |

## Approach
1. Capture memory early if private browsing is relevant and the browser may still be open.
2. Pull network-layer logs for the user's IP and time window.
3. Carve pagefile/unallocated for URL patterns (`bulk_extractor -e url`).
4. Check downloads folder and Zone.Identifier streams.

## Limits
Absence of history is expected and proves nothing; findings from memory/pagefile are
fragmentary and undated unless tied to process start times. State confidence carefully.

## Verify
Any URL claimed from residue is corroborated by a network log entry with timestamp and
source IP of the user's machine.
