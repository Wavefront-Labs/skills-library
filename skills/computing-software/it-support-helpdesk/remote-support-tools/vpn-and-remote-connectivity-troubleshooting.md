---
id: computing-software.it-support-helpdesk.remote-support-tools.vpn-and-remote-connectivity-troubleshooting
name: vpn-and-remote-connectivity-troubleshooting
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, vpn, split-tunnel, full-tunnel, dns-leak, always-on-vpn, certificate-authentication, ikev2, ssl-vpn, global-protect, anyconnect, latency, packet-loss, captive-portal, mfa]
level: practitioner
status: draft
description: "Diagnose VPN client issues: split vs full tunnel DNS behavior, certificate auth failures, always-on VPN reconnect loops, latency vs real outage, captive portal conflicts."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vpn-and-remote-connectivity-troubleshooting

Goal: separate "the VPN is broken" from "the thing behind the VPN is
slow/down", and know the handful of VPN-specific failure modes that look
like something else entirely.

## Split tunnel vs full tunnel — the single biggest source of confusion
- **Full tunnel**: all traffic, including general internet browsing,
  routes through the VPN. **Split tunnel**: only traffic to defined
  corporate ranges goes through the VPN; everything else uses the local
  internet connection directly.
- A user on split tunnel reporting "the internet is slow since I
  connected to VPN" is almost never a VPN problem — their general browsing
  never touches the VPN at all under split tunnel; look at their local
  ISP/Wi-Fi first.
- **DNS behavior is the classic split-tunnel gotcha**: even with split
  tunnel for traffic, DNS resolution can be configured to go either way
  — if DNS queries for internal names go to the public DNS server instead
  of the corporate resolver (or vice versa for public names), internal
  resources resolve to nothing (or public DNS leaks defeat the point of
  split tunnel). Check `nslookup <internal-hostname>` and
  `nslookup <public-hostname>` while connected to confirm each resolves
  via the expected server before assuming routing is broken.
- "Can't reach the internal file share but can reach the internet fine"
  on a split-tunnel VPN is a routing-table/ACL issue on the VPN side
  (the destination subnet isn't in the tunnel's route list), not a
  client fault — check the VPN concentrator's split-tunnel route
  definitions, this is often outside helpdesk's own console access and
  needs network-team escalation.

## Certificate-based authentication
- Cert-auth VPNs (IKEv2 with machine certs, or user certs for SSL VPN)
  fail silently with a generic "authentication failed" when the cert has
  **expired**, was issued to the wrong device after a reimage (new
  machine, old cert request), or the device clock is wrong enough to
  invalidate cert validity windows — check cert expiry and device time
  before assuming a credentials problem.
- A reimaged/reprovisioned device needs a *new* certificate enrollment
  (via the org's PKI/Intune cert profile) — the old cert doesn't
  transfer, and a user "it worked yesterday, now it doesn't" right after
  a reimage is explained by this, not a VPN server issue.

## Always-on VPN reconnect loops
- Always-on VPN (device-tunnel or user-tunnel, configured via Intune
  VPN profiles or GPO) should reconnect automatically on network change
  (Wi-Fi to Ethernet, sleep/wake) — a loop where it connects, drops, and
  reconnects repeatedly usually points to either an unstable underlying
  network (check Wi-Fi signal/roaming between APs) or a conflicting
  always-on profile left over from a previous VPN client that was
  supposed to be removed during a migration.
- Device-tunnel (machine-level, connects before user logon) vs
  user-tunnel (per logged-on user) have different failure signatures —
  a device-tunnel failure blocks things that need connectivity before
  login (like a cached-credential domain logon over VPN for a remote-
  first device); don't troubleshoot it with user-level diagnostics.

## Latency, packet loss, and "the VPN is slow" vs an actual outage
- Compare `ping`/`tracert` to the VPN gateway itself vs to a destination
  *behind* the VPN — high latency to the gateway but fine beyond it
  (once connected) points to the user's own internet path (home Wi-Fi,
  ISP congestion, satellite/4G backup links), not the corporate VPN
  infrastructure.
- A full VPN outage (nobody can connect) vs one user failing is a
  different escalation: check status dashboards/other users' reports
  before deep individual-machine troubleshooting — don't spend 30
  minutes on one laptop's VPN client when the concentrator itself is
  down for everyone.
- MTU mismatches over VPN show up as "small pages load, large file
  transfers/video calls stall" — a classic but easy-to-miss symptom;
  worth testing a lower MTU client-side as a diagnostic (not necessarily
  a permanent fix) before escalating as a mystery intermittent fault.

## Captive portals and conflicting network layers
- Hotel/airport/guest Wi-Fi captive portals block all traffic, including
  VPN negotiation, until the portal's own login page is accepted in a
  browser — a VPN client silently failing to connect on public Wi-Fi is
  frequently this, not a VPN bug; have the user open a plain browser tab
  first.
- Home routers with their own VPN pass-through settings, or a user's
  personal VPN/proxy service running simultaneously, can conflict with
  the corporate client — ask what else is running before deep client-side
  diagnosis on an otherwise-working setup.

## Gotchas
- MFA prompt not appearing on VPN connect is sometimes a cached/stale
  session token rather than an MFA outage — a full client restart (not
  just reconnect) often clears it.
- Corporate VPN client auto-update pushed mid-session can leave a stale
  running process holding the old network adapter — a reboot, not just
  client restart, clears genuinely stuck VPN virtual adapters.

## Verify
- Connects and resolves both internal and external hostnames to the
  expected resolver, routes to in-scope destinations only if split
  tunnel is intended (confirm with `tracert` to an out-of-scope public
  site showing it does NOT go through the tunnel), and holds the
  connection through a sleep/wake or network-switch cycle without
  manual reconnect.
