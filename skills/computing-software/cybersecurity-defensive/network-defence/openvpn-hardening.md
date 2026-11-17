---
id: computing-software.cybersecurity-defensive.network-defence.openvpn-hardening
name: openvpn-hardening
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [openvpn, openvpn-hardening, tls-crypt, easy-rsa, client-certificates, vpn-remote-access, data-ciphers]
level: practitioner
status: docs-checked
description: "Deploy and harden OpenVPN: PKI with Easy-RSA, tls-crypt, modern data ciphers, certificate plus MFA auth, revocation, per-client routes and server privilege dropping."
sources: ["https://openvpn.net/community-resources/reference-manual-for-openvpn-2-6/", "https://community.openvpn.net/openvpn/wiki/Hardening", "https://easy-rsa.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenVPN

## PKI (Easy-RSA 3)
```
./easyrsa init-pki && ./easyrsa build-ca
openvpn --genkey tls-crypt tc.key
```
Then issue one server certificate and one certificate per user/device with Easy-RSA (see its documentation
for the build commands). The OpenVPN Hardening wiki advises keeping the CA on a secure system with limited
login access, not running CA tasks as root, and generating private keys on the target system rather than
transporting them. It also says 2048-bit RSA is a good minimum (1024-bit is not sufficient) and that an
empty CRL should be set up from the start because OpenVPN needs a restart to add the option later (the wiki
page was last updated in 2016).
## Server (2.6)
```
port 1194
proto udp
dev tun
ca ca.crt
cert vpn1.crt
key vpn1.key
dh none                       # ECDH only
tls-crypt tc.key              # encrypts/authenticates control channel packets
tls-version-min 1.2           # default in 2.6.0 and later
data-ciphers AES-256-GCM:CHACHA20-POLY1305
remote-cert-tls client
crl-verify crl.pem
user nobody
group nogroup
persist-key
persist-tun
topology subnet
server 10.8.0.0 255.255.255.0
client-config-dir ccd          # per-client routes/fixed IPs
verb 3
```
Add MFA with an authentication plugin loaded with `--plugin` so a stolen client profile alone is
insufficient.

Notes from the 2.6 reference manual: `tls-crypt` hides the certificate used for the TLS connection and
makes OpenVPN traffic harder to identify, but all peers share one pre-shared key (no forward secrecy), so for
large setups or untrusted clients consider `tls-crypt-v2` with per-client keys. `dh none` needs peers whose
SSL library supports ECDH. The default `data-ciphers` list is AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305.
`remote-cert-tls client` makes the server require a peer certificate with TLS client key usage. Handshake
ciphers can be restricted with `tls-cipher` (TLS 1.2 and below) or `tls-ciphersuites` (TLS 1.3), but the
Hardening wiki warns that a mistaken list easily causes hard-to-debug failures, so only restrict it if you
can test every client.

## Revocation
`./easyrsa revoke alice && ./easyrsa gen-crl` then copy `crl.pem` to the server. The CRL file is read every
time a peer connects, so with `user` set make sure that user can read it. A missing CRL only logs a warning
and lets the connection through. The OpenVPN wiki has a page on expired CRLs; regenerate the CRL before it
expires.

## Gotchas
- `.ovpn` files with embedded keys are credentials; deliver securely and use passphrase-protected keys or MFA.
- `compress` and `comp-lzo` are deprecated and the manual says tunnels using compression are susceptible to the VORACLE attack; leave compression off.
- Firewall the tunnel network: VPN clients should reach only needed subnets (iptables/nftables on the server or upstream firewall).

## Verify
- [ ] Server log shows the negotiated data channel cipher and TLS version you expect.
- [ ] Revoked client is refused.
- [ ] A client without the tls-crypt key cannot complete a handshake.

## Checked
Checked 2026-11-09 against the OpenVPN 2.6 reference manual (genkey tls-crypt, tls-crypt, tls-crypt-v2, dh none, tls-version-min, tls-cipher and tls-ciphersuites, data-ciphers, remote-cert-tls, crl-verify, compress and comp-lzo deprecation, --user and --group, persist-key and persist-tun, topology, client-config-dir, plugin), the OpenVPN Hardening wiki (PKI practice, key size, tls-version-min, tls-cipher) and the Easy-RSA overview (init-pki, build-ca, revoke, gen-crl). Removed: the specific tls-cipher suite names, the build-server-full and build-client-full commands (not on the Easy-RSA page read), the PAM plugin file name, the Easy-RSA 180 day CRL default, the log line and port scan checks, and the claim that tls-crypt hides the server from scanners.
Method: docs-checked 2026-11-09 against the OpenVPN reference manual, Hardening wiki and Easy-RSA docs.
