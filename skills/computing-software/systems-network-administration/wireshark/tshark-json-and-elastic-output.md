---
id: computing-software.systems-network-administration.wireshark.tshark-json-and-elastic-output
name: tshark-json-and-elastic-output
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, tshark-json, elastic-ek, json, jq, elasticsearch, ndjson]
level: practitioner
status: verified
description: "Feed captures into pipelines with tshark -T json, jsonraw and ek (Elasticsearch bulk), limiting protocols and fields with -j/-J/-e, and parsing with jq."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://www.elastic.co/guide/en/beats/packetbeat/current/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark JSON and EK output

| `-T` | Output |
|---|---|
| `json` | one JSON array, nested layers per protocol |
| `jsonraw` | like json but values are `[raw hex, offset, length, ...]` arrays instead of strings |
| `ek` | newline-delimited JSON in Elasticsearch bulk format: an index line such as `{"index":{"_index":"packets-2023-11-15","_type":"doc"}}` then the document, with dots in field names replaced by underscores (`ip_src`) and every value an array |
| `pdml` | XML |

```bash
# Chosen fields as flat JSON (each value is a list of strings), parsed with Python
tshark -r cap.pcapng -Y dns -T json -e ip.src -e dns.qry.name | python -c "import json,sys; [print(p['_source']['layers']['dns.qry.name'][0]) for p in json.load(sys.stdin)]"
# Only chosen fields in EK (ndjson) for a bulk loader
tshark -r cap.pcapng -Y http.request -T ek -e frame.time -e ip.src -e http.host -e http.request.uri > http.ndjson
```
In the full (no `-e`) JSON the DNS name is not directly under `dns`: it sits inside a nested `Queries` object keyed by
`name: type A, class IN`, so a path like `.dns["dns.qry.name"]` fails with a key error on 4.4.1. Use `-e dns.qry.name` for flat access.
The commands were run on TShark 4.4.1; `jq` was not installed for the test, so the parsing here is shown with Python's `json`.
- `-j "proto ..."` keeps the listed protocols' parent node only; child nodes appear only if listed (`-j "ip ip.flags http"`).
  `-J` keeps the listed protocol and all its children, but lower-level protocols must be listed explicitly (man page).
  Excluded children show as `"Queries": {"filtered": "Queries"}`. Without filters, JSON per packet is large.
- `-e` with json/ek outputs only those fields (flat; values are lists of strings in `json`).
- Field values are strings in json (`"ip.len": "683"`); cast them in your parser.
- EK index names come from the capture date (`packets-YYYY-MM-DD`). `tshark -G elastic-mapping` prints a mapping template
  (`"dynamic": false`, `timestamp` as `date`) to create before loading.

## Gotchas
- Duplicate keys appear when a protocol occurs twice (tunnels); some JSON parsers keep only
  the last. Use `--no-duplicate-keys` (listed in `tshark -h` for `-T json`) to merge them into arrays: on a GRE packet the two `ip` objects
  became one `ip` array.
- Streaming large files: `-T ek` is line oriented and safe to stream; `-T json` is a single
  array (load into memory or use a streaming JSON parser).

## Verify
- [ ] Your JSON parser reads the whole output without error and the record count equals `tshark -Y <filter> | wc -l`.
