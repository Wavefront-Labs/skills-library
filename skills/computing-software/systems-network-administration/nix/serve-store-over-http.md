---
id: computing-software.systems-network-administration.nix.serve-store-over-http
name: serve-store-over-http
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-serve, binary-cache, http-cache, substituters]
level: practitioner
status: docs-checked
description: "Share a machine's Nix store as an HTTP binary cache with nix-serve, check nix-cache-info, and add it to a client's substituters."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/binary-cache-substituter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The store is served with the same binary cache mechanism as cache.nixos.org. `nix-serve` is not part of Nix but is in Nixpkgs.

Server:

```
nix-env --install --attr nixpkgs.nix-serve
nix-serve -p 8080
```

Verify from a client; the reply lists `StoreDir`, `WantMassQuery` and `Priority`:

```
curl http://avalon:8080/nix-cache-info
```

(`avalon` is the manual's example host.) `nix copy` creates that file automatically when writing to a binary cache that lacks it.

Use it once:

```
nix-env --install --attr nixpkgs.firefox --substituters http://avalon:8080/
```

This adds the server to your default caches; Nix builds from source if no cache has the path.

Make permanent in `nix.conf`, keeping the default cache in the list:

```
substituters = http://avalon:8080/ https://cache.nixos.org/
```

## Checked

2026-11-04: nix-serve install and start, nix-cache-info check and reply fields, automatic nix-cache-info creation, --substituters use, fallback to building from source and the nix.conf line confirmed against the Serving a Nix store via HTTP manual page. Removed the signature Gotcha, which this page does not state.

Method: documentation only; no commands were run.
