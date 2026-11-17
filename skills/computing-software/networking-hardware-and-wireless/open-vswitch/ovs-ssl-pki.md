---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovs-ssl-pki
name: ovs-ssl-pki
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovs-pki, ssl, tls, certificates, set-ssl, bootstrap, pki, fingerprint]
level: advanced
status: docs-checked
description: "Secure OpenFlow and OVSDB connections with ovs-pki: init a CA, req and sign certificates, self-sign, fingerprint, verify, ovs-vsctl set-ssl."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-pki.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovs-pki and SSL
Commands:
- `ovs-pki init` creates the PKI/CA.
- `ovs-pki req+sign ctl controller` makes and signs a certificate for a controller (use `switch` type for bridges).
- `ovs-pki self-sign sc` self-signs the request produced by `ovs-pki req sc` (some controllers accept self-signed certificates); `req` and `sign` do the two steps separately (run `req` on the switch or controller, `sign` on the CA machine).
- `ovs-pki fingerprint cert`, `ovs-pki verify cert type`.
Options: `-d dir` PKI dir (default /var/lib/openvswitch/pki unless changed at build time), `-f` force, `-b` batch (skips fingerprint verification), `-u` unique CN, `-k rsa|dsa` (default rsa), `-B bits` (minimum 1024, default 2048).

Point a switch at its files (use absolute paths):
`ovs-vsctl set-ssl /etc/openvswitch/sc-privkey.pem /etc/openvswitch/sc-cert.pem /etc/openvswitch/cacert.pem`
Then connect with `ovs-vsctl set-controller br0 ssl:IP:6653`. The SSL table holds `private_key`, `certificate`, `ca_cert`, `bootstrap_ca_cert`.

`ovs-vsctl --bootstrap set-ssl ...` lets the switch trust the CA on first connect, which exposes it to a man-in-the-middle on that connection.

Verify: `ovs-vsctl get-ssl` prints the SSL/TLS configuration.

Gotcha: the SSL files are read only once at ovs-vswitchd startup; if their contents change, ovs-vswitchd must be restarted.

## Checked
2026-11-09. Read in full: ovs-pki(8) (commands, options, defaults, self-sign, fingerprint is SHA-1) and the SSL/TLS and CA bootstrap sections of ovs-vsctl(8) (set-ssl, get-ssl, --bootstrap man-in-the-middle warning, default controller port 6653). Partial read of ovs-vswitchd.conf.db(5): SSL table columns private_key, certificate, ca_cert, bootstrap_ca_cert. Removed: the is_connected verify step and the relative-path claim (not in the sources); the absolute-path advice is kept only as a convention.
Method: documentation only; no commands were run.
