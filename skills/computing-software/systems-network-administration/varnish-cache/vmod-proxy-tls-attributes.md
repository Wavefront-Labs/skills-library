---
id: computing-software.systems-network-administration.varnish-cache.vmod-proxy-tls-attributes
name: vmod-proxy-tls-attributes
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vmod-proxy, proxy-protocol-v2, tlv-attributes, client-certificate]
level: advanced
status: docs-checked
description: "Read PROXY protocol v2 TLV attributes in VCL with vmod_proxy: alpn, authority (SNI), is_ssl, TLS version and cipher, client certificate fields and verify result."
sources:
  - https://www.varnish.org/docs/reference/vmod_proxy/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vmod proxy tls attributes

vmod_proxy extracts proxy-protocol-v2 TLV attributes. Use it when a TLS terminator in front sends the PROXY protocol: the varnishd reference says the `-a` PROXY protocol option accepts versions 1 and 2, e.g. `-a :8443,PROXY`. The VMOD documents only v2 TLVs, so use v2.

```vcl
import proxy;
sub vcl_recv {
    set req.http.alpn = proxy.alpn();
    set req.http.authority = proxy.authority();
    if (proxy.is_ssl()) {
        set req.http.ssl-version = proxy.ssl_version();
    }
    if (proxy.client_has_cert_sess() && proxy.ssl_verify_result() == 0) {
        set req.http.ssl-verify = "ok";
    }
}
```

All functions are restricted to the client context:

- `alpn()` returns the ALPN attribute; `authority()` the authority attribute, which corresponds to the SNI of the TLS connection.
- `is_ssl()` reports whether the PROXY v2 header has the SSL TLV.
- `ssl_version()`, `ssl_cipher()` return those attributes.
- `client_has_cert_sess()`: the client provided a certificate at least once over the TLS session; `client_has_cert_conn()`: over the current connection.
- `ssl_verify_result()` (INT) is SSL_get_verify_result; it matters only if `client_has_cert_sess()` is true, and defaults to 0 (X509_V_OK).
- `client_cert_cn()` is the client certificate's common name; `cert_sign()` the certificate signature algorithm; `cert_key()` the certificate key algorithm.

## Checked

Method: 2026-11-08 docs-only read of the vmod_proxy reference; the -a PROXY wording in the varnishd reference was checked by search. Removed unsupported side notes from the earlier text (`.proxy_header` on backends, `std.port(server.ip)`, native TLS in Varnish 9), none of which this VMOD page states.
