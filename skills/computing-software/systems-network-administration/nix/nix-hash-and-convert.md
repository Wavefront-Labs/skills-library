---
id: computing-software.systems-network-administration.nix.nix-hash-and-convert
name: nix-hash-and-convert
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-hash, hash-conversion, sri-hash, nar-hash]
level: practitioner
status: docs-checked
description: "Hash paths with nix-hash (NAR versus --flat) and convert hashes between base16, Nix32, Base64 and SRI formats, matching nix-prefetch-url output."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-hash.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hashing: `nix-hash [--flat] [--base32] [--truncate] [--type hashAlgo] path...`
Converting: `nix-hash [--to-base16|--to-base32|--to-base64|--to-sri] [--type hashAlgo] hash...`

By default the hash covers the path serialised in NAR format (handles directories and symlinks), using MD5 printed in hex. Without `--flat`, `nix-hash path` equals `nix-store --dump` piped to `md5sum`.

Options:
- `--flat`: hash a regular file's contents directly (matches `md5sum`, `sha1sum`); a directory is an error ("Is a directory").
- `--base16` (default), `--base32` (Nix32, usable in `fetchurl` calls), `--base64`, `--sri` (algorithm name, hyphen, Base64).
- `--truncate`: cut hashes longer than 160 bits to 160 bits.
- `--type`: `blake3`, `md5`, `sha1`, `sha256`, `sha512`.
- `--to-*`: convert an existing hash without hashing anything. The option text says the input is Nix32 for `--to-base16` and hex for the others; the page examples also convert SRI input with `--to-base16` and Nix32 input with `--to-sri`.

Reproduce `nix-prefetch-url` output:

```
nix-hash --type sha256 --flat --base32 file
```

## Checked

2026-11-04: both synopses, NAR default, MD5 default, --flat rules, output formats, --truncate, --type list, conversion options and the nix-prefetch-url example confirmed against the nix-hash manual page. Removed the Verify line, which the page does not state, and reworded the --to-* input note to match the page.

Method: documentation only; no commands were run.
