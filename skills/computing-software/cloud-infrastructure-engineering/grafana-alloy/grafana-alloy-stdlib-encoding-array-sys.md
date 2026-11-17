---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-stdlib-encoding-array-sys
name: grafana-alloy-stdlib-encoding-array-sys
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [encodingfrom-json, encodingto-json, encodingfrom-yaml, encodingfrom-base64, arrayconcat, arraycombine-maps, arraygroup-by, coalesce, sysenv, filepath-join]
level: practitioner
status: docs-checked
description: "Alloy stdlib for JSON, YAML, Base64, URL encoding, array.concat, combine_maps, group_by, coalesce defaults, sys.env and file.path_join."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/stdlib/encoding.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/stdlib/array.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/stdlib/coalesce.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/stdlib/sys.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/stdlib/file.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# encoding, array, coalesce, sys and file functions

## encoding
- `encoding.from_json` / `encoding.from_yaml` decode a string into an Alloy value, commonly applied to `local.file.some_file.content`. Escape quotes in literals: `encoding.from_json("{\"key\": \"value\"}")`.
- `encoding.to_json` encodes a map; useful for components that want a JSON string such as the `config` argument of `prometheus.exporter.blackbox`.
- `encoding.to_base64`, `from_base64`, `to_URLbase64`, `from_URLbase64` (RFC4648), and `encoding.url_encode` / `url_decode` (RFC3986 percent encoding). Invalid input errors.

## array
- `array.concat([1, 2], [3, 4])` joins lists; every argument must be a list.
- `array.combine_maps(list_a, list_b, ["instance"], true)` (experimental) merges maps whose listed keys match. Maps lacking the keys are discarded, values from the second list win, and a true fourth argument keeps unmatched items from the first list. It enriches targets before a scrape; it cannot add labels to metrics (use `prometheus.enrich`).
- `array.group_by(objects, "type", drop_missing)` (experimental) groups by a top-level string key, returning `{type, items}`; pair with `foreach` and `id`.

## Misc
- `coalesce(a, b, ...)` returns the first argument that is not null, an empty string, an empty list or an empty object, else the last argument: `coalesce(sys.env("DOES_NOT_EXIST"), "c")` gives `"c"`.
- `sys.env("NAME")` returns an empty string for an unset variable.
- `file.path_join("this/is", "a/path")` joins with the OS separator.

## Checked

2026-11-04. Confirmed against the Alloy stdlib pages encoding, array, coalesce, sys and file: function names, behaviour, experimental status of combine_maps and group_by, prometheus.enrich note, sys.env empty-string result, file.path_join. Fixed coalesce wording to match the page.

Method: documentation only; no commands were run.
