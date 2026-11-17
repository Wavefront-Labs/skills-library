---
id: computing-software.systems-network-administration.wireshark.saved-capture-filters-cfilters
name: saved-capture-filters-cfilters
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, capture-filters, cfilters, dfilters, configuration-profiles]
level: practitioner
status: verified
description: "Manage Wireshark saved capture filters: the Capture Filters dialog, the cfilters file format, sharing per profile, and the filter bookmark button."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkDefineFilterSection.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAppFilesConfigurationSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saved capture filters (cfilters)

Wireshark stores named capture filters so analysts do not retype BPF under pressure.

## GUI
- Capture > Capture Filters... adds, edits, deletes named filters.
- The bookmark icon next to the filter box opens the saved list; "Manage Capture Filters" there, or Capture >
  Capture Filters..., edits it.
- Display filters live separately (Analyze > Display Filters, file `dfilters`); display filter
  buttons (`dfilter_buttons`) are another file.

## File format
Personal configuration folder (Help > About > Folders shows the path), file `cfilters`, one per line:
```
"Ethernet address 00:00:5e:00:53:00" ether host 00:00:5e:00:53:00
"No ARP and no DNS" not arp and port not 53
"Not my SSH session" not (tcp port 22 and host 192.0.2.10)
"VoIP SIP+RTP" udp port 5060 or udp portrange 10000-20000
```
Name in double quotes, then the filter (format as in the Wireshark User's Guide, "Files and Folders"). Each
configuration profile has its own `cfilters`; if the personal folder lacks one, the one in the global
configuration folder is read. Saving in the Capture Filters dialog rewrites the personal file.

## Sharing across a team
- Put a curated `cfilters` in a team profile directory and distribute the profile as a zip
  (Configuration Profiles > Import from zip).
- Global defaults for all users live in the Wireshark install data directory; edit there only on
  managed builds since upgrades overwrite it.

## Gotchas
- Validate each filter before saving with `dumpcap -i <iface> -f "<filter>" -d` (an invalid one is reported as
  "isn't a valid capture filter"; the example filters above all compile).
- In scripts pass filters to dumpcap/tshark with `-f`.

## Verify
- [ ] Restart Wireshark, switch to the profile and confirm the saved filters appear in the bookmark list.
