---
id: computing-software.cryptography-implementation.openssl.openssl-ca-database-and-index
name: openssl-ca-database-and-index
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, private-ca, openssl-ca, ca-database, index-txt, serial-numbers, certificate-issuance]
level: advanced
status: docs-checked
description: "Run openssl ca's file database correctly: config keys, index.txt and serial files, policy sections, random serials, updatedb, backups and single-writer limits."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ca/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openssl ca database (index.txt, serial, crlnumber)

`openssl x509 -req` signs one CSR and forgets it. `openssl ca` keeps a text database of every issued
certificate and its status, which you need for revocation, CRLs and audits.

## Layout and config
The `database` file (mandatory) must exist, initially empty. The `serial` file (mandatory) holds the next serial in
hex. The `crlnumber` file holds the next CRL number; CRLs carry a number only if that file exists.
```
mkdir -p ca/{certs,newcerts,crl,private} && chmod 700 ca/private
touch ca/index.txt
echo 1000 > ca/serial && echo 1000 > ca/crlnumber
```
```
[ca]
default_ca = CA_default
[CA_default]
dir             = ./ca
database        = $dir/index.txt
serial          = $dir/serial
crlnumber       = $dir/crlnumber
new_certs_dir   = $dir/newcerts
certificate     = $dir/certs/issuing.pem
private_key     = $dir/private/issuing.key
default_md      = sha256
default_days    = 90
default_crl_days= 7
policy          = policy_strict
copy_extensions = copy
unique_subject  = no
email_in_dn     = no
[policy_strict]
countryName            = optional
organizationName       = match
commonName             = supplied
```
Issue: `openssl ca -config ca.cnf -extensions server -in r.csr -out out.pem -batch -rand_serial`
(`-rand_serial` generates a large random serial and overrides the serial file).

Policy values: `match` must equal the CA certificate's field, `supplied` must be present, `optional` may be present.
Request fields not named in the policy are silently deleted unless `-preserveDN` is used.
Use `copy_extensions = copy` rather than `copyall`: the man page warns that `copyall` can let a request smuggle in
unwanted extensions.

## Commands
```
openssl ca -config ca.cnf -status 4A3F...       # status of one serial
openssl ca -config ca.cnf -updatedb             # purge expired entries from the index
openssl ca -config ca.cnf -revoke cert.pem -crl_reason keyCompromise
openssl ca -config ca.cnf -gencrl -crldays 7 -out ca.crl
```

## Operating rules
- **Single writer.** No locking is done on the files; two concurrent `openssl ca` runs on one database can have
  unpredictable results. Run issuance from one host, serialised.
- The index is critical: if corrupted it can be hard to fix, and there is no option to rebuild it from issued
  certificates and a CRL. Back up `index.txt`, `serial`, `crlnumber` and the issued certificates with every change.
- `unique_subject` defaults to `yes`; set `no` to allow several valid certificates with the same subject (the man
  page recommends it for CA roll-over).
- The index is held in memory, which can be a problem with very large numbers of certificates.
- The man page says the command was meant as an example and is not production quality; keep signing keys on an HSM
  or smart card via a crypto provider. Delta CRLs are not supported.

## Verify
- [ ] Every certificate you can find in use has a row in `index.txt`.
- [ ] Serials are unique; backups of the database exist off-host.

## Checked

2026-11-01. Confirmed in the OpenSSL openssl-ca man page: config keys (`database`, `serial`, `crlnumber`, `new_certs_dir`, `certificate`, `private_key`, `default_md`, `default_days`, `default_crl_days`, `policy`, `copy_extensions`, `unique_subject`, `email_in_dn`), policy match/supplied/optional, `-rand_serial`, `-batch`, `-extensions`, `-status`, `-updatedb`, `-revoke`, `-crl_reason`, `-gencrl`, `-crldays`, `-preserveDN`, RESTRICTIONS, BUGS and WARNINGS (no locking, in-memory database, HSM advice, no delta CRLs). Removed: index.txt column layout, `index.txt.attr`, the 159-bit serial and CA/B Forum figures, the TXT_DB error text, alternative CA products.
Method: documentation only; no commands were run.
