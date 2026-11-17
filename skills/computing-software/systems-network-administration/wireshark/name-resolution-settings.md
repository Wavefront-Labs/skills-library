---
id: computing-software.systems-network-administration.wireshark.name-resolution-settings
name: name-resolution-settings
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, name-resolution, mac-name-resolution, transport-name-resolution, network-name-resolution, hosts-file, ethers, manuf, oui, dns-lookup, resolved-addresses, wireshark-profiles]
level: practitioner
status: verified
description: "Configure Wireshark name resolution without slowing analysis or leaking lookups: MAC OUI, port names, IP via capture-file DNS or a hosts file, and when to turn each off."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvNameResolutionSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name resolution settings

Preferences > Name Resolution (the `nameres.*` preferences). In tshark, `-n` disables resolution and `-N <flags>` enables only the listed types.

## Types
| Type | Default | Source |
|---|---|---|
| MAC (layer 2) | on (`nameres.mac_name: TRUE`) | ARP, `ethers`, then `manuf` OUI file: `00:50:56:aa:bb:cc` shows `VMware_aa:bb:cc` |
| Transport (ports) | **off** (`nameres.transport_name: FALSE`) | system port names: with `-N t` the SYN to port 80 printed `http(80)` and 40000 as `safetynetp(40000)` |
| Network (IP) | off (`nameres.network_name: FALSE`) | DNS packets in the capture, `hosts` files, optional active DNS lookups |
| VLAN IDs | off (`nameres.vlan_name: FALSE`) | `vlans` file |
Defaults are from `tshark -G defaultprefs` on 4.4.1; the man page says that with no `-n`/`-N` the preference values apply, which default to `-N dmN`.

## IP name resolution choices
- **Use captured DNS packet data** (`nameres.dns_pkt_addr_resolution: TRUE`; flag `d`): names from
  DNS answers inside the capture. Passive, accurate for that moment. Test: after a DNS answer `www.example.com A 1.2.3.4`, a later packet to
  1.2.3.4 gave `ip.dst_host = www.example.com` with `-N dn` and `1.2.3.4` with `-N d` (needs `n` as well) or `-n`.
- **Use an external network name resolver** (`nameres.use_external_name_resolver`, flag `N`; TRUE by default in 4.4.1 but "no effect without n"):
  the User's Guide says resolution is asynchronous in the GUI, DNS may add packets to your capture, and the observer effect applies;
  tshark's man page warns that in single-pass mode external lookups are performed synchronously. Lookups reveal the addresses you
  are analysing to the resolver (bad for incident response), so do not combine `n` with `N` on evidence.
- **hosts file**: the User's Guide says to add a `hosts` file to your personal configuration directory for known servers:
  ```
  10.0.0.53   dns1
  10.20.30.40 app-db-01
  ```
- `ethers` file maps MACs to names (e.g. gateways, firewalls).
The GUI's Resolved Addresses list has a CLI equivalent: `tshark -r cap -N dn -z hosts -q` printed `# TShark hosts output` and `1.2.3.4  www.example.com`.
`tshark -H hosts.txt -w out.pcapng` writes the hosts entries into the capture (man page); in a test reading that file back with `-N n` did not show
the names for `-e ip.dst_host`, so verify before relying on embedded names.

## When to turn things off
- Transport name resolution hides the real port (`http-alt` might be 8080 or 8008). Keep it off when documenting firewall rules (it is off by default).
- MAC resolution hides the full MAC that you need for switch MAC-table lookups. Use `eth.src` (always the address) instead of `eth.src_resolved`,
  or run with `-N` flags that omit `m`: `eth.src_resolved` printed `00:50:56:aa:bb:cc` with `-n` and `VMware_aa:bb:cc` with `-N m`.
- Shared/exported screenshots: names can reveal internal hostnames.

## tshark
```
tshark -r cap.pcapng -N dn -T fields -e ip.src_host -e ip.dst_host  # -N: d=captured DNS m=MAC n=network N=external resolvers t=transport v=VLAN s=SNI g=GeoIP
tshark -r cap.pcapng -n                                             # disable network object name resolution
```

## Verify
- [ ] External resolver off (no `N` flag); names still appear for hosts seen in DNS within the capture (`-N dn`).
- [ ] Names from your `hosts` file show for known servers in the Wireshark GUI (the CLI check above did not confirm the `-H` route).
