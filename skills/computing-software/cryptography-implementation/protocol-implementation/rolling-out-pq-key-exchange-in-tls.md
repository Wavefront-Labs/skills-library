---
id: computing-software.cryptography-implementation.protocol-implementation.rolling-out-pq-key-exchange-in-tls
name: rolling-out-pq-key-exchange-in-tls
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, post-quantum-migration, pq-tls, x25519mlkem768, tls-1-3, clienthello-size, middleboxes, rollout]
level: advanced
status: docs-checked
description: "Roll out hybrid post-quantum key exchange in TLS: X25519MLKEM768 sizes, ClientHello size and HelloRetryRequest breakage, and staged enablement."
sources: ["https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/", "https://tldr.fail/", "https://blog.cloudflare.com/pq-2024/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling out PQ key exchange in TLS

Store-then-decrypt attacks harvest encrypted traffic now to decrypt once
quantum computers exist, so key exchange is the urgent part of the migration
(tldr.fail). Authentication is less urgent, since it is checked in real time.

## The group (draft-ietf-tls-ecdhe-mlkem-03)

- X25519MLKEM768 is codepoint 4588 (0x11EC). The client key share is 1216
  bytes (1184 ML-KEM plus 32 X25519); the server share is 1120 bytes (1088
  ML-KEM plus 32 X25519); the shared secret is 64 bytes.
- The draft also defines SecP256r1MLKEM768 and SecP384r1MLKEM1024. For
  X25519MLKEM768 the ML-KEM secret goes first in the concatenation; for the
  P-256 and P-384 hybrids the ECDH secret goes first. That affects which part
  must come from a FIPS-certified implementation.

## Known breakage

- **Large ClientHello (tldr.fail):** post-quantum ClientHellos exceed the
  threshold for a single packet, so one TCP `read()` may not return the whole
  message. Buggy servers that cannot handle that reject the connection instead
  of negotiating classical cryptography. This is a bug even without post-quantum
  and is merely exposed more often. You can test by sending half a
  ClientHello, waiting, then sending the rest. QUIC deployments with a TCP
  race may mask the intolerance.
- **HelloRetryRequest (Cloudflare, 2024):** when testing origin connections,
  sending the post-quantum key share immediately (the fast way) broke 0.34%
  of connections, higher than browser failure rates; the safe way, where the
  origin asks via HelloRetryRequest, worked for all tested origins. Many
  failures were the large ClientHello; the majority came from servers not
  implementing HelloRetryRequest correctly. If the origin does not support it,
  fall back to traditional key agreement.

## Staged rollout

1. Enable in staging and run your client matrix.
2. Enable on a canary percentage and watch handshake failure rate and
   negotiated group.
3. Expand, keeping a switch to remove the group quickly.

## Verify

- [ ] Negotiated-group metric shows the hybrid for modern clients.
- [ ] No increase in handshake failures after canary.
- [ ] Servers in the path tolerate a ClientHello split across reads.

## Checked

Method: docs-checked 2026-11-09 against draft-ietf-tls-ecdhe-mlkem-03 (text), tldr.fail, Cloudflare blog "pq-2024". Removed: per-stack version lists (OpenSSL 3.5, Go 1.24, JDK 24, rustls), nginx and OpenSSL group config lines, the "~1.7 KB" ClientHello figure, the claim that inspection proxies strip PQ protection on the inner leg, the `openssl s_client -groups` check, and the nginx `$ssl_curve` logging tip.
