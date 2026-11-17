---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.certificate-sni
name: certificate-sni
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, certificate-entity, sni-entity, wildcard-sni, tls, snis]
level: practitioner
status: docs-checked
description: "Kong Certificate and SNI entities: cert, key and snis, creating them via /certificates/ and /snis/, wildcard positions and SNI match priority."
sources:
  - https://developer.konghq.com/gateway/entities/certificate/
  - https://developer.konghq.com/gateway/entities/sni/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificates and SNIs

**Certificate** fields: `cert` (PEM public certificate), `key` (optional PEM private key), `snis` (hostnames served; `"*"` is the SNI wildcard that assigns the Certificate across all SNIs).

```bash
curl -i -X POST http://localhost:8001/certificates/ \
  --header "Content-Type: application/json" \
  --data '{"cert": "<PEM_CERT>", "key": "<PEM_KEY>", "snis": ["example.com"]}'
```

**SNI** fields: `name` (hostname) and `certificate` (`{ "id": "<UUID>" }`).

```bash
curl -i -X POST http://localhost:8001/snis/ \
  --header "Content-Type: application/json" \
  --data '{"name": "example-sni", "certificate": {"id": "<CERT_ID>"}}'
```

Valid wildcard positions: `mydomain.*`, `*.mydomain.com`, `*.www.mydomain.com`.

Match order when resolving a handshake:
1. exact SNI
2. prefix wildcard
3. suffix wildcard
4. certificate for SNI `*`
5. default certificate on the file system

Certificates can also act as a trusted CA store when validating the peer certificate of a client or Service.

## Checked

2026-11-04. Confirmed against the Certificates and SNIs pages: TLS termination via SNI association, SNI wildcard "*", valid wildcard positions, the five-step match order, trusted CA store use. Removed cert_alt and key_alt, encryption at rest, required-field claims, the private-key rule and the ssl_cert name: the pages' schema sections are empty and do not state them.

Method: documentation only; no commands were run.
