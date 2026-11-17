---
id: computing-software.cryptography-implementation.openssl.benchmarking-with-openssl-speed
name: benchmarking-with-openssl-speed
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, cipher-strings, openssl-speed, benchmarking, capacity-planning, evp, multi-threaded, ml-kem, rsa-performance]
level: practitioner
status: docs-checked
description: "Benchmark crypto throughput with openssl speed: -evp, -aead, -multi, -seconds and -bytes, and cautions when turning numbers into capacity estimates."
sources: ["https://docs.openssl.org/3.5/man1/openssl-speed/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking with openssl speed

`openssl speed` measures raw primitive throughput on the machine you run it
on. Use it to choose algorithms, size TLS terminators, and confirm hardware
acceleration is in use.

## Symmetric

```bash
openssl speed -evp aes-128-gcm -evp chacha20-poly1305 -seconds 3
openssl speed -evp aes-256-gcm -bytes 16384 -seconds 3   # one TLS-record-sized block
```

- `-evp algo` benchmarks a cipher or digest through the EVP interface; for an AEAD cipher add `-aead` to benchmark a TLS-like sequence.
- `-bytes N` benchmarks N-byte buffers (ciphers, digests and the CSPRNG); `-seconds N` sets the run time.

## Asymmetric

Pass algorithm names after the options (see the openssl-speed man page for the list your version accepts). Figures vary widely by CPU: measure yours, do not quote numbers from elsewhere.

## Multi-core

```bash
openssl speed -multi 4 -evp aes-128-gcm
```

## From numbers to capacity

A full TLS handshake on the server costs at least one signature (certificate key)
plus one key exchange, so benchmark both for the algorithms you deploy. Real servers
achieve less than the crypto-only figure (kernel, parsing, allocation).

## Gotchas

- Turbo boost and noisy neighbours distort results: run several times, pin
  CPU frequency for comparisons.
- Compare builds: `openssl version -a` shows the build settings.
- Benchmark the provider configuration you will deploy.

## Verify

- [ ] `-evp` used; results recorded with OpenSSL version and CPU model.
- [ ] Capacity estimate checked against a real load test of the TLS endpoint.

## Checked
2026-11-01. Confirmed in the openssl-speed man page: `-evp algo`, `-aead`, `-mb`, `-multi num`, `-seconds num`, `-bytes num`. Removed: asymmetric algorithm names (not listed on the page), all throughput and handshake figures, the 5-10x claim, 16 B to 16 KB block sizes, ML-KEM/ML-DSA speed names and the propquery claim.
Method: documentation only; no commands were run.
