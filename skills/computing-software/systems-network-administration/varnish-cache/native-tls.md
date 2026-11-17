---
id: computing-software.systems-network-administration.varnish-cache.native-tls
name: native-tls
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [native-tls, https-listener, tls-cert-load, tls-config-file]
level: practitioner
status: docs-checked
description: "Enable HTTPS in Varnish 9 natively, via a TLS config file (-A) or an HTTPS listener plus runtime tls.cert.load/commit, discard, rollback, reload, and backend .ssl."
sources:
  - https://www.varnish.org/docs/tutorials/tls/
  - https://www.varnish.org/docs/reference/varnish-cli/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# native tls

Native TLS exists as of Varnish 9, for client connections and for backends. Two ways to enable it.

Option 1, config file: `varnishd -a :80 -A /etc/varnish/tls.cfg` (the varnishd reference says -A loads the TLS configuration from the file). Example file:

```
frontend = {
    host = ""
    port = "443"
}
pem-file = "/etc/varnish/certs/mycert.pem"
```

`frontend` opens port 443 for all hosts and interfaces. Several `pem-file` entries are matched by SNI. `pem-file` may be a block with `cert`, `private-key` and `dhparam`. Other settings on the page: `ciphersuites`, `tls-protos` and `ecdh-curve`.

Option 2, HTTPS listener: `varnishd -a :80,http -a :443,https`. The -a protocols are http (default), https and proxy. A listener alone is not enough; load certificates with varnishadm:

```bash
varnishadm tls.cert.load /etc/varnish/cert.pem   # shows as staged in tls.cert.list
varnishadm tls.cert.commit                       # becomes active
```

Runtime changes work only with option 2, with no restart and the cache kept:

- `tls.cert.discard <id>` marks certificates as discard; ongoing sessions complete; `tls.cert.commit` removes them.
- `tls.cert.rollback` is the inverse of commit: it clears staged certs and turns discarded ones active again.
- `tls.cert.reload` atomically rereads all active certs with their current parameters and commits on success; on error everything is rolled back. It cannot run while there are staged or discarded changes.
- `tls.cert.list -s` shows only staged or discarded certificates.
- `tls.cert.load [cert-id] [-f frontend] [-k key-file] [-p protos] [-c TLS1.2-ciphers] [-s TLS1.3-ciphersuites] [-o] [-d]`: -f limits the cert to a frontend, -d marks the default fallback certificate, -o prefers the server's cipher order.

Persistence: loaded certificates are lost on varnishd restart. Put `start`, `tls.cert.load ...` and `tls.cert.commit` in a CLI file and pass it with `-I` (start must come first, to start the child).

Backend TLS: add `.ssl = 1;` to the backend definition (the page uses port 443).

## Checked

Method: 2026-11-08 docs-only read of the TLS tutorial; the tls.cert.* entries in the CLI reference and the -a, -A and -I entries in the varnishd reference were checked by search, not read in full. Corrections: -A is not a runtime-changeable setup (stated), added persistence via -I and backend .ssl which the earlier text lacked.
