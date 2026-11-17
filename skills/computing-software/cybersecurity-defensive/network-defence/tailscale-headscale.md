---
id: computing-software.cybersecurity-defensive.network-defence.tailscale-headscale
name: tailscale-headscale
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [tailscale, headscale, mesh-vpn, wireguard, tailnet-acl, tailscale-ssh, vpn-remote-access]
level: practitioner
status: docs-checked
description: "Run a mesh VPN with Tailscale or Headscale securely: IdP auth, ACL policy and tags, device approval, key expiry, exit nodes and subnet routers, Tailscale SSH and logging."
sources: ["https://tailscale.com/kb/1018/acls", "https://tailscale.com/kb/1196/security-hardening", "https://headscale.net/stable/", "https://tailscale.com/kb/1226/tailnet-lock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mesh VPN with Tailscale or Headscale

WireGuard-based mesh: devices connect peer-to-peer; the coordination server (Tailscale SaaS or
self-hosted Headscale) distributes keys and policy.

## Identity and devices
- Authenticate through the corporate IdP (SSO with MFA); restrict tailnet to your domain.
- **Device approval** on so new devices need admin approval; **key expiry** on (default 180 days) for user devices; disable expiry only for tagged servers.
- **Tailnet Lock** so the coordination server cannot add nodes without signatures from trusted nodes (protects against coordination server compromise).

## ACLs (default allow-all must be replaced)
The policy file has `groups`, `tagOwners`, `acls` and `tests` sections (see the Tailscale ACL documentation for the exact syntax). Use `tests` so policy edits that break intent fail validation, and keep the policy in version control.

## Subnet routers and exit nodes
Subnet routers expose whole LANs - restrict who can reach advertised routes via ACLs and require route
approval. Exit nodes route all traffic - limit to specific groups.

## Logging
Enable network flow logs and configuration audit logs (Tailscale) and stream them to your SIEM; for Headscale collect the server logs.

## Gotchas
- Default policy allows everything between all devices; replace it on day one.
- Auth keys for servers: use tagged keys with short expiry; store them in a vault.

## Verify
- [ ] ACL tests pass; non-SRE user cannot reach prod SSH.
- [ ] Tailnet Lock enabled; new device requires signing.

## Checked

2026-10-28. Confirmed against: Tailscale docs: ACLs (policy file sections, tests), security best practices (device approval, key expiry 180 days default), Tailnet Lock; Headscale documentation (existence and scope).

Removed as unconfirmed: the full example policy JSON (autogroup and port-list syntax not confirmed), ephemeral/pre-approved key advice, posture integration remark, GitOps action name.

Method: documentation only; no commands were run.
