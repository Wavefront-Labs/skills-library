---
id: computing-software.systems-network-administration.wireshark.tshark-pdml-and-psml-output
name: tshark-pdml-and-psml-output
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, pdml, psml, xml-output, automation]
level: practitioner
status: verified
description: "Export full dissection as PDML or summary lines as PSML from tshark, and parse them with XPath when field extraction is not enough."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://wiki.wireshark.org/PDML
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDML/PSML output

- PDML (Packet Details Markup Language): every protocol and field, as XML.
- PSML (Packet Summary Markup Language): the packet list columns, as XML.

## Commands
```
tshark -r in.pcapng -T pdml > in.pdml
tshark -r in.pcapng -Y "sip" -T pdml -J "sip sdp" > sip.pdml    # trims fields below the listed protocols (see Gotchas)
tshark -r in.pcapng -T psml > in.psml
```
PSML starts with `<structure>` listing the column names (No., Time, Source, Destination, Protocol, Length, Info) and then one row per packet.

## PDML structure
```xml
<packet>
  <proto name="ip" showname="Internet Protocol Version 4" size="20" pos="14">
    <field name="ip.src" showname="Source Address: 10.1.1.5" size="4" pos="26" show="10.1.1.5" value="0a010105"/>
```
`show` is the display value, `value` the raw hex, `pos`/`size` the byte offset and length. The real output also carries a leading
`geninfo` proto and a `frame` proto before `eth` and `ip`; sub-fields nest inside their parent `field`.

## Parsing
```
xmllint --xpath '//field[@name="dns.qry.name"]/@show' in.pdml    # needs libxml2; not available in the test environment
python - <<'PY'
import xml.etree.ElementTree as ET
for _, el in ET.iterparse("in.pdml"):
    if el.tag == "packet":
        q = el.find(".//field[@name='dns.qry.name']")
        if q is not None: print(q.get("show"))
        el.clear()
PY
```
Use iterparse and `el.clear()`; PDML is far larger than the capture (a 1.7 KB, 13-packet capture produced 209 KB of PDML, about 119x).
The Python snippet found both DNS names in the test capture.

## When to choose PDML
- You need the hierarchy (which field belongs to which protocol layer instance).
- You need byte positions for carving or highlighting.
For flat values prefer `-T fields`; for scripting with nested structure prefer `-T json` / `-T ek`.

## Gotchas
- Combine with `-Y` to keep size manageable. In 4.4.1 `-J dns` / `-j dns` on `-T pdml` still emitted the `geninfo`, `frame`, `eth`,
  `ip` and `udp` protos; they trim child fields in json/ek (`"filtered"` markers), so measure the size before relying on them.
- Two-pass dissection (`-2`) is needed for fields that depend on later packets (reassembly
  results, response-in links).

## Verify
- [ ] The XPath result count equals `tshark -Y <field> | wc -l` on the same file.
