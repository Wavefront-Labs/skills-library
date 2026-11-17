---
id: computing-software.systems-network-administration.wireshark.export-pdus-to-file
name: export-pdus-to-file
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, export-pdus, exported-pdu, tshark-export, reassembly]
level: practitioner
status: verified
description: "Use Wireshark Export PDUs to write reassembled or tunnel-inner PDUs (OSI layer 3, 7, DLT) to a new capture for focused analysis or sharing."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Export PDUs to file

Export PDUs writes PDUs from a chosen tap into a new capture. The `OSI layer 3/4/7`, `DLT User`, `DVB-CI` and `Logcat` taps use the
"Wireshark Upper PDU export" encapsulation (LINKTYPE_WIRESHARK_UPPER_PDU, DLT 252 per tcpdump.org/linktypes.html), where each record carries
tags such as the protocol name; the `IP` and `Ethernet` taps write plain Raw IP and Ethernet records. `tshark -U ""` lists the taps on 4.4.1:
`DLT User`, `DVB-CI`, `Ethernet`, `IP`, `Logcat`, `Logcat Text`, `OSI layer 3`, `OSI layer 4`, `OSI layer 7`.

## Typical uses
- Strip tunnels: the `IP` tap writes every IP layer as its own Raw IP record. On a 2-packet capture (one VXLAN packet and one ICMP error
  with an embedded IP header) `tshark -U "IP"` wrote 3 records, the third being the inner `10.20.0.5 -> 10.20.0.6` packet, and the
  `Ethernet` tap wrote the inner Ethernet frame. Outer headers stay inside the first record of each packet.
- The `OSI layer 3/4/7` taps only receive PDUs from dissectors that feed them (for example after decryption); on plain captures they
  wrote 0 records (`OSI layer 7` on an unencrypted HTTP capture, `OSI layer 3` on a VXLAN capture), so test on your own file first.

## tshark
```
tshark -r vxlan.pcapng -U "IP" -w inner.pcapng            # Raw IP records, outer and inner layers
tshark -r vxlan.pcapng -U "Ethernet" -w inner-eth.pcapng
tshark -r cap.pcapng -Y <filter> -U "OSI layer 7" -w l7.pcapng   # only if the dissector exports PDUs (see above)
tshark -r cap.pcapng -U ""        # list taps (-U needs -r)
```
The man page: `-U` exports PDUs according to the tap name, and `-Y` filters. Quote the tap name; an unquoted `?` is a shell glob.
Without `-r`, tshark says `PDUs export requires a capture file (specify with -r)`.

## Gotchas
- Many non-Wireshark tools do not understand DLT 252; prefer the `IP` or `Ethernet` taps for them, which give `File encapsulation: Raw IP` / Ethernet.
- Exports of decrypted application data are plaintext: treat them as sensitive.

## Verify
- [ ] `capinfos` shows the expected encapsulation and a non-zero packet count; open the exported file and confirm the top protocol in Protocol Hierarchy.
