---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-preshared-keys-and-post-quantum
name: wireguard-preshared-keys-and-post-quantum
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [preshared-key, post-quantum, genpsk, noise-ikpsk2, symmetric-key, psk]
level: advanced
status: docs-checked
description: "Add a preshared key per peer pair for an extra symmetric layer, and understand its limits for post-quantum resistance."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html", "https://www.wireguard.com/known-limitations/", "https://www.wireguard.com/protocol/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preshared keys and post-quantum resistance

Out of the box WireGuard is not post-quantum secure. The optional per-peer preshared key (PSK) mixes an extra symmetric secret into the Noise_IKpsk2 handshake. Without one the PSK value used is 32 zero bytes.

```bash
umask 077
wg genpsk > psk-a-b
wg set wg0 peer PUBKEY preshared-key psk-a-b      # path to a file
```

or in the file: `PresharedKey = <base64>` inside the `[Peer]` section. Both ends must use the same value.

Remove with `wg set wg0 peer PUBKEY preshared-key /dev/null`.

Limits stated in the known-limitations page: the best bet for post-quantum security is to run a truly post-quantum handshake on top of WireGuard and insert that key into the preshared-key slot. Hashing the public keys is not part of the Noise Protocol Framework and would not give forward-secure post-quantum secrecy either.

`wg show wg0 preshared-keys` prints them (they are hidden in the pretty view unless `WG_HIDE_KEYS=never`).

Verify: change the PSK on only one side and confirm the handshake stops completing, then restore it.

## Checked

2026-11-03. Confirmed: Optional PSK for post-quantum resistance, genpsk, wg set preshared-key file path and /dev/null removal, the PresharedKey field, the all-zero PSK when unused, the known-limitations post-quantum text, and WG_HIDE_KEYS against the wg(8) man page, the protocol page and the known-limitations page. Removed: 'static so no forward secrecy by itself', 'rotate regularly' and 'different PSK per pair' (not in the docs).

Method: documentation only; no commands were run.
