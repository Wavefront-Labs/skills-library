---
id: computing-software.systems-network-administration.wireshark.repairing-corrupted-captures
name: repairing-corrupted-captures
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, pcapfix, corrupted-capture, editcap, truncated-file, pcapng, recovery]
level: practitioner
status: verified
description: "Recover packets from truncated or corrupted capture files: diagnose the error, salvage with editcap and tshark, repair headers with pcapfix, and avoid corruption next time."
sources:
  - https://github.com/Rup0rt/pcapfix
  - https://www.wireshark.org/docs/man-pages/editcap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repairing corrupted captures

## Typical errors
- `The capture file appears to have been cut short in the middle of a packet.` Capture killed
  (power loss, disk full, kill -9). Everything before the cut is fine.
- `The file "x" isn't a capture file in a format Wireshark understands.` (tshark and editcap say "TShark"/"editcap" instead) Header damaged, wrong
  extension (gzip, a text export), or transferred in FTP ASCII mode.
- `pcapng: total block length N is too large (> M)`. Corruption mid-file (message text from wiretap/pcapng.c in Wireshark 4.4.1).

## Salvage the readable part
Wireshark opens a cut-short file and shows packets up to the damage. Re-save it:
```
editcap cut.pcapng clean.pcapng          # copies readable packets, writes a valid file
tshark -r cut.pcapng -w clean.pcapng     # same idea
```
Both stop at the first unreadable record; packets after it need pcapfix.

## pcapfix
```
pcapfix -d broken.pcap            # -d deep scan (pcap only; pcapng is scanned block by block anyway)
pcapfix -n broken.pcap            # force the pcapng format
pcapfix -o repaired.pcap broken.pcap   # choose the output name
# default output name: fixed_ + input name, e.g. fixed_broken.pcap
capinfos fixed_broken.pcap
```
It rebuilds the global header, fixes record lengths and skips garbage. Check timestamps afterwards;
garbage interpreted as packets shows as absurd dates (sort by time and trim with editcap -A/-B).

## Check for wrong formats first
```
file mystery.cap            # gzip? Microsoft Network Monitor? Text?
```
- gzip: Wireshark reads `.pcap.gz` directly; or `gunzip`.
- NetMon `.cap`, Snoop, Endace ERF: Wireshark reads them natively; just use File > Open.
- Text hex dumps: use text2pcap.
- ASCII-mode FTP corruption (CR/LF rewrites) is often irrecoverable; re-transfer in binary.

## Prevent it
- Capture with ring buffers (`-b filesize`): a crash loses at most the last file's tail.
- Leave disk headroom; `dumpcap` stops cleanly with `-a filesize`/`-a duration`.
- Stop captures with Ctrl+C / SIGINT (clean close), not SIGKILL.

## Verify
- [ ] `capinfos` on the repaired file shows sane first/last times and packet count close to
  expectations.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1: a pcapng and a pcap truncated mid-file gave `... appears to have been cut short in the middle of a packet.` from tshark (exit 2) and editcap; `editcap cut.pcapng clean.pcapng` and `tshark -r cut.pcapng -w clean.pcapng` both wrote valid files (capinfos 73 packets); a pcap whose magic number was zeroed gave `isn't a capture file in a format TShark understands` from tshark and the editcap equivalent; `tshark -r x.pcap.gz` read a gzip-compressed pcap (73 packets).
- pcapfix itself is not installed here and was not run; its options (`-d` deep scan, pcap only; `-n` force pcapng; `-o` output; default output `fixed_` + name) were read from its README and source: https://raw.githubusercontent.com/Rup0rt/pcapfix/master/README and pcapfix.c.
- pcapng error wording taken from wiretap/pcapng.c at tag wireshark-4.4.1; the old "bad record length" string does not exist there and was removed. `text2pcap -e 0x800` turned a hex dump into a 1-packet pcap, `dumpcap -b filesize:1 -a duration:2` rotated ring files (`-a filesize`/`-a duration`/`-b filesize` appear in `dumpcap -h`), and the Wireshark User's Guide open-file list (https://www.wireshark.org/docs/wsug_html_chunked/ChIOOpenSection.html) includes Microsoft Network Monitor, Sun snoop and Endace ERF captures. The FTP ASCII-mode corruption remark and "stop with Ctrl+C not SIGKILL" are advice, not tested.
