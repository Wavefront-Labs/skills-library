---
id: computing-software.networking-hardware-and-wireless.haproxy.tls-runtime-certificate-updates
name: tls-runtime-certificate-updates
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, set-ssl-cert, commit-ssl-cert, runtime-certificate-update, show-ssl-cert]
level: practitioner
status: docs-checked
description: "Replace or add a TLS certificate in a running HAProxy through the runtime API: set ssl cert, commit ssl cert, abort, new ssl cert and add ssl crt-list."
sources:
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls runtime certificate updates
Certificates can be changed over the stats socket as a transaction. The transaction system works on any certificate listed by `show ssl cert`, frontend or backend.

```
echo -e "set ssl cert localhost.pem <<\n$(cat 127.0.0.1.pem)\n" | socat /var/run/haproxy.stat -
echo "commit ssl cert localhost.pem" | socat /var/run/haproxy.stat -
```
- `set ssl cert <filename> <payload>`: with no transaction in progress it duplicates the certificate in memory into a temporary transaction and updates it from the PEM payload; with one in progress it updates that transaction. It can also update the linked files (`.issuer`, `.sctl`, `.ocsp` and so on), for example `set ssl cert localhost.pem.issuer <<` or the base64 of the OCSP response for `localhost.pem.ocsp`.
- The payload ends at the first empty line, so inject a sanitised PEM with no empty lines. The manual's example strips empty lines with `sed -n '/^$/d;/-BEGIN/,/-END/p'`.
- `commit ssl cert <filename>`: for an existing certificate in `Used` state it generates the SSL contexts and SNIs, inserts them, removes the old ones and replaces the certificate in memory everywhere it was used. On failure nothing is removed or inserted. After commit the transaction is destroyed.
- `abort ssl cert <filename>` destroys the pending transaction.
- New certificate: `new ssl cert <filename>` creates an empty store, then `set ssl cert` and `commit ssl cert`. The certificate then shows `Unused` and is not used anywhere until added with `add ssl crt-list <crtlist> <certificate>`. That command loads it on every bind line using the crt-list (directories are loaded the same way). To give SSL options or filters, pass a crt-list line as a payload, only one line allowed: `add ssl crt-list certlist1 <<` then `foobar.pem [allow-0rtt] foo.bar.com !test1.com`.
- `show ssl cert [<filename>]` lists certificates and shows `Status` (`Used` or `Unused`), `Serial`, `notBefore`, `notAfter`, issuer, subject and fingerprint for one. A filename prefixed with an asterisk is an uncommitted transaction. Suffix `.ocsp` shows the OCSP response details.
- The commands work through the master CLI too, prefixed with a worker selector, for example `echo "@1 show ssl cert" | socat /var/run/haproxy.master -`.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 management guide: `set ssl cert`, `commit ssl cert`, `abort ssl cert`, `new ssl cert`, `add ssl crt-list` and `show ssl cert` entries with their examples, and the section 9.3 payload description. Removed: version claims (2.1 and 2.2), the `level admin` requirement, the advice to also update the file on disk, the Let's Encrypt deploy-hook remark, the claim that a mismatched key blocks later `set` until aborted, and the `openssl s_client` verification. Only the cited command entries of the management guide were read, not the whole document.
Method: documentation only; no commands were run.
