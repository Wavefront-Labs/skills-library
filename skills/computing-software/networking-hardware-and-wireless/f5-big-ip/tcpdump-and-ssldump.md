---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.tcpdump-and-ssldump
name: tcpdump-and-ssldump
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, tcpdump, ssldump, packet-capture]
level: practitioner
status: draft
description: "Capture BIG-IP traffic on specific VLANs with tcpdump, include TMM-side TLS keys, and run ssldump for handshake issues."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packet capture with tcpdump and ssldump

```
tcpdump -nni 0.0:nnn -s0 -w /var/tmp/cap.pcap host 10.1.10.100 and port 443
tcpdump -nni external:nnn host 10.1.10.50
tcpdump -nni 0.0:nnnp -s0 -w /var/tmp/both.pcap host 10.1.20.11
ssldump -Aed -nr /var/tmp/cap.pcap | less
tmsh modify sys db tcpdump.sslprovider value enable
tcpdump -nni 0.0 -s0 --f5 ssl:v -w /var/tmp/keys.pcapng host 10.1.10.100
```
- `-i 0.0` captures all VLANs; `:n` shows the VLAN name, `:nn` the connection flow ID and TMM, and `:nnn` adds the owning TMM, peer ID, and so on. `:p` includes the peer flow (client and server side of the same flow) in a single capture.
- `--f5 ssl` embeds TLS session keys in a pcapng so Wireshark can decrypt; it exposes plaintext secrets, so protect and delete the file (confirm option names on your version, KB `K10209014`).
- Always limit with a host/port filter; unfiltered capture on a loaded unit can hit CPU. Use `-c 10000`/`-G` rotation to cap file size.
- The management port uses a separate interface `mgmt`: `tcpdump -nni mgmt`.
- Gotcha: with hardware offload (fastL4 with PVA/ePVA/SmartNIC) packets can bypass capture; check `tmsh list ltm profile fastl4 pva-acceleration` and disable temporarily.
- Gotcha: a capture on 0.0 shows each packet twice for a full proxy (client side and server side); the `:p` option merges, filtering by VLAN separates them.

Verify: open the pcap in Wireshark and follow the stream; both TCP handshakes (client and server side) must complete before data.
