---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-ca-setup
name: openssl-ca-setup
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-ca-setup, pki-openssl-ca, openssl, openssl-ca, ca-database, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Lay out an openssl ca working directory: openssl.cnf, index.txt, serial, crlnumber, private dir and policy sections."
sources:
  - https://docs.openssl.org/master/man1/openssl-ca/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSL ca directory and config
Goal: a repeatable small CA you can operate by hand.
```
mkdir -p ca/{certs,crl,newcerts,private} && cd ca
touch index.txt; echo 1000 > serial; echo 1000 > crlnumber; chmod 700 private
```
`openssl.cnf` essentials:
```
[ ca ]
default_ca = CA_default
[ CA_default ]
dir = .
database = $dir/index.txt
serial = $dir/serial
crlnumber = $dir/crlnumber
new_certs_dir = $dir/newcerts
certificate = $dir/certs/ca.crt
private_key = $dir/private/ca.key
default_md = sha256
default_days = 90
default_crl_days = 30
policy = policy_strict
copy_extensions = none
unique_subject = no
[ policy_strict ]
countryName = supplied
organizationName = optional
commonName = supplied
```
- Keep one config per CA tier so extension sections cannot be mixed.
- `unique_subject = no` allows several valid database entries with the same subject (the default is `yes`); the manual recommends `no` to ease CA certificate roll-over.
- `copy_extensions = none` ignores extensions in the request; `serial` and `crlnumber` are text files holding the next number in hex.
- The policy section lists DN fields as `match`, `supplied` or `optional`; fields not mentioned are silently deleted.
- Back up `index.txt` and `serial`; they are the CA database.
Gotcha: `openssl ca` does no locking, so concurrent runs against one database give unpredictable results; the manual calls it a single-user command and warns it is not production quality, so keep the signing key in an HSM or smart card where you can.
Verify:
- [ ] `openssl ca -config openssl.cnf -status 1000` runs without errors.
- [ ] Private directory is 700 and the key is not world readable.

## Checked
2026-11-03. Confirmed in the openssl-ca manual page: `database`, `serial`, `crlnumber`, `new_certs_dir`, `certificate`, `private_key`, `default_md`, `default_days`, `default_crl_days`, `policy` (mandatory), `copy_extensions`, `unique_subject` (default yes, recommended no for roll-over), `-status serial`, the match/supplied/optional policy values, the no-locking and single-user warnings. Removed: the relative-`dir` second-database claim (not on the page). Fixed: the sample config put several settings on one line, which does not parse; `policy_strict` was undefined; `crlnumber` was missing from the config.
Method: documentation only; no commands were run.
