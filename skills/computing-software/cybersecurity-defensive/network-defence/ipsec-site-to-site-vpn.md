---
id: computing-software.cybersecurity-defensive.network-defence.ipsec-site-to-site-vpn
name: ipsec-site-to-site-vpn
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [vpn, ipsec-vpn, ikev2, site-to-site-vpn, proposal-selection, pfs, dead-peer-detection, route-based-vpn, policy-based-vpn]
level: practitioner
status: docs-checked
description: "Configure secure IPsec site-to-site VPNs: IKEv2 with strong proposals and PFS, certificate or strong PSK auth, route-based design, and troubleshooting phase 1/2."
sources: ["https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html", "https://docs.strongswan.org/docs/latest/swanctl/swanctl.html", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-77r1.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPsec site-to-site VPN

**Goal:** encrypted tunnels between sites or to cloud networks that use strong cryptography and
are stable and debuggable.

## Crypto settings
Take the exact algorithm, DH group, PFS and lifetime choices from current NIST SP 800-77 Rev. 1
and your organisation's crypto policy (not restated here). General rules:
- Use IKEv2 only; strongSwan documents IKEv1 as deprecated, and `version = 2` is its default.
- Prefer certificates from a managed CA; if using PSKs, make them long, random and unique per peer.
- Enable PFS for Child SAs and match lifetimes and proposals on both ends.

## Route-based vs policy-based
Prefer **route-based** designs (routing decides what enters the tunnel) where your platform
supports them. Policy-based designs depend on traffic selectors matching exactly on both ends
and break when subnets change.

## Example (strongSwan swanctl.conf)
```
connections {
  site-b {
    version = 2
    proposals = <IKE_PROPOSAL>   # see the strongSwan cipher suite docs and NIST SP 800-77r1
    local { auth = pubkey  certs = site-a.pem  id = site-a.example.com }
    remote { auth = pubkey  id = site-b.example.com }
    remote_addrs = 203.0.113.10
    children {
      net { local_ts = 10.1.0.0/16  remote_ts = 10.2.0.0/16
            esp_proposals = <ESP_PROPOSAL>  dpd_action = restart  start_action = trap }
    }
  }
}
```

## Troubleshooting
- Phase 1 / IKE SA fails: proposal mismatch, wrong identity/PSK, blocked UDP traffic, NAT-T issues.
- Phase 2 fails: traffic selector mismatch (most common with policy-based), PFS group mismatch.
- Tunnel up, no traffic: routing, firewall policy on either side, MTU and TCP MSS clamping.
- strongSwan: `swanctl --list-sas` lists active IKE SAs; use your vendor's equivalent elsewhere.

## Gotchas
- Same PSK for all peers: one leaked config compromises every tunnel.
- VPN endpoints are prime exploitation targets: patch quickly and restrict management interfaces.
- Monitor every tunnel of a redundant pair, not just one.

## Verify
- [ ] Negotiated SA shows IKEv2, the intended algorithms and PFS.
- [ ] Alert when a tunnel goes down; failover tested.

## Checked
2026-11-01. Confirmed in the strongSwan swanctl.conf reference: `version` (IKEv1 deprecated, 2 default), `remote_ts`, `certs`, `id`, `dpd_action` values (clear, trap, restart) and `start_action` including trap; and the swanctl page (`--list-sas`). Removed: the algorithm/DH-group/lifetime table (NIST SP 800-77 Rev. 1 PDF text was not extractable in this batch), NSA and CompTIA citations, vendor show commands, MSS value, KEV claim, cloud two-tunnel claim, and the example proposal strings (replaced with placeholders).
Method: documentation only; no commands were run.
