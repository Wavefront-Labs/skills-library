---
id: computing-software.systems-network-administration.wireshark.working-with-large-capture-files
name: working-with-large-capture-files
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, large-capture-files, editcap, tshark, splitting, memory, performance]
level: practitioner
status: verified
description: "Analyse multi-GB captures without crashing Wireshark: split by time or count, pre-filter with tshark/dumpcap, disable costly dissection, and choose the right tool per size."
sources:
  - https://www.wireshark.org/docs/man-pages/editcap.html
  - https://wiki.wireshark.org/KnownBugs/OutOfMemory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with large capture files

Wireshark keeps per-packet state in RAM plus reassembly buffers, so very large captures need a lot of memory; measure
on your own files rather than trusting a per-packet figure.

## Narrow first, then open
```
capinfos -c -a -e big.pcapng                       # what's in it
editcap -A "2026-10-18 14:00:00" -B "2026-10-18 14:10:00" big.pcapng window.pcapng
tshark -r big.pcapng -Y "ip.addr == 10.0.0.5" -w host.pcapng
```
tshark cannot apply a BPF capture filter while reading a file (`tshark -r f -f "host 10.0.0.5"` fails with "Only read filters,
not capture filters, can be specified when reading a capture file"), so a display-filter cut dissects every packet. Cut by
time with `editcap -A/-B` first, which does not dissect.

## Split
```
editcap -c 1000000 big.pcapng part.pcapng          # 1M packets per file
editcap -i 300 big.pcapng part.pcapng              # 5-minute files
```

## Statistics without the GUI
```
tshark -r big.pcapng -q -z conv,tcp > conv.txt
tshark -r big.pcapng -q -z io,stat,60 > io.txt
tshark -r big.pcapng -q -z endpoints,ip
```
Find the interesting time/host with stats, then cut that slice for the GUI.

## Make Wireshark lighter
- Disable heavy protocols you do not need (Analyze > Enabled Protocols), turn off TCP reassembly
  and "Analyze TCP sequence numbers" for a first look.
- Turn off name resolution.
- Use a lean profile with few columns and no custom columns that force full dissection.
- `tshark -2` reads the file twice (needed for `-R` read filters and some dependent fields); avoid it on huge files unless needed.

## Other tools for very big data
Flow or log generators and capture indexers exist (not covered or run here); when you only need connection summaries,
`tshark -q -z conv,tcp` above is the built-in route.

## Gotchas
- Ring-buffer captures are pre-split; use capinfos to find the right file instead of merging all.
- `mergecap` on many big files produces an even bigger file; merge only the slice you need.

## Verify
- [ ] The file opened in the GUI is under a few hundred MB and covers the incident window.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 with a 73-packet loopback pcapng: `capinfos -c -a -e` (packet count, earliest and latest time), `editcap -A/-B` with the space-separated timestamp form (04:00 start returned 0 packets, 03:00-23:00 returned all 73; the ISO `T` form from `editcap -h` also works), `editcap -c 20` made 4 part files and `-i 1` split by seconds (6 files in the folder), `tshark -q -z io,stat,60`, `-z conv,tcp`, `-z endpoints,ip` and `-2` ran as shown.
- Removed the unverified figures ("1 KB per packet", "10x faster tcpdump", 32-bit failure) and the tool list I could not run; a `tshark -r ... -f` BPF read cut does not work in 4.4.1 (error text above, run), so that suggestion was replaced.
