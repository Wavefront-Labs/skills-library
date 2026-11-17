---
id: computing-software.systems-network-administration.dns-dhcp.oblivious-doh-odoh
name: oblivious-doh-odoh
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, odoh, oblivious-doh, dns-privacy, rfc9230]
level: practitioner
status: docs-checked
description: "Understand Oblivious DoH (RFC 9230, experimental): client/proxy/target roles, HPKE-encrypted queries, URI template, key configs, collusion assumption and stated limits."
sources:
  - https://www.rfc-editor.org/rfc/rfc9230
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oblivious DoH

Plain DoH hides queries from the network but the resolver sees both the client IP and the query. ODoH (RFC 9230, Experimental, not an Internet Standard) separates them:

- The **client** encrypts the DNS query to the **target**'s HPKE public key.
- The **proxy** (an HTTP server) forwards the encrypted message. It knows the client IP and the target but not the query.
- The **target** decrypts, resolves, and returns an encrypted response via the proxy. It sees the query but only the proxy's origin.

Only the client knows both. The threat model assumes proxy and target do not collude.

## Message flow
The proxy is identified by an HTTPS URI template that contains the variables `targethost` and `targetpath` exactly once and no others:
```
https://dnsproxy.example/dns-query{?targethost,targetpath}
```
Requests are HTTP POST with `Content-Type: application/oblivious-dns-message`. The mandatory HPKE suite is DHKEM(X25519, HKDF-SHA256), HKDF-SHA256, AES-128-GCM. Responses are encrypted with keys derived from the HPKE context plus a fresh nonce.

## Target keys
Public keys are carried in an `ObliviousDoHConfigs` structure (version 0x0001: KEM, KDF, AEAD IDs and key). The RFC says servers should rotate keys daily. How clients discover the configs is left out of scope, so check the target operator's documentation rather than assuming a well-known path or SVCB record.

## Rules and limits stated by the RFC
- Proxies must not forward client-identifying data (such as Forwarded headers); clients must not send cookies or similar state to proxies.
- Clients may include EDNS Client Subnet in the DNS message to get location-relevant answers without exposing their exact IP.
- Requests and responses are not cacheable.
- An on-path observer can tell the connection is oblivious DoH.
- Traffic-analysis mitigation is out of scope; padding is suggested (RFC 8467).
- Malicious proxies or targets are outside the threat model.

## Checked
Method: 2026-11-08 read RFC 9230 and kept only what it states. Removed as unsupported by it: Cloudflare, dnscrypt-proxy and odoh-server-go deployment specifics, the 10-50 ms latency figure, the claim that ECS is absent (the RFC allows it), well-known/SVCB key discovery, and enterprise-blocking advice. Cited blog and wiki pages were dropped from sources unread.

## Verify
- [ ] Your proxy URI template contains `targethost` and `targetpath` once each, and a test query returns a response through it.
