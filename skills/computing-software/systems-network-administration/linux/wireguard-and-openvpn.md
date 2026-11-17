---
id: computing-software.systems-network-administration.linux.wireguard-and-openvpn
name: wireguard-and-openvpn
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, wireguard, wg-quick, openvpn, vpn, site-to-site, road-warrior, allowedips, persistent-keepalive, nat-traversal, ip-forward, masquerade, easy-rsa, tls-crypt, split-tunnel, networkmanager-vpn, systemd-networkd-wireguard, mtu, lpic-2, networking, security, sysadmin, openvpn-server, push-route]
level: practitioner
status: docs-checked
description: "Stand up WireGuard (preferred) or OpenVPN on Linux: peer config, wg-quick/networkd units, routing and NAT for road-warrior and site-to-site, Easy-RSA PKI, and the MTU/keepalive/AllowedIPs traps."
sources:
  - https://www.wireguard.com/quickstart/
  - https://github.com/WireGuard/wireguard-tools/blob/master/src/man/wg.8
  - https://github.com/WireGuard/wireguard-tools/blob/master/src/man/wg-quick.8
  - https://github.com/OpenVPN/openvpn/tree/release/2.6/doc/man-sections
  - https://github.com/OpenVPN/easy-rsa/blob/master/easyrsa3/easyrsa
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WireGuard and OpenVPN on Linux — tunnels that route the right traffic

**Goal:** an encrypted tunnel between hosts or sites with correct routing, NAT only
where needed, keepalives through NAT, and a config you can debug in two commands.

## 1. WireGuard (default choice: in the mainline kernel from 5.6, short config)
```bash
# install wireguard-tools with your distro's package manager (names vary); the kernel module is in mainline from 5.6
umask 077; wg genkey | tee server.key | wg pubkey > server.pub   # once per peer
```
Server `/etc/wireguard/wg0.conf`:
```ini
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <server.key>
PostUp   = nft add table ip wg; nft add chain ip wg post '{ type nat hook postrouting priority 100; }'; nft add rule ip wg post oifname "eth0" masquerade
PostDown = nft delete table ip wg

[Peer]   # laptop
PublicKey = <laptop.pub>
PresharedKey = <wg genpsk>           # optional extra symmetric-key layer for post-quantum resistance
AllowedIPs = 10.8.0.2/32

[Peer]   # branch office router (site-to-site)
PublicKey = <branch.pub>
AllowedIPs = 10.8.0.3/32, 192.168.50.0/24
```
Client:
```ini
[Interface]
Address = 10.8.0.2/24
PrivateKey = <laptop.key>
DNS = 10.8.0.1                       # wg-quick runs resolvconf -a for this; omit it and use PostUp/PostDown if you manage DNS another way
[Peer]
PublicKey = <server.pub>
Endpoint = vpn.example.com:51820
AllowedIPs = 10.8.0.0/24, 192.168.50.0/24   # split tunnel; 0.0.0.0/0, ::/0 = full tunnel
PersistentKeepalive = 25             # client behind NAT: keep the mapping open
```
```bash
sysctl -w net.ipv4.ip_forward=1       # persist in /etc/sysctl.d/ on the server
systemctl enable --now wg-quick@wg0
wg show                               # latest handshake, transfer; no handshake = key/endpoint/firewall
```
Allow the ListenPort (UDP) through the server firewall.
- **AllowedIPs is both a routing table and an ACL** (wg(8)): it lists the addresses from which incoming traffic for that peer is allowed and to which outgoing traffic is directed. On the server it says which source
  IPs a peer may send; on the client it says what goes into the tunnel. Give each peer distinct ranges.
- `wg-quick` infers routes from the peers' AllowedIPs; when one is a default route (`0.0.0.0/0` or `::/0`) it uses `ip rule` and fwmark handling to override the default gateway (`Table = off` disables route creation). Don't replicate that by hand.
- Site-to-site: both routers need `ip_forward=1`, no masquerade, and the LANs' default
  gateways must route the remote subnet to the WireGuard router (or run WG on the gateway).
- MTU: wg-quick determines it from the endpoint address or default route unless you set `MTU =`; if HTTPS hangs over a link with a smaller path MTU, set a lower `MTU` explicitly.
- Add peers live: `wg set wg0 peer <pub> allowed-ips 10.8.0.9/32` then `wg-quick save wg0` (or `SaveConfig = true`).
- Managed hosts: a `systemd-networkd` `.netdev` with `Kind=wireguard` and `[WireGuardPeer]` sections, or a NetworkManager `wireguard` connection, keep it under the normal
  network stack instead of wg-quick.

## 2. OpenVPN (when clients can't do WireGuard, or you need TCP/443, user/pass + certs)
```bash
# install openvpn and easy-rsa with your distro's package manager, then work in a copy of the Easy-RSA directory
./easyrsa init-pki && ./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
./easyrsa build-client-full laptop nopass
./easyrsa gen-dh; openvpn --genkey secret ta.key          # tls-crypt key ("tls-crypt" is an alias of "secret")
```
`/etc/openvpn/server/server.conf`:
```
port 1194
proto udp               # use tcp-server (clients: tcp-client) only when UDP is blocked
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem               # "dh none" uses ECDH only
tls-crypt ta.key        # encrypts and authenticates all control channel packets
server 10.9.0.0 255.255.255.0
push "route 192.168.10.0 255.255.255.0"
push "dhcp-option DNS 10.9.0.1"
# push "redirect-gateway def1 bypass-dhcp"   # full tunnel
client-to-client
keepalive 10 60
data-ciphers AES-256-GCM:CHACHA20-POLY1305   # the old "cipher" option should no longer be used in TLS mode
auth SHA256
user nobody
group <unprivileged group>   # group name is distro-specific
persist-key
persist-tun
verb 3
crl-verify crl.pem      # after ./easyrsa gen-crl; revoke with ./easyrsa revoke laptop
```
Start the server with your package's unit (for example `openvpn-server@server`); allow 1194/udp and add masquerade as for
WireGuard. Clients get a `.ovpn` with inline `<ca>`, `<cert>`, `<key>`, `<tls-crypt>` blocks
and `remote vpn.example.com 1194 udp`; `explicit-exit-notify` is a client option (UDP). `dhcp-option DNS` pushes are only exported to the client's environment: a plugin or `--up` script must apply them on Linux. Username/password on top of certs:
`plugin <path to openvpn-plugin-auth-pam.so> login` + `auth-user-pass` on clients.

## 3. Debugging both
```bash
wg show wg0; journalctl -u wg-quick@wg0
tcpdump -ni eth0 udp port 51820            # are packets arriving at all?
ip route get 192.168.50.10                 # does the route point into the tunnel?
tcpdump -ni wg0                            # decrypted traffic enters here: shows reply routing problems
journalctl -u openvpn-server@server -f     # unit name per your package; TLS negotiation failures usually mean a blocked port or a tls-crypt key mismatch
```
- Handshake OK, no traffic: `ip_forward`, missing masquerade/return route on the LAN, or
  the client's AllowedIPs excludes the destination.
- Works for ping but not for web: MTU. Lower it 40 bytes at a time.
- Peers behind CGNAT need `PersistentKeepalive`; a server behind NAT needs a port forward.

## Verify
- [ ] `wg show` lists a handshake within the last 2 minutes for each peer and transfer counters rising.
- [ ] From the client: `ping 10.8.0.1`, then a LAN host behind the server, then (full tunnel) `curl ifconfig.me` returns the server's IP.
- [ ] Reboot both ends; the tunnel comes back without intervention.

## Checked
Checked 2026-10-27 against the wireguard-tools man page sources (wg.8, wg-quick.8), wireguard.com/install, the systemd.netdev and nmcli manual sources, the OpenVPN 2.6 manual sources (github.com/OpenVPN/openvpn, release/2.6, doc/man-sections) and the Easy-RSA 3 script and docs.
- wg(8): `genkey`, `genpsk`, `pubkey`; AllowedIPs semantics (incoming allowed, outgoing directed); PresharedKey is an extra symmetric layer for post-quantum resistance; PersistentKeepalive 1-65535 seconds.
- wg-quick(8): `up`/`down`/`save`/`strip`; DNS runs `resolvconf -a`; MTU is auto-determined unless set (there is no fixed 1420 default); routes inferred from AllowedIPs, default routes handled with `ip rule`; `Table`, `PostUp`, `SaveConfig`.
- WireGuard is in the mainline kernel from 5.6 (wireguard.com/install); systemd.netdev has `Kind=wireguard` and `[WireGuardPeer]`; nmcli lists a `wireguard` connection type.
- OpenVPN 2.6: `--genkey secret` with `tls-crypt` alias, `--tls-crypt`, `--data-ciphers`, `--auth` (default SHA1), `--dh none`, `--keepalive`, `--client-to-client`, `--crl-verify`, `--push`, `redirect-gateway def1`, `--plugin`, `--user`/`--group`; the `--cipher` option should not be used in TLS mode; `--explicit-exit-notify` is a client (UDP) option; `dhcp-option` values need a plugin or `--up` script on Linux.
- Easy-RSA: `init-pki`, `build-ca`, `build-server-full`, `build-client-full`, `gen-dh`, `gen-crl`, `revoke`, and the `nopass` option.
- Removed unconfirmed claims: default MTU 1420 and the 1380 figure, last-wins AllowedIPs overlap behaviour, `nmcli import` for WireGuard, firewalld commands, `make-cadir`, TCP-over-TCP wording, SELinux label, distro package names and the invalid server-side `explicit-exit-notify`.
Method: documentation only; no commands were run.
