---
id: computing-software.systems-network-administration.nix.nix-prefetch-url-hash
name: nix-prefetch-url-hash
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-prefetch-url, prefetch, fetchurl-hash, unpack]
level: intro
status: docs-checked
description: "Download a file into the Nix store and print its hash with nix-prefetch-url for fetchurl, fetchzip and fetchFromGitHub; use --unpack, --name and --print-path."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-prefetch-url.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-prefetch-url` downloads a file, prints its hash and copies it into the store as hash plus the URL's base name, so `fetchurl` can reuse it.

```
nix-prefetch-url ftp://ftp.gnu.org/pub/gnu/hello/hello-2.10.tar.gz
nix-prefetch-url --print-path mirror://gnu/hello/hello-2.10.tar.gz
nix-prefetch-url --unpack --print-path https://github.com/NixOS/patchelf/archive/0.8.tar.gz
```

Options:
- `--type <hashAlgo>`: `blake3`, `md5`, `sha1`, `sha256` (default), `sha512`.
- `--print-path`: also print the store path.
- `--unpack`: unpack a tarball or zip first; the hash then suits `fetchzip` or `fetchFromGitHub`.
- `--executable`: set the executable bit.
- `--name <name>`: override the store filename when the URL's base name has characters not allowed in store paths.

Notes:
- Passing a hash argument skips the download if the store already has that file; a mismatch after download is an error.
- The hash prints in Nix32, except `--type md5`, which is base-16.

## Checked

2026-11-04: store naming, options, defaults, hash-argument behaviour, Nix32 versus base-16 output and the three examples confirmed against the nix-prefetch-url manual page. Removed the Verify line, which restated the hash-argument rule with a claim the page does not make.

Method: documentation only; no commands were run.
