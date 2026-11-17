---
id: computing-software.cryptography-implementation.protocol-implementation.mtls-termination-at-proxies
name: mtls-termination-at-proxies
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, mutual-tls, mtls, mtls-termination, envoy, nginx, x-forwarded-client-cert]
level: practitioner
status: docs-checked
description: "Terminate mTLS at nginx or an AWS load balancer and pass the client identity on safely: header forwarding, stripping spoofed headers, and locking down the hop."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mTLS termination at proxies and header forwarding

When the proxy terminates mTLS, the backend learns the client identity only from headers the
proxy adds. The classic hole: the backend also accepts that header from anyone else.

## nginx
```nginx
ssl_client_certificate /etc/nginx/client-ca.pem;
ssl_verify_client on;
location / {
    proxy_set_header X-Client-Verify  $ssl_client_verify;       # verification result
    proxy_set_header X-Client-Cert    $ssl_client_escaped_cert; # urlencoded PEM
    proxy_set_header X-Client-S-DN    $ssl_client_s_dn;
    proxy_pass https://backend;
}
```
`proxy_set_header` replaces any client-supplied header of the same name, which is the stripping
you need. With `ssl_verify_client optional`, check `$ssl_client_verify = SUCCESS` before trusting anything.

## Cloud load balancers
- AWS ALB verify mode adds `X-Amzn-Mtls-Clientcert-Leaf` (URL-encoded PEM) plus `-Subject`, `-Issuer`,
  `-Serial-Number` and `-Validity` headers. Passthrough mode sends the whole chain in
  `X-Amzn-Mtls-Clientcert` without verifying it - your backend must validate the chain then.
- Envoy has its own client-certificate forwarding header (x-forwarded-client-cert) with sanitise/append modes; read its docs before relying on it.

## Backend rules
1. Accept those headers only on connections from the proxy: network policy / security group
   allows only the proxy, and ideally proxy -> backend is itself mTLS with the proxy's identity
   checked.
2. Parse the forwarded cert and authorise on the identity field (SAN URI/DNS), same rules as direct
   mTLS. Do not trust a DN string you cannot parse unambiguously (commas, escaping).
3. Fail closed when the header is missing or verify status is not SUCCESS.
4. Never log the full forwarded certificate chain on every request at info level; log identity and serial.

## Verify
- [ ] A request through the proxy with a forged client-cert header and no certificate is rejected, and the
      backend never sees the forged value.
- [ ] Direct connections to the backend (bypassing the proxy) are blocked at the network layer.
- [ ] Optional-verify paths check the verification status header.

## Checked
2026-11-01. Confirmed against the nginx ssl module page ($ssl_client_verify, $ssl_client_escaped_cert, ssl_verify_client) and the AWS ALB mutual authentication page (passthrough versus verify modes, X-Amzn-Mtls-Clientcert headers, passthrough does not verify). Removed: Envoy XFCC option details and RFC 9440 claim (pages unreadable).
Method: documentation only; no commands were run.
