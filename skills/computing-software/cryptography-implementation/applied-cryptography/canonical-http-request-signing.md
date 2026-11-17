---
id: computing-software.cryptography-implementation.applied-cryptography.canonical-http-request-signing
name: canonical-http-request-signing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, request-signing, http-message-signatures, rfc-9421, sigv4, aws-sigv4, content-digest, rfc-9530, hmac, canonicalization]
level: advanced
status: docs-checked
description: "Sign and verify HTTP requests with AWS SigV4-style canonical requests or RFC 9421 HTTP Message Signatures: covered components, digests, clock skew, replay."
sources: ["https://www.rfc-editor.org/rfc/rfc9421", "https://www.rfc-editor.org/rfc/rfc9530", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-create-signed-request.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canonical HTTP request signing

**Goal:** authenticate an HTTP request end to end so that method, path, query, selected headers and body cannot be
altered or replayed.

## Option 1: RFC 9421 HTTP Message Signatures (standard)
```
Content-Digest: sha-256=:X48E9qOokqqrvdts8nOJRJN3OWDUoyWxBf7kbu9DBPE=:
Signature-Input: sig1=("@method" "@target-uri" "content-digest" "content-type");created=1739890000;keyid="client-1";alg="ed25519"
Signature: sig1=:<base64 signature>:
```
- The verifier rebuilds the signature base from the listed components in order and checks with the key for `keyid`.
- Body integrity comes from `Content-Digest` (RFC 9530); always cover it for requests with bodies.
- Algorithms: `ed25519`, `ecdsa-p256-sha256`, `rsa-pss-sha512`, `hmac-sha256`. Bind the algorithm to the key on the
  server; never trust `alg` alone.

## Option 2: AWS SigV4 pattern (HMAC, widely copied)
```
CanonicalRequest = Method \n CanonicalURI \n CanonicalQuery \n CanonicalHeaders \n SignedHeaders \n hex(SHA256(body))
StringToSign     = "AWS4-HMAC-SHA256" \n AmzDate \n Date/Region/Service/aws4_request \n hex(SHA256(CanonicalRequest))
kSigning = HMAC(HMAC(HMAC(HMAC("AWS4"+secret, Date), Region), Service), "aws4_request")
Signature = hex(HMAC(kSigning, StringToSign))
```
The derived, scoped signing key limits damage if it leaks; the date in the scope bounds validity.

## Rules for any scheme
- Canonicalise precisely: URI-encode the path and query as the scheme specifies, sort query parameters by encoded
  name, lowercase and sort header names, trim leading and trailing header whitespace (the SigV4 rules). Most interop bugs are canonicalisation bugs.
- Include a timestamp and enforce a clock-skew tolerance you choose; add a nonce plus a replay cache
  for non-idempotent operations.
- Sign the `Host`/authority so requests cannot be redirected to another tenant.
- Verify before routing to business logic; compare MACs in constant time.

## Gotchas
- Proxies that rewrite headers (Host, Content-Length, Transfer-Encoding) break signatures; sign only headers that
  survive the path.
- Prefer the SDK's signer over hand-rolling SigV4.
- Old "draft-cavage" HTTP signatures differ from RFC 9421; do not mix.

## Verify
- [ ] Test vectors from RFC 9421 Appendix B verify.
- [ ] Changing method, path, any covered header or one body byte fails verification.
- [ ] A request replayed outside the skew window is rejected.

## Checked
2026-11-01. Confirmed in RFC 9421 (`Signature-Input`/`Signature` shape, `created`, `keyid`, `alg` values, Appendix B
examples, draft-cavage listed as a prior draft), RFC 9530 (`Content-Digest` example value) and the AWS IAM page on
creating a signed request (canonical request parts, `AWS4-HMAC-SHA256`, scoped signing key chain ending in
`aws4_request`, lowercase header names, sorted encoded query, trimmed header values). Removed: the 15-minute skew
figure and the path-encode-once wording (not on the page).
Method: documentation only; no commands were run.
