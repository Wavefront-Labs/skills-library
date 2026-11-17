---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.wireshark-investigation-profiles-and-columns
name: wireshark-investigation-profiles-and-columns
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [wireshark-profiles, wireshark, custom-columns, coloring-rules, time-display, filter-buttons, dfir, wireshark-coloring-rules, time-display-format]
level: practitioner
status: draft
description: "Build Wireshark configuration profiles for DFIR: UTC time, custom columns for host, SNI and DNS, colouring rules and filter buttons, and share them across the team."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChCustConfigProfilesSection.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChCustPreferencesSection.html", "https://unit42.paloaltonetworks.com/unit42-customizing-wireshark-changing-column-display/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Investigation profiles, columns and colouring

**Goal:** a repeatable Wireshark setup that surfaces the fields investigators need without
clicking into every packet, and a consistent time base for reports.

## Create a profile
Edit > Configuration Profiles > New (`DFIR`). Profiles live in the personal config
directory (Help > About > Folders: `profiles/DFIR/`), so they can be zipped and shared or
imported (Configuration Profiles > Import).

## Time
View > Time Display Format > **UTC Date and Time of Day** (`Ctrl+Alt+7`), seconds precision
as needed. Reports in UTC avoid analyst time-zone confusion.

## Columns (Preferences > Appearance > Columns, or right-click a field > Apply as Column)
| Title | Field |
|---|---|
| Src port / Dst port | `tcp.srcport or udp.srcport` / `tcp.dstport or udp.dstport` |
| Host | `http.host` |
| SNI | `tls.handshake.extensions_server_name` |
| DNS query | `dns.qry.name` |
| DNS answer | `dns.a` |
| User-Agent | `http.user_agent` |
| Stream | `tcp.stream` |
| Delta time displayed | `frame.time_delta_displayed` (beacon intervals) |
Hide noisy defaults (No., Length) and enable name resolution only deliberately: resolving
causes DNS lookups to attacker infrastructure from your analysis box (View > Name Resolution,
keep network name resolution off).

## Filter buttons
Click the `+` at the right of the filter bar: e.g. `web` = `(http.request or tls.handshake.type == 1) and !(ssdp)`,
`dns` = `dns.flags.response == 0`, `smb` = `smb2.cmd == 5`, `kerb` = `kerberos`,
`notlocal` = `!(ip.dst == 10.0.0.0/8 or ip.dst == 172.16.0.0/12 or ip.dst == 192.168.0.0/16)`.

## Colouring rules
View > Coloring Rules: put specific rules first, e.g. red for `tcp.flags.reset == 1`, orange
for `http.request.method == "POST"`, purple for `dns.qry.name.len > 50`, yellow for
`kerberos.msg_type == 13 and kerberos.etype == 23` (RC4 TGS: Kerberoasting).

## Disable things that mislead
- Preferences > Protocols > TCP: keep "Allow subdissector to reassemble TCP streams" on, but
  disable "Validate checksum" if offload is present.
- Turn off "Check for updates" and online name resolution on air-gapped analysis machines.

## Self-check
A colleague importing your profile sees the same UTC times, columns and filter buttons and
can reproduce your screenshots.
