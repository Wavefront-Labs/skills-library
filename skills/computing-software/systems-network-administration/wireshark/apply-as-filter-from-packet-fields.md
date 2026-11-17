---
id: computing-software.systems-network-administration.wireshark.apply-as-filter-from-packet-fields
name: apply-as-filter-from-packet-fields
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, apply-as-filter, prepare-as-filter, conversation-filter, display-filter, colorize-conversation]
level: practitioner
status: verified
description: "Build display filters from packet details: Apply/Prepare as Filter with Selected, And, Or and Not, conversation filters, and copying filters for tshark."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkDefineFilterSection.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apply as Filter from packet fields

Typing field names from memory is slow and error prone. Let Wireshark write them.

## From the packet details pane
Right-click any field (e.g. `Server Name Indication: api.example.com`) ->
- **Apply as Filter > Selected**: replaces the filter, applies now.
- **Prepare as Filter > Selected**: puts it in the bar without applying; edit first.
- **...and Selected / or Selected / and not Selected**: combines with the current filter.
  "and not Selected" repeatedly is the fastest way to peel away noise (multicast, ARP, a
  chatty host) until the problem traffic is left.

The status bar shows the selected field's name in parentheses (e.g. `tls.handshake.extensions_server_name`):
that is the name to use in tshark `-Y` and `-e`. Check any name with `tshark -G fields` (tab-separated, field
abbreviation in column 3).

## From the packet list
- Right-click a packet > **Conversation Filter > TCP/UDP/IP/Ethernet**: everything between
  the two endpoints.
- **Follow > TCP Stream** sets a display filter that selects the stream (`tcp.stream eq N`; the same
  expression works in tshark, where the first stream is 0). Closing the dialog with **Back** resets the filter.
- **Colorize Conversation** (View menu or the packet-list menu) marks it without filtering. Wireshark tries a
  TCP conversation filter first, then UDP, IP and Ethernet.

## Copy for other tools
Right-click field > Copy > **As Filter** gives the exact expression to paste into tshark,
a filter button or documentation.

## Filter buttons
Click "+" on the filter toolbar (or right-click in the button area, or use Preferences > Filter Buttons) to
save a frequently used filter as a button; buttons live in the profile's `dfilter_buttons` file. Group buttons
in a drop-down by putting `//` in the label.

## Verify
- [ ] The prepared filter matches the intended packets (status bar count) and is reusable in tshark `-Y`.

## Checked
Menu names and behaviour were read from the Wireshark 4.4.1 User's Guide shipped with the install (Analyze menu,
packet-details pop-up, Follow Stream, Filter Toolbar, Coloring, status bar sections). Run: `tcp.stream eq 1` selected
the 9 packets of one connection in a synthetic pcap; `tshark -G fields` column layout confirmed. Menu behaviour comes from the guide text.
