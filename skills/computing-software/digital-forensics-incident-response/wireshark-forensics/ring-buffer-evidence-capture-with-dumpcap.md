---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.ring-buffer-evidence-capture-with-dumpcap
name: ring-buffer-evidence-capture-with-dumpcap
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [dumpcap, ring-buffer, packet-capture, continuous-capture, capture-filters, evidence-collection, dfir]
level: practitioner
status: verified
description: "Run long-term evidentiary packet capture with dumpcap ring buffers: file rotation, capture filters, snaplen, drop monitoring, hashing and service setup."
sources: ["https://www.wireshark.org/docs/man-pages/dumpcap.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChCapCaptureFiles.html", "https://www.tcpdump.org/manpages/pcap-filter.7.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ring-buffer evidence capture with dumpcap

**Goal:** capture traffic on a SPAN/TAP port or a suspect host for days without filling the
disk or dropping packets, producing files you can hash and hand over.

## Why dumpcap
It is Wireshark's capture engine without dissectors: low CPU and memory, safe to run with
reduced privileges, and stable for long runs (Wireshark GUI capture is not).

## Command
```bash
dumpcap -D                                            # list interfaces
dumpcap -i eth1 -B 512 -s 0 \
  -b filesize:1000000 -b files:200 \
  -f "not (host 10.0.0.5 and port 22)" \
  -w /evidence/case42/sensor1.pcapng
```
- `-b filesize:<kB>` rotate at ~1 GB; `-b duration:3600` rotate hourly; `-b files:N` keep N
  files (ring); omit `files` to keep everything (watch disk).
- `-B` kernel buffer in MiB; raise it for busy links to avoid drops.
- `-s 0` full packets (default snaplen is already 262144); reduce only if legal/privacy limits
  require headers only.
- `-f` capture filter (BPF): exclude your own management traffic and high-volume trusted flows
  (backups) to extend retention; do not over-filter.
- Output files are `sensor1_00001_20261016093000.pcapng`: sequence plus start time.
- `-P` writes pcap instead of pcapng (files are then named `.pcap`); the dumpcap man page marks it deprecated in favour of `-F`, and multi-interface captures stay pcapng.

## Running as a service
```bash
sudo setcap cap_net_raw,cap_net_admin+eip /usr/sbin/dumpcap   # run without root (form from the Wireshark capture-privileges page)
```
Then start dumpcap from your service manager of choice (for example a systemd unit).
On Windows, use the Npcap driver and run dumpcap from a scheduled task or NSSM service.

## Integrity
- Hash each rotated file once it is closed (a scheduled job that hashes every file except the newest one works);
  store hashes separately. The filter string and capture length are stored in the pcapng interface block
  (`capinfos -I`), which helps the collection log.
- Record sensor location, interface, filter, start/stop times, NTP status and examiner.
- `capinfos sensor1_*.pcapng` reports packet counts, duration and first/last times.

## Watching for drops
dumpcap prints `Packets captured: N` and, on Windows, `Packets received/dropped on interface '<name>': R/D (pcap:..
/dumpcap:../flushed:../ps_ifdrop:..)` on exit; pcapng can also record interface statistics
(Statistics > Capture File Properties). Drops on SPAN ports also occur in the
switch; compare with interface counters.

## Gotchas
- Full-packet capture contains personal data; confirm legal authority and retention.
- Ring buffers overwrite evidence: when an alert fires, copy relevant files out of the ring
  immediately.
- Clock: the sensor must be NTP-synced or timestamps will not line up with logs.

## Self-check
Capture runs without drops, files rotate and are hashed as they close, and the capture
parameters are documented.

## Checked
Run on Wireshark 4.4.1 on Windows with a loopback capture: `-B 512 -s 0 -b filesize:1 -b files:3 -f ...` produced only
the newest 3 of 31 rotated files named `sensor1_00031_20261022044229.pcapng` (sequence plus start time), `-b duration:2
-P` produced `.pcap` files, `capinfos -I` showed capture length 262144 for `-s 0` and the filter string, and the exit
output was as quoted above. The `setcap` form is from the Wireshark capture-privileges page; `-P` text is from the
dumpcap man page. The Linux-only service lines that were not runnable here were removed.
