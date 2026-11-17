---
id: computing-software.systems-network-administration.dns-dhcp.kea-dhcpv6-prefix-delegation
name: kea-dhcpv6-prefix-delegation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcpv6, kea, kea-dhcp6, prefix-delegation, pd-pool, ia-pd, ia-na, duid, dhcpv6-relay, interface-id, rapid-commit, ra-flags, managed-flag, cpe]
level: advanced
status: verified
description: "Serve DHCPv6 with Kea: IA_NA address pools, IA_PD prefix delegation pools for CPE/branch routers, DUID-based reservations, relays and interface-id, and how RA M/O flags interact."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
  - https://datatracker.ietf.org/doc/html/rfc8415
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea DHCPv6 and prefix delegation

## Config
```json
"Dhcp6": {
  "interfaces-config": {"interfaces": ["eth1"]},
  "preferred-lifetime": 3000, "valid-lifetime": 4000, "renew-timer": 1000, "rebind-timer": 2000,
  "subnet6": [{
    "id": 20, "subnet": "2001:db8:20::/64", "interface": "eth1",
    "pools": [{"pool": "2001:db8:20::1000 - 2001:db8:20::ffff"}],
    "pd-pools": [{"prefix": "2001:db8:8000::", "prefix-len": 40, "delegated-len": 56}],
    "option-data": [{"name": "dns-servers", "data": "2001:db8::53"}],
    "reservations": [{"duid": "00:03:00:01:00:11:22:33:44:55", "ip-addresses": ["2001:db8:20::10"],
                      "prefixes": ["2001:db8:8001:100::/56"]}]
  }]
}
```
- **IA_NA** = addresses for hosts; **IA_PD** = prefixes for downstream routers (CPE, branch,
  container hosts). A /40 pool delegating /56s gives 2^(56-40) = 65,536 delegations.
- The requesting router then assigns /64s from its /56 to its LANs and sends RAs there.
- The upstream router must **route** delegated prefixes to the client: Kea only allocates prefixes
  and does not install routes. Options are a relay agent that installs routes for delegated
  prefixes (support varies by vendor: check yours), a routing protocol from the CPE, static
  routes per reservation, or scripts driven by lease events (for example the `run_script` hook).

## DUIDs
Clients are identified by DUID (+ IAID), not MAC: DUID-LLT (type 1, includes time), DUID-EN (2),
DUID-LL (3, MAC-based), DUID-UUID (4) (RFC 9915 table of DUID types). A reinstalled OS may
generate a new DUID. DHCPv6 has no reliable MAC, so Kea tries sources in order via the global
`mac-sources` list (default `any`, meaning all methods in sequence; others include `raw`, `duid`,
`ipv6-link-local`, `client-link-addr-option` (RFC 6939 relay option), `remote-id`, `subscriber-id`,
`docsis-cmts`, `docsis-modem`). Reservations by `hw-address` work only when one of these yields a MAC.

## Relays
For relayed clients Kea first matches the `link-address` of the RELAY_FORW message against subnets,
and can also use the relay's `interface-id` option (subnet `interface-id`) or a `relay`
`ip-addresses` list:
```json
{"subnet": "2001:db8:30::/64", "relay": {"ip-addresses": ["2001:db8:30::1"]}, ...}
```

## RA interplay
In RFC 4861 the RA **M** flag says addresses are available via DHCPv6 (and makes O redundant); **O**
says other configuration (DNS and so on) is available via DHCPv6. A router requesting PD does so by
its own configuration, not by these flags. Not every client implements DHCPv6 address requests
(IA_NA): confirm each client OS, and keep SLAAC (A=1) on client LANs if some cannot (see
dhcpv6-stateless-and-stateful-on-ios).

## Verify
- [ ] `lease6-get-all` shows IA_NA and IA_PD leases; delegated prefix routed and reachable.
- [ ] Reserved DUID receives its fixed address/prefix.
