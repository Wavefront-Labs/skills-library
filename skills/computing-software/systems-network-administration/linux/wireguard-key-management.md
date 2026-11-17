---
id: computing-software.systems-network-administration.linux.wireguard-key-management
name: wireguard-key-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, wireguard, wg-keygen, wireguard-keys, wg-genkey, wg-pubkey, wg-genpsk, preshared-key, key-rotation, peer-management, vpn, security, sysadmin]
level: practitioner
status: docs-checked
description: "Generate, store, distribute and rotate WireGuard keys: genkey/pubkey/genpsk with safe permissions, keeping private keys off the wire, PresharedKey use, live rotation and peer revocation."
sources:
  - https://man7.org/linux/man-pages/man8/wg.8.html
  - https://www.wireguard.com/quickstart/
  - https://man7.org/linux/man-pages/man8/wg-quick.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WireGuard key management

**Goal:** every peer's private key is generated where it is used, never copied around,
and you can add, rotate or revoke a peer without downtime for the others.

## 1. Generate (on the peer that will use it)
```bash
umask 077
wg genkey | tee /etc/wireguard/wg0.key | wg pubkey > /etc/wireguard/wg0.pub
wg genpsk > /etc/wireguard/peer-laptop.psk      # optional, one per peer pair
chmod 600 /etc/wireguard/*.key /etc/wireguard/*.psk
```
Keys are base64-encoded. Only the **public** key is exchanged. A preshared key (PSK) is optional and adds a layer of symmetric-key cryptography mixed into the public-key cryptography, for post-quantum resistance (wg(8)); share it per peer pair over an already-secure channel.

## 2. Keep private keys out of config files
```ini
[Interface]
PostUp = wg set %i private-key /etc/wireguard/wg0.key
```
or with systemd-networkd: `PrivateKeyFile=/etc/wireguard/wg0.key` in the `[WireGuard]` section of the `.netdev` (the file must be readable by `systemd-network`, for example owned by `root:systemd-network` with mode 0640). Config files then can go into git; key files never do.

## 3. Add, rotate, revoke peers live
```bash
wg set wg0 peer <PUBKEY> preshared-key /etc/wireguard/peer-laptop.psk allowed-ips 10.8.0.12/32
wg set wg0 peer <OLD_PUBKEY> remove          # revoke immediately
wg-quick save wg0                             # wg-quick subcommand that saves the current interface state to its config
wg show wg0 dump                              # machine-readable
```
Rotating a host's own key:
1. Generate the new pair on the host.
2. Plan the change window: remote peers must learn the host's new public key, and the host must switch to the new private key. A second interface with its own port and key can be used to migrate peers gradually before removing the old interface.
3. `wg set wg0 private-key /etc/wireguard/wg0.key.new` sets the new private key on the running interface (the argument is a file path); peers need the new public key to keep handshaking.

## 4. Inventory hygiene
- Keep a peer register (public key → owner, device, AllowedIPs, created date); WireGuard has no names, only keys.
- Lost/stolen device = remove its public key on every peer it was configured on.
- Do not reuse a key pair across devices.

## Verify
- [ ] Key files are owned by root with restrictive mode (600, or 640 with group `systemd-network`); config files contain no `PrivateKey` line if you use key files.
- [ ] `wg show wg0` lists only peers in the register; a removed peer no longer appears.

## Checked

Date: 2026-10-25. Documentation release: wg(8) and wg-quick(8) (WireGuard/wireguard-tools master), systemd.netdev(5) (PrivateKeyFile and permissions), WireGuard quickstart (wireguard.com), read 2026-10-25.
Confirmed: `wg genkey`, `wg pubkey`, `wg genpsk`, the `umask 077; wg genkey | tee ... | wg pubkey` recipe; `wg set ... private-key <file>`, `peer <key> remove`, `preshared-key <file>`, `allowed-ips`; `wg-quick save`; `PostUp` with `%i` expanded to the interface name; `PrivateKeyFile=` readable by systemd-network (0640 root:systemd-network).
Removed as unconfirmed: the Curve25519/44-character description, the "AllowedIPs cannot overlap" rotation constraint, the NetworkManager keyfile statement, the "no CRL" remark, dump field list, and the protocol page link.

Method: documentation only; no commands were run.
