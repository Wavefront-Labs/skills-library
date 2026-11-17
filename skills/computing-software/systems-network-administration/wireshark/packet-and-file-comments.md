---
id: computing-software.systems-network-administration.wireshark.packet-and-file-comments
name: packet-and-file-comments
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, packet-comments, pcapng, annotation, capture-file-properties]
level: practitioner
status: verified
description: "Annotate captures with pcapng packet and file comments in Wireshark, editcap and tshark, filter on them, and strip them before sharing."
sources:
  - https://www.wireshark.org/docs/man-pages/editcap.html
  - https://www.wireshark.org/docs/dfref/f/frame.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Packet and file comments

pcapng stores comments per packet and per file. Use them to hand an analysis to someone else:
"retransmission starts here", "user reported freeze at 10:42:05".

## Adding comments in Wireshark
- Packet: right-click > Packet Comment > Add New Comment (Ctrl+Alt+C, per the User's Guide). A packet can hold
  several.
- File: Statistics > Capture File Properties, edit the comment there.
- Save as pcapng; pcap does not support comments (the User's Guide says so, and `editcap -F pcap` dropped both kinds in a run).

## Finding commented packets
```
frame.comment
frame.comment contains "retrans"
pkt_comment                       # old name; still accepted as a filter in 4.4.1
```
Expert Information lists every packet comment under "Comment" (`tshark -z expert` printed a `Comments (1)` section), a quick table of contents. Add a
column for `frame.comment` to read them inline.

## Command line
```
editcap -a 1523:"first RST from LB" in.pcapng out.pcapng      # add comment to frame 1523
editcap --capture-comment "Case 4471, site B core" in.pcapng out.pcapng
editcap --discard-packet-comments in.pcapng clean.pcapng
editcap --discard-capture-comment in.pcapng clean.pcapng
tshark -r in.pcapng -Y frame.comment -T fields -e frame.number -e frame.comment
capinfos -k in.pcapng                                           # show capture comments
```

## Gotchas
- Comments can contain sensitive notes (usernames, IPs, case details). Strip them when sending a
  capture outside the team.
- Some tools (old tcpdump, libpcap writers) cannot read pcapng comments; convert with
  `editcap -F pcap` only after exporting the notes elsewhere.
- Comments edited in the GUI are not saved until you save the file; the title bar shows `*`.

## Verify
- [ ] Reopen the saved file and confirm `frame.comment` matches the expected count (the commands above were all run: `-a`
added frame 23's comment, `--capture-comment` showed in `capinfos -k`, and both discard options removed them).
