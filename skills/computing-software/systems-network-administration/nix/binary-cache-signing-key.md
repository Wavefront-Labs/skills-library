---
id: computing-software.systems-network-administration.nix.binary-cache-signing-key
name: binary-cache-signing-key
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, signing-key, trusted-public-keys, secret-key-files, generate-binary-cache-key]
level: advanced
status: docs-checked
description: "Generate a binary cache signing key pair with nix-store --generate-binary-cache-key and wire trusted-public-keys, substituters and secret-key-files."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/post-build-hook.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate the pair (name, private file, public file):

```
nix-store --generate-binary-cache-key example-nix-cache-1 /etc/nix/key.private /etc/nix/key.public
cat /etc/nix/key.public
```

The public key prints as `example-nix-cache-1:<base64>`.

Machines that read from the cache add its URL and public key in `nix.conf`:

```
substituters = https://cache.nixos.org/ s3://example-nix-cache
trusted-public-keys = cache.nixos.org-1:<key> example-nix-cache-1:<public-key>
```

Keep the default cache's own entries in both lists; the example above shows how to add yours beside them.

Machines that build for the cache also sign with the private key:

```
secret-key-files = /etc/nix/key.private
```

Restart the Nix daemon for changes to take effect.

## Checked

2026-11-04. Confirmed against the Nix manual page on the post-build hook: the `nix-store --generate-binary-cache-key` form, the `substituters` and `trusted-public-keys` lines, `secret-key-files`, and the daemon restart. Removed an unsourced key-permission gotcha and a verify line the page does not state.

Method: documentation only; no commands were run.
