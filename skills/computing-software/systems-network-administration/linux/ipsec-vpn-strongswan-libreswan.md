---
id: computing-software.systems-network-administration.linux.ipsec-vpn-strongswan-libreswan
name: ipsec-vpn-strongswan-libreswan
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, strongswan, libreswan, ipsec, ikev2, swanctl, site-to-site-vpn]
level: practitioner
status: docs-checked
description: "Build IPsec IKEv2 site-to-site and road-warrior tunnels with strongSwan (swanctl) or Libreswan: configs, PSK vs certificates, firewall, and debugging failed negotiations."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlInitiate.html
  - https://docs.strongswan.org/docs/latest/config/logging.html
  - https://libreswan.org/man/ipsec.conf.5.html
  - https://libreswan.org/man/ipsec.8.html
  - https://datatracker.ietf.org/doc/html/rfc7296
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPsec with strongSwan and Libreswan

strongSwan and Libreswan are both IKEv2 implementations; crypto-policies (see the system-wide-crypto-policies skill) covers Libreswan. Match the IKE and ESP proposals to the peer.

## strongSwan site-to-site (swanctl)
Install the strongSwan swanctl tool and the charon-systemd daemon from your distro (package names vary).
```
# /etc/swanctl/conf.d/s2s.conf
connections {
  hq-dc {
    version = 2
    local_addrs = 203.0.113.10
    remote_addrs = 198.51.100.20
    proposals = aes256gcm16-prfsha384-ecp384
    local { auth = pubkey  certs = hq.crt  id = hq.example.com }
    remote { auth = pubkey  id = dc.example.com }
    children {
      net { local_ts = 10.1.0.0/16  remote_ts = 10.2.0.0/16
            esp_proposals = aes256gcm16-ecp384  start_action = trap  dpd_action = restart }
    }
  }
}
secrets { }   # PSK alternative: ike-1 { id = dc.example.com  secret = "<long random>" } with auth = psk
```
```bash
swanctl --load-all
swanctl --initiate --child net
swanctl --list-sas            # IKE and CHILD SAs, bytes in/out
```

## Libreswan site-to-site
```
# /etc/ipsec.d/hq-dc.conf
conn hq-dc
    keyexchange=ikev2
    left=203.0.113.10
    leftid=@hq.example.com
    leftsubnet=10.1.0.0/16
    leftcert=hq
    right=198.51.100.20
    rightid=@dc.example.com
    rightsubnet=10.2.0.0/16
    authby=rsasig
    ike=aes256-sha2;dh19
    esp=aes_gcm
    auto=start
```
```bash
ipsec initnss; ipsec import hq.p12     # certificates and keys live in the NSS database
systemctl enable --now ipsec
ipsec add hq-dc; ipsec up hq-dc         # auto=start already does both when Libreswan starts
ipsec trafficstatus; ipsec status
```

## Firewall and routing
- Allow UDP 500 and 4500 (IKE and NAT traversal, RFC 7296) and ESP (IP protocol 50) between the peers.
- Policy-based IPsec doesn't create a route; traffic matching the selectors is encrypted by XFRM policy (`ip xfrm policy`, `ip xfrm state`). Exclude tunnel traffic from NAT masquerade or it won't match.
- For route-based VPNs use XFRM interfaces (strongSwan `if_id_in/out`, Libreswan `ipsec-interface=`) and run BGP over them.

## Debugging
| Symptom | Likely cause |
|---|---|
| `NO_PROPOSAL_CHOSEN` | cipher/DH mismatch; align proposals with the peer |
| `AUTHENTICATION_FAILED` | ID mismatch (IP vs FQDN), wrong PSK, cert not trusted |
| `TS_UNACCEPTABLE` | traffic selectors (subnets) differ |
| SA up, no traffic | NAT rule catches packets, firewall drops ESP, missing return route |
Logs: charon-systemd logs to the journal by default (levels per subsystem are set in strongswan.conf; the default is 1, and `charon.filelog` sections can raise e.g. `ike = 2` and `knl = 2`); Libreswan logs for the `ipsec` unit appear in the journal too.

## Verify
- [ ] `swanctl --list-sas` / `ipsec trafficstatus` shows bytes increasing both ways.
- [ ] Ping between 10.1.x and 10.2.x works; `tcpdump -ni eth0 esp` shows ESP, not cleartext.

## Checked
Checked 2026-10-27 against the strongSwan documentation (swanctl.conf, swanctl --initiate, logging), the Libreswan ipsec.conf(5) and ipsec(8) manuals and RFC 7296.
- strongSwan: `start_action` (`none`, `trap`, ...), `dpd_action` (`clear`, `trap`, `restart`), `if_id_in`/`if_id_out`, `secrets.ike<suffix>` PSK sections, `swanctl --load-all`, `--list-sas`, `--initiate [--child <name>]`, `charon.filelog` sections with per-subsystem levels (e.g. `ike`, `knl`), charon-systemd logs to the journal.
- Libreswan: `keyexchange=ikev2` replaces `ikev2=yes|no|insist` (the earlier `ikev2=insist` was the old spelling), `auto=start` equals add plus up, `ipsec add`/`ipsec up`, `ipsec initnss`/`import`, `trafficstatus`, `ipsec-interface=` for route-based VPNs (`vti-interface` deprecated), `ike=...;dhNN` and `esp=aes_gcm` forms, `authby=rsasig`.
- RFC 7296 names NO_PROPOSAL_CHOSEN, AUTHENTICATION_FAILED and TS_UNACCEPTABLE notifications and the UDP 500/4500 ports.
- Removed unconfirmed claims: distro packaging statements, firewalld service name, NSS database path and `ipsec auto` commands, which do not appear in the current ipsec(8) manual.
Method: documentation only; no commands were run.
