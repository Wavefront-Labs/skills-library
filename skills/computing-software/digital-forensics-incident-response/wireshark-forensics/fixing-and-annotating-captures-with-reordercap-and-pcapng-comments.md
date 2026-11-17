---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.fixing-and-annotating-captures-with-reordercap-and-pcapng-comments
name: fixing-and-annotating-captures-with-reordercap-and-pcapng-comments
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [reordercap, pcapng-comments, editcap, mergecap, capture-preparation, dfir]
level: practitioner
status: draft
description: "Prepare evidence captures: reorder out-of-order timestamps with reordercap, merge and time-shift with mergecap/editcap, and annotate packets and files with pcapng comments."
sources: ["https://www.wireshark.org/docs/man-pages/reordercap.html", "https://www.wireshark.org/docs/man-pages/editcap.html", "https://www.wireshark.org/docs/man-pages/mergecap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixing and annotating captures (reordercap, pcapng comments)

Captures from multiple interfaces, taps with buffering, or merged sensors often have frames out of timestamp order, which confuses TCP analysis and timelines. pcapng comments let you annotate evidence for colleagues and reports without altering packet data.

## Working copies only
Never modify the original capture. Hash it, work on copies, and record every command.

## Reorder by timestamp
```bash
reordercap original.pcapng ordered.pcapng
```
reordercap sorts frames by timestamp and reports how many were out of order. Use `-n` to avoid writing a file if already in order (check `-h`). Out-of-order counts themselves can be noted in the report (sensor behaviour).

## Merge and correct time
```bash
mergecap -w merged.pcapng sensorA.pcapng sensorB.pcapng      # chronological merge (default)
mergecap -a -w concat.pcapng part1.pcap part2.pcap           # concatenate without sorting
editcap -t -3.250 sensorB.pcapng sensorB_shifted.pcapng      # shift timestamps by seconds
editcap -A "2026-10-18 13:00:00" -B "2026-10-18 14:00:00" in.pcapng window.pcapng
editcap -D 5 in.pcapng dedup.pcapng                          # drop duplicates seen within 5 frames
```
Apply a time shift only when you have measured the sensor's clock offset; document the offset and its source.

## Annotate with comments
- GUI: select a packet > Edit > Packet Comment (Ctrl+Alt+C); file-level comment via Statistics > Capture File Properties. Find commented packets with filter `frame.comment` (or `pkt_comment` in older versions), and list them in Statistics > Capture File Properties.
- CLI: `editcap -a 1234:"Beacon starts, see case note 17" in.pcapng annotated.pcapng` adds a packet comment (Wireshark 3.6+); `editcap --capture-comment "Case 2026-0147, sensor A, SPAN of core switch"` adds a file comment (newer versions; check `editcap -h`).
- Save as pcapng: comments are lost in legacy pcap.

## Gotchas
- Wireshark "Save" after adding comments rewrites the file; use "Save As" to a new name.
- Merging captures with different link types forces pcapng with multiple interfaces; some tools handle that poorly; check `capinfos` afterwards.
- `editcap -D` deduplication may remove legitimate retransmissions; only use when SPAN duplication is confirmed.

## Verify
`capinfos` on derived files shows expected packet counts and time range, original hashes are unchanged, and every derived file has its generating command recorded.
