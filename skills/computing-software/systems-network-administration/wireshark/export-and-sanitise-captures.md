---
id: computing-software.systems-network-administration.wireshark.export-and-sanitise-captures
name: export-and-sanitise-captures
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, export-specified-packets, pcap-sanitization, tracewrangler, editcap, anonymisation, data-protection]
level: practitioner
status: verified
description: "Share only what is needed: Export Specified Packets of the displayed subset, strip payloads, anonymise addresses with TraceWrangler, and remove keys and comments."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html
  - https://www.tracewrangler.com/
  - https://wiki.wireshark.org/Tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and sanitise captures

Captures contain credentials, personal data, internal addressing, TLS keys (if embedded),
and comments. Before sending one to a vendor or posting it, cut it down.

## Export only the relevant packets
1. Apply a display filter (e.g. `tcp.stream in {17,23}`; Wireshark 4.x set members are comma separated, spaces fail to parse).
2. File > **Export Specified Packets** > "All packets: Displayed" (optionally "Include
   depended upon packets" so reassembly still works), save as pcapng.
3. Or mark packets (Ctrl+M) and export "Marked packets only".
CLI: `tshark -r in.pcapng -2 -R 'tcp.stream in {17,23}' -w out.pcapng` (`-2` is required for `-R`).

## Remove what is not needed
- Payloads: `editcap -s 96 in.pcapng hdrs.pcapng` (headers only).
- Embedded TLS secrets: `editcap --discard-all-secrets in.pcapng out.pcapng`.
- Packet comments: `editcap --discard-packet-comments` (present in 4.4.1); `editcap -a <frame>:<comment>` adds one.
- Interface names and OS info sit in the pcapng SHB/IDB; saving as plain pcap drops them.

## Anonymise
- **TraceWrangler** (Windows, or Linux via WINE; GPLv2 open source): sanitises and anonymises pcap/pcapng by removing
  or replacing sensitive data. Its page warns IPv6 checksums may be wrong when extension headers are present.
- `tcprewrite --pnat=10.1.0.0/16:198.51.0.0/16 --infile=in.pcap --outfile=out.pcap --fixcsum`
  (tcpreplay suite) for simple prefix mapping; `--pnat` takes comma-separated `from-CIDR:to-CIDR` pairs (the second
  netblock's prefix is used as the mask) and already forces checksum recalculation, so `--fixcsum` is optional.
- Anonymising does not touch addresses inside payloads (DNS answers, HTTP headers, SIP SDP);
  strip or check those.

## Verify
Open the output, run `Statistics > Endpoints` and search for strings
(`frame contains "password"`, internal domain names, emails). Check
Capture File Properties for comments and embedded secrets.
- [ ] Shared file contains only the target flows, no secrets, and anonymised addresses where required.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1: `tshark -r in.pcapng -2 -R 'tcp.stream in {0,1}' -w out.pcapng` wrote only streams 0 and 1; the space-separated form `{0 1}` is a syntax error ("1" was unexpected), as is `tcp.port in {8443 8444}` (the old form in this skill), so the examples now use commas. `editcap -s 96` (capinfos: snaplen 96), `--discard-all-secrets`, `-a 3:hello`, `--discard-packet-comments` (comment count 1 then 0) and `-F pcap` all ran.
- tcprewrite flags checked in the tcpreplay source (https://raw.githubusercontent.com/appneta/tcpreplay/master/src/tcpedit/tcpedit_opts.def): `--pnat` pair syntax and `--fixcsum` (auto-enabled by `--pnat`); tcprewrite itself is not installed here and was not run.
- TraceWrangler capabilities and licence read at https://www.tracewrangler.com/ (open source GPLv2, Windows or WINE, sanitising/anonymising, IPv6 checksum warning).
