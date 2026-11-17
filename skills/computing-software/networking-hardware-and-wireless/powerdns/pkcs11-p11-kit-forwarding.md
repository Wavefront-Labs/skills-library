---
id: computing-software.networking-hardware-and-wireless.powerdns.pkcs11-p11-kit-forwarding
name: pkcs11-p11-kit-forwarding
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pkcs11, p11-kit, forwarding, ssh, hsm, token]
level: advanced
status: docs-checked
description: "Forward a PKCS#11 token to PowerDNS with p11-kit server: module file, non-root server, SSH remote forwarding, pdnsutil hsm assign."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/pkcs11.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCS#11 token forwarding with p11-kit

Use this when the token is not on the DNS host. PKCS#11 support is experimental and needs `pkcs11=yes` since 5.2.0. `p11-kit server` cannot run as root; run it as a dedicated user in the `softhsm` group, and install `gnutls-bin` for `p11tool`.

1. Initialise the token, generate a key with `pkcs11-tool --keypairgen --key-type EC:prime256v1`, and list it.
2. Get the token URL from `p11tool --provider .../p11-kit-client.so --list-tokens`. It looks like `pkcs11:model=SoftHSM%20v2;manufacturer=SoftHSM%20project;serial=...;token=ecdsa%231`.
3. Create `/etc/pkcs11/modules/p11-kit-client.module` containing `module: /usr/lib/x86_64-linux-gnu/pkcs11/p11-kit-client.so`.
4. Start the server: `p11-kit server -u pdns --provider /usr/lib/x86_64-linux-gnu/softhsm/libsofthsm2.so "<token URL>"`. It prints `P11_KIT_SERVER_ADDRESS` and `P11_KIT_SERVER_PID`; export both.
5. Verify as the pdns user: `pkcs11-tool --module .../p11-kit-client.so -T`.
6. Assign: `pdnsutil hsm assign example.com ecdsa256 ksk p11-kit-client 'ecdsa#1' 1234 'my key'`, then `pdnsutil zone show example.com`.

Remote token over SSH, run from the token server:
```
ssh -R /var/run/pdns/pkcs11:${P11_KIT_SERVER_ADDRESS#*=} pdns@server
export P11_KIT_SERVER_ADDRESS=/var/run/pdns/pkcs11
```
then run the same `pkcs11-tool -T` and `pdnsutil hsm assign` commands on the DNS host.

## Checked

2026-11-08. Read in full: PowerDNS docs dnssec/pkcs11.rst (the SoftHSM2 with forwarding section is the basis; the build and setting notes come from the page opening). Confirmed the non-root and group requirement, gnutls-bin, the token URL step, the client module file, the server command and exported variables, the verify command, hsm assign arguments and the SSH remote forward. Added the experimental and pkcs11 setting note.

Method: documentation only; no commands were run.
