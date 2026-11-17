---
id: computing-software.software-engineering.ruby.ruby-unsafe-deserialization
name: ruby-unsafe-deserialization
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-io-security, unsafe-deserialization]
level: advanced
status: docs-checked
description: "Avoid code execution via Marshal.load, YAML.load and ERB on untrusted input."
sources: ["https://docs.ruby-lang.org/en/master/Marshal.html", "https://docs.ruby-lang.org/en/master/Psych.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marshal and YAML deserialisation safety
- `Marshal.load` can deserialize almost any loaded class and can lead to remote code execution; do not Marshal untrusted data, use JSON or another format limited to simple types.
- Use `YAML.safe_load` / `Psych.safe_load` with `permitted_classes:` for restricted classes; `Psych.unsafe_load` and loading trusted files is a separate call.
- Keep gems updated.
Verify: run a malicious-YAML test against your loader.

## Checked
2026-11-02. Confirmed against: Marshal security section and Psych safe_load/unsafe_load. Removed or softened (not stated on those pages): Psych 4 default-behaviour claim, ERB advice (removed).
Method: documentation only; no commands were run.
