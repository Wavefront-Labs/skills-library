---
id: computing-software.software-engineering.v-lang.v-json2-and-other-formats
name: v-json2-and-other-formats
category: computing-software
field: software-engineering
product: v-lang
tags: [v-json2-and-other-formats, json-module, toml, csv, base64, hex, encoding, x.json2, config files, ini, yaml, v-lang]
level: practitioner
status: docs-checked
description: "Parse TOML with toml, YAML with yaml, CSV with encoding.csv, base64/hex with encoding modules, and use json2 for JSON."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Other data formats: toml, yaml-style configs, csv, base64

Goal: pick the right serialisation module.

- TOML: `import toml; doc := toml.parse_file('config.toml')!; port := doc.value('server.port').int()`; or `toml.decode[Config](text)!`.
- CSV: `import encoding.csv; mut r := csv.new_reader(data); for { row := r.read() or { break } ... }`.
- Base64: `import encoding.base64; base64.encode_str('hi')`, `base64.decode_str(s)`; url-safe variants `url_encode`.
- Hex: `import encoding.hex; hex.encode(bytes)`, `hex.decode(s)!`.
- JSON: `json2.decode[T](s)!` and `json2.encode(x)` (top-level `json2` module).
- YAML: `import yaml`; `yaml.parse_file(path)!`, `yaml.parse_text(text)!`, `yaml.decode[T](text)!`.
- Binary: `encoding.binary` (for example `big_endian_u32(b)`); compression: `compress.zlib` and `compress.gzip` (`compress(data)!`, `decompress(data)!`).

Gotchas:
- CSV quoting edge cases differ per producer.

Verify: round trip data through base64 and TOML sample.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: toml.parse_file/parse_text/decode and Doc.value, Any.int (vlib/toml), csv.new_reader and Reader.read, base64 encode_str/decode_str/url_encode/url_encode_str, hex.encode/decode, json2.decode/encode (vlib/json2, README), yaml.parse_file/parse_text/decode (vlib/yaml), compress.zlib and gzip compress/decompress, encoding.binary big_endian_u32.
Removed or corrected: `x.json2` (json2 is a top-level module), the 'YAML only on VPM' claim (vlib/yaml exists), the 'x. modules are experimental' gotcha, and '(confirm)' markers.
Method: documentation only; no commands were run.
