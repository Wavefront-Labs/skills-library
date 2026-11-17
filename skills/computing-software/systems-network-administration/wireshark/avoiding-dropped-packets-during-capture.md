---
id: computing-software.systems-network-administration.wireshark.avoiding-dropped-packets-during-capture
name: avoiding-dropped-packets-during-capture
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dumpcap, dropped-packets, capture-buffer, snaplen, ring-buffer, tcpdump-buffer, pcapng]
level: practitioner
status: verified
description: "Prevent capture loss on busy links: dumpcap buffer size, snaplen, capture filters, writing to fast disk, no live update, and reading the drop counters."
sources:
  - https://wiki.wireshark.org/Performance
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
  - https://www.tcpdump.org/manpages/tcpdump.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding dropped packets

A capture that dropped packets shows fake problems (missing segments, ACKed unseen). Know
your drop counts before you trust the analysis.

## Where drops are reported
- Wireshark: the User's Guide says pcapng files can save the number of packets dropped while capturing; that comes from
  interface statistics blocks, and a short dumpcap ring-buffer run here wrote none (`capinfos -I`: `Number of stat
  entries = 0`), so keep the console message below.
- `dumpcap` at exit (4.4.1, Windows): `Packets captured: 63` and `Packets received/dropped on interface '...': 63/0
  (pcap:0/dumpcap:0/flushed:0/ps_ifdrop:0) (100.0%)`; `-q` suppresses these counts.
- tcpdump: `N packets dropped by kernel` (OS buffer space) and `M packets dropped by interface` where the platform reports it.
- `ethtool -S eth0 | grep -i drop` for driver and NIC counters below libpcap (`-S` queries device statistics; counter names vary by driver).

## Settings that help
```bash
dumpcap -i eth0 -B 512 -s 128 -f "host 10.1.1.10" -b filesize:500000 -b files:20 -w /fast/cap.pcapng
tcpdump -i eth0 -B 524288 -s 128 -n -w /fast/cap.pcap "host 10.1.1.10"
```
The dumpcap line ran on Windows with `-i` set to the Npcap loopback adapter and `-f "host 127.0.0.1"` plus `-a duration:4`
(`-b filesize` is in kB, so 500000 = 500 MB; the file is named `cap_00001_<timestamp>.pcapng`; `capinfos` reported a 128-byte
packet size limit). The tcpdump line uses flags documented on its manual page.
- `-B` kernel buffer (dumpcap MiB, default 2; tcpdump KiB; so tcpdump `-B 524288` equals dumpcap `-B 512`): absorbs bursts.
- Snaplen 96-128 bytes captures headers only: 128 of a 1500-byte frame is 8.5%, about 12 times less to copy and write.
- A capture filter costs some processing but, per the same wiki page, can reduce overall load when you only need some packets.
- Use `dumpcap`, not the Wireshark GUI, for long or fast captures: the Wireshark Performance wiki says to capture with a
  "capture only" program, not to use "Update list of packets in real time", and to raise the buffer size.
- `-n` / disable name resolution (tcpdump `-n` does no name conversion; lookups for every address can stall printing).
- Write to local SSD, not a network share.

## Beyond software
- NIC offloads such as GRO/LRO change what the capture sees; `ethtool -K eth0 gro off lro off` switches them off (`-K` changes offload
  parameters, `gro`/`lro` take on|off; ethtool(8)).

## Verify
- [ ] Capture summary reports 0 dropped (kernel and interface) for the analysed window.

## Checked
Run on Windows with Wireshark 4.4.1: the dumpcap command above (loopback, 4 s) captured 63 packets, printed the quoted
received/dropped summary, wrote one ring-buffer file, and `capinfos -a -e -c` showed 63 packets and a 128-byte limit;
`dumpcap -h` confirmed `-B` is in MiB with a 2 MiB default and the `-b` units. tcpdump `-B` (KiB), `-n`, and the
kernel/interface drop wording were read from the tcpdump.org manual page; User's Guide read for the dropped-packet note and the
real-time update option. ethtool `-S`, `-K` and the `gro`/`lro` options were read from the Debian ethtool manual page and the Wireshark Performance wiki was read for the capture advice; SPAN and high-speed capture remarks were removed.
