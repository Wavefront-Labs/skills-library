---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-key-generation
name: wireguard-key-generation
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wg-genkey, wg-pubkey, wg-genpsk, private-key, public-key, umask-077, key-management]
level: intro
status: docs-checked
description: "Generate WireGuard private, public and preshared keys with wg genkey, pubkey and genpsk, keeping files private."
sources: ["https://www.wireguard.com/quickstart/", "https://man7.org/linux/man-pages/man8/wg.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generating WireGuard keys

WireGuard uses base64-encoded Curve25519 keys, created by the `wg` utility. Restrict permissions first so the private key is never world-readable:

```bash
umask 077
wg genkey > privatekey
wg pubkey < privatekey > publickey
# or all at once:
wg genkey | tee privatekey | wg pubkey > publickey
# optional preshared key:
wg genpsk > psk-alice-bob
```

`genkey` prints a new private key; `pubkey` reads a private key on stdin and prints the matching public key; `genpsk` prints a random preshared key in base64. A public key is calculated from the private key and is the one usually transmitted out of band to the other side.

Passing keys to `wg set`: `private-key` and `preshared-key` must be file paths, because command-line arguments are not private on most systems. In bash you can pass a string without a file using process substitution: `private-key <(echo PRIVATEKEYSTRING)`. Giving `/dev/null` (or any empty file) removes the key from the device.

To keep private keys in encrypted form, the wg-quick man page shows loading one from pass with `PreUp = wg set %i private-key <(pass WireGuard/private-keys/%i)`.

The known-limitations page names rotating or regenerating keys as the mitigation for identity-hiding concerns (see wireguard-known-limitations).

Verify: `wg pubkey < privatekey` prints exactly the value you gave your peer.

## Checked

2026-11-03. Confirmed: Key generation commands, umask 077, base64 keys, process-substitution and /dev/null behaviour for private-key and preshared-key, and the pass PreUp example against the quick start and the wg(8) and wg-quick(8) man pages. Removed: the 32-byte genpsk claim, the per-pair PSK wording and the key-rotation procedure (not in the docs).

Method: documentation only; no commands were run.
