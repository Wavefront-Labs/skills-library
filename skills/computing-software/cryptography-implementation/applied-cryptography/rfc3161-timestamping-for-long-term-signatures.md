---
id: computing-software.cryptography-implementation.applied-cryptography.rfc3161-timestamping-for-long-term-signatures
name: rfc3161-timestamping-for-long-term-signatures
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, rfc3161-timestamp, openssl-ts, timestamping, tsa, long-term-validation, code-signing, signature-validity]
level: practitioner
status: docs-checked
description: "Request and verify RFC 3161 timestamps with openssl ts and curl so signatures stay verifiable after certificate expiry or key revocation."
sources: ["https://www.rfc-editor.org/rfc/rfc3161", "https://docs.openssl.org/3.0/man1/openssl-ts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RFC 3161 timestamping for long-term signatures

A signature verified today proves nothing after the signer's certificate expires or is revoked, unless you can show
the signature existed before then. A trusted timestamp authority (TSA) signs a hash of the data together with a time.

## Request a timestamp
```
openssl ts -query -data artifact.bin -sha256 -cert -out req.tsq     # -cert asks the TSA to include its certificate
curl -sS -H "Content-Type: application/timestamp-query" --data-binary @req.tsq \
     <TSA_URL> -o resp.tsr
openssl ts -reply -in resp.tsr -text                                # inspect the TSTInfo fields
```
Without `-no_nonce`, openssl includes a 64-bit pseudo-random nonce in the request. Timestamp the signature value when
you need to prove a signature existed; timestamp the file when you just need proof of existence.

## Verify
```
openssl ts -verify -data artifact.bin -in resp.tsr -CAfile tsa-root.pem -untrusted tsa-chain.pem
# or against the query: openssl ts -verify -queryfile req.tsq -in resp.tsr -CAfile tsa-root.pem
```
Check: the TSA certificate has the `timeStamping` extended key usage marked critical (RFC 3161 requires it), the
imprint matches, and the TSA chain was valid at the time in the token.

## Gotchas
- Keep the nonce (do not pass `-no_nonce`) when replay of an old response is a concern; RFC 3161 says the response must
  echo the nonce if the request carried one.
- Keep the TSA chain and revocation data with the archive; online sources disappear.
- Check the TSA's policy and the hash algorithm it accepts before depending on it.

## Verify
- [ ] `openssl ts -verify` succeeds with the archived TSA chain offline.
- [ ] Signed releases carry a timestamp; verification still passes with the signing cert's validity in the past.

## Checked
2026-11-01. Confirmed in RFC 3161 (HTTP content types `application/timestamp-query` and `application/timestamp-reply`,
nonce echo rule, `id-kp-timeStamping` extended key usage MUST be critical) and the openssl-ts 3.0 manual (`-query`,
`-reply`, `-verify`, `-data`, `-cert`, `-no_nonce`, `-queryfile`, `-untrusted`, 64-bit nonce default, critical
timeStamping EKU). Removed: Authenticode/jarsigner/CAdES level/Sigstore claims, the SHA-1 statement and a named TSA
host (not checked against any page).
Method: documentation only; no commands were run.
