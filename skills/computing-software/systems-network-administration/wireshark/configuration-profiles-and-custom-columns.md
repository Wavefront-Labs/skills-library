---
id: computing-software.systems-network-administration.wireshark.configuration-profiles-and-custom-columns
name: configuration-profiles-and-custom-columns
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wireshark-profiles, configuration-profile, custom-columns, coloring-rules, preferences, column-preferences, profile-switching, recent-file, troubleshooting-profile, field-occurrence]
level: practitioner
status: verified
description: "Build task-specific Wireshark profiles (TCP, DNS, VoIP, WLAN) with custom columns, coloring rules and filter buttons, share them across machines and auto-switch by display filter."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustConfigProfilesSection.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustPreferencesSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration profiles and custom columns

A profile is a folder holding preferences, columns, coloring rules, display filter buttons,
Decode As entries and recent settings. Switching profiles changes the whole analysis view.

## Create and switch
- Status bar bottom right: click the profile name for the profile menu, or Edit > Configuration Profiles
  (Shift+Ctrl+A).
- Copy from Default or from a global profile to start.
- Location: Help > About > Folders > "Personal configuration" (e.g. `~/.config/wireshark/profiles/<name>`
  on Linux, `%APPDATA%\Wireshark\profiles\<name>` on Windows). Zip the folder to share; import
  via Configuration Profiles > Import (zip or directory; profiles whose name already exists, and "Default", are skipped).
- Auto-switch: in the profile dialog set "Auto Switch Filter", e.g. `sip || rtp`. When you open a capture file
  Wireshark checks the first "Auto switch packet limit" packets and selects the first profile whose filter matches;
  a limit of 0 disables it, and picking a profile by hand disables it until the next file.

## Custom columns
Right-click any field in the packet details > **Apply as Column**. Edit via Preferences >
Appearance > Columns: type "Custom", field name, occurrence.
Useful sets:
| Profile | Columns |
|---|---|
| TCP | `tcp.stream`, `tcp.time_delta`, `tcp.analysis.bytes_in_flight`, `tcp.window_size`, `tcp.len`, `tcp.analysis.ack_rtt` |
| DNS | `dns.qry.name`, `dns.flags.rcode`, `dns.time`, `dns.a` |
| HTTP | `http.host`, `http.request.uri`, `http.response.code`, `http.time` |
| TLS | `tls.handshake.extensions_server_name`, `tls.handshake.type`, `tls.record.version` |
| WLAN | `wlan_radio.signal_dbm`, `wlan_radio.data_rate`, `wlan.fc.retry`, `wlan_radio.channel` |
- Fields with multiple occurrences (e.g. `ip.src` in ICMP errors, tunnels): set occurrence `1` or `-1` (last).
- A column can show an expression: `tcp.srcport or udp.srcport` as a custom column shows whichever exists
  (checked: `-o 'gui.column.format:"SP","%Cus:tcp.srcport or udp.srcport:0:R"'` printed ports for TCP and UDP rows).
- Right-click column header > Resize / Align / Hide; columns can be sorted numerically.

## Coloring rules and buttons per profile
- View > Coloring Rules: add rules at the top for the profile's focus, e.g. `tcp.analysis.flags
  && !tcp.analysis.window_update` black/red, `dns.flags.rcode != 0` orange.
- Filter buttons (the + on the filter toolbar) saved per profile: `tcp.analysis.retransmission`,
  `tcp.flags.reset==1`, `http.time > 1`.

## Gotchas
- Profiles copied from another Wireshark version may contain obsolete field names; the column
  shows empty. Check field names in View > Internals > Supported Protocols, or `tshark -G fields`.

## Verify
- [ ] Switching to the TCP profile shows the custom columns and coloring immediately.
- [ ] The zipped profile imports cleanly on a second machine.

## Checked
Profile contents, dialog buttons, import/export rules and auto-switch behaviour read from the 4.4.1 User's Guide
(Configuration Profiles section) shipped with the install; column field names (`tcp.stream`, `tcp.time_delta`,
`tcp.analysis.bytes_in_flight`, `tcp.window_size`, `tcp.len`, `tcp.analysis.ack_rtt`, `dns.*`, `http.*`, `tls.*`,
`wlan_radio.*`, `wlan.fc.retry`) confirmed in `tshark -G fields`; the `or` expression column and the `%Cus:` format ran.
The per-profile TCP/DNS layouts are suggestions, not tool behaviour. Removed an unsourced performance claim and the
3.6+ version gates, which the 3.6.0 release notes do not support.
