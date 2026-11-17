---
id: computing-software.digital-privacy-hygiene.vpn-tools.self-hosted-wireguard-server-setup
name: self-hosted-wireguard-server-setup
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, wireguard, self-hosted-vpn, vps, iptables, nat, trust-model, wg-easy, allowedips, keepalive, cloud-vps-vpn]
level: advanced
status: draft
description: "Run your own WireGuard VPN server on a VPS: config generation, firewall/NAT rules, and the real trust trade-off (your cloud provider sees traffic) versus a commercial no-logs VPN."
sources:
  - "https://www.wireguard.com/quickstart/"
  - "https://github.com/wg-easy/wg-easy"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self-hosted WireGuard server setup

**Goal:** stand up your own VPN endpoint on a cheap VPS, for the specific case
where you want a single IP you control (bypassing geo-blocks tied to your home
IP, securing a specific set of devices on untrusted networks) — while
understanding exactly what trust you're moving, not eliminating, by doing it
yourself instead of using a commercial provider.

## 1. The trade-off this doesn't solve
`computing-software.digital-privacy-hygiene.vpn-tools.vpn-dns-and-tracker-blocking-setup`
section 1 notes a VPN moves trust from your ISP to the VPN provider — self-hosting
doesn't remove that trust, it moves it again, to your **cloud/VPS provider**
(DigitalOcean, Hetzner, AWS, etc.), who can see the same traffic pattern an ISP
could, and to **you**, who now has to secure the server correctly. The one real
advantage: you know for certain there's no "no-logs" marketing claim to verify,
because you control the box — but also no large anonymity set shared with
thousands of other users on the same exit IP, which is itself a de-anonymizing
factor since your traffic is clearly linked to a server that's clearly yours
(especially if the VPS is billed to you directly).

## 2. Minimum setup
- Provision a small VPS; **WireGuard** is in-kernel on modern Linux and
  extremely lightweight — a $5/month VPS handles a single user easily.
- Generate a key pair on the server (`wg genkey | tee privatekey | wg pubkey >
  publickey`) and one per client device; **never reuse a key pair across
  devices** — each device should have its own WireGuard identity so a single
  lost device's key can be revoked without affecting others.
- Server config (`/etc/wireguard/wg0.conf`): set `ListenPort`, the server's
  `Address` (a private range like `10.0.0.1/24`), and a `[Peer]` block per
  client with their public key and a unique `AllowedIPs` (e.g. `10.0.0.2/32`
  per device) — **don't** give every client the same internal address.
- Enable **IP forwarding** (`net.ipv4.ip_forward=1`) and add NAT/masquerade
  `iptables`/`nft` rules so client traffic routed through the tunnel reaches
  the internet via the VPS's own interface — this is the step people forget
  and then can't figure out why the tunnel connects but nothing loads.
- **wg-easy** (a Docker-based web UI wrapper) automates client config/QR-code
  generation if you don't want to hand-edit configs for every device — useful
  for a household rolling out several client devices.

## 3. Client config essentials
- `AllowedIPs = 0.0.0.0/0, ::1/0` on the client routes **all** traffic through
  the tunnel (full VPN); a narrower range routes only specific destinations
  (split tunneling) — decide deliberately per device/use case.
- `PersistentKeepalive = 25` on the client side if it's behind NAT (most
  phones/home routers are) — without it, the server may stop sending packets
  back through a NAT mapping that's timed out, making the tunnel look "up" but
  silently stop passing traffic.
- Set the client's `DNS` to a resolver you trust (not left as whatever the
  VPS's own default resolver is, which may log queries) — see
  `computing-software.digital-privacy-hygiene.vpn-tools.vpn-dns-and-tracker-blocking-setup`
  section 4 for picking one.

## 4. Firewall and exposure
- Restrict SSH to key-based auth only, change it off port 22 if you want to cut
  casual scanning noise (security theater against a targeted attacker, mild
  noise reduction against mass scanners), and allow only the WireGuard UDP
  port plus SSH inbound — nothing else needs to be open on a single-purpose
  VPN box.
- Keep the VPS patched; it's a full Linux box, not an appliance — the usual
  server-hardening basics apply and a neglected VPS is a worse outcome than
  not self-hosting at all.

## 5. When this is NOT the right tool
If the actual goal is hiding your traffic pattern within a large crowd of other
users (the core value proposition of a commercial VPN with thousands of
customers sharing exit IPs), a single-user self-hosted server defeats that —
your traffic is uniquely attributable to a server only you use. Self-hosting
fits "I want a consistent IP I control and I trust my own operational security
more than a vendor's," not "I want anonymity within a crowd."

## Gotchas
- Forgetting the NAT/masquerade rule is the most common "it connects but
  doesn't work" failure.
- A VPS billed with your real name/card directly links the server to you far
  more easily than a commercial VPN subscription would, if that distinction
  matters to your threat model.
- Uncertain: specific cloud providers' data-retention/logging practices for
  network traffic at the hypervisor level aren't something you control by
  self-hosting — check the provider's own policy if this matters.

## Verify
- [ ] Each client device has its own key pair and unique internal `AllowedIPs`.
- [ ] NAT/masquerade and IP forwarding confirmed working — test a client
      actually reaching the public internet through the tunnel, not just
      connecting.
- [ ] `PersistentKeepalive` set on any client behind NAT.
- [ ] Firewall allows only SSH and the WireGuard port; VPS OS kept patched.
- [ ] You've deliberately decided whether this fits your actual goal (control)
      vs. a commercial VPN's goal (anonymity within a crowd).
