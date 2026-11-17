---
id: computing-software.systems-network-administration.wireshark.custom-coloring-rules
name: custom-coloring-rules
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, custom-coloring-rules, coloring-rules, colorfilters, profiles, conversation-colors]
level: practitioner
status: verified
description: "Write coloring rules that surface problems at a glance: rule order, filter-based rules for errors and slow responses, temporary conversation colors, and sharing colorfilters."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustColorizationSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom coloring rules

## How rules work
View > Coloring Rules. Rules are display filters evaluated top to bottom; the first match wins and colors
the packet. Put specific rules above general ones (a `tcp` rule above your `tcp.analysis.flags`
rule hides it).

## Useful additions (put at the top)
| Name | Filter | Suggested color |
|---|---|---|
| TCP problems | `tcp.analysis.flags && !tcp.analysis.window_update && !tcp.analysis.keep_alive` | black on red |
| Resets | `tcp.flags.reset == 1` | red on yellow |
| Slow DNS | `dns.time > 0.3` | orange |
| DNS errors | `dns.flags.rcode != 0` | dark orange |
| HTTP errors | `http.response.code >= 400` | magenta |
| Slow HTTP | `http.time > 1` | orange |
| TLS alerts | `tls.alert_message` | red |
| Big delta | `frame.time_delta > 1` | purple (`frame.time_delta_displayed > 1` matched nothing in TShark 4.4.1) |
| My host | `ip.addr == 10.0.0.5` | light blue background |

The built-in "Bad TCP" rule is similar; disable it rather than duplicating.

## Temporary conversation colors
Select a packet, then View > Colorize Conversation > Color 1-10, or press Ctrl with a number key. Wireshark builds
a conversation filter from TCP first, then UDP, IP and Ethernet. Temporary rules last until you quit; View >
Colorize Conversation > Reset coloring clears them. View > Colorize Packet List toggles all coloring.

## Share
Rules are stored in the profile's `colorfilters` file (plain text, one rule per line,
`@name@filter@[bg r,g,b][fg r,g,b]` with 16-bit values 0-65535, background first, e.g.
`@tcp@tcp@[59345,58980,65534][0,0,0]`). Export/Import buttons in the dialog, or copy the file into
teammates' profiles. A personal `colorfilters` file replaces the global one; they are not merged. Keep a
team profile in git.

## Gotchas
- Coloring is evaluated per packet; complex rules on big captures slow scrolling.
- Colors alone fail for color-blind analysts; also add a filter button for the same condition.
- Rules referencing fields from disabled protocols silently never match.

## Verify
- [ ] Open a known-bad capture: retransmissions, resets and slow responses stand out without
  filtering.

## Checked
Every filter in the table was compiled and run with TShark 4.4.1 against a synthetic capture; all are valid, and the
`frame.time_delta > 1` variant matched 17 packets with 60 s gaps while `frame.time_delta_displayed > 1` matched 0
(this is TShark's evaluation; the GUI uses the same filter engine). `colorfilters` line format, ordering ("first match wins"), temporary-rule keys and the
global/personal rule from the 4.4.1 User's Guide and the `wireshark`/`tshark` manual pages shipped with the install,
where the example line is `@tcp@tcp@[59345,58980,65534][0,0,0]`.
