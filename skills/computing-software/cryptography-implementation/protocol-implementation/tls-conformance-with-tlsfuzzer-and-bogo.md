---
id: computing-software.cryptography-implementation.protocol-implementation.tls-conformance-with-tlsfuzzer-and-bogo
name: tls-conformance-with-tlsfuzzer-and-bogo
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, protocol-conformance, tlsfuzzer, bogo, tls-anvil, tls-attacker, conformance-testing, rfc8446-compliance]
level: sme
status: docs-checked
description: "Test a TLS implementation for conformance and robustness with tlsfuzzer, the BoGo runner (BoringSSL PORTING.md) and TLS-Anvil: setup and reading results."
sources: ["https://github.com/tlsfuzzer/tlsfuzzer", "https://github.com/google/boringssl/blob/master/ssl/test/PORTING.md", "https://github.com/tls-attacker/TLS-Anvil"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS conformance with tlsfuzzer and BoGo

Use these suites when you build or modify a TLS stack, a TLS-terminating
proxy or an embedded TLS library. They check how the implementation reacts to
malformed and edge-case messages, not only what it negotiates.

## tlsfuzzer (README)

- A test suite for SSLv2 through TLS 1.3 implementations. It randomises
  inputs, but its scripts check that the system returned correct error
  messages, not just that it did not crash. API stability is not guaranteed.
- Needs Python and tlslite-ng (`pip install --pre tlslite-ng`; plain `tlslite`
  conflicts and will not work) plus ecdsa. Clone with
  `git clone https://github.com/tlsfuzzer/tlsfuzzer.git`.
- The server under test runs on localhost port 4433 and should answer HTTP
  queries. Run a script from `scripts/`, for example
  `scripts/test-invalid-compression-methods.py`. No printed errors means all
  expectations were met. Scripts accept `--help`, `-h` host and `-p` port.
- OpenSSL example server: `openssl s_server -key localhost.key -cert localhost.crt -www`.
- tlsfuzzer checks TLS-level behaviour only; it does not check certificate
  hostname, CA signatures or key usage.
- Scripts exist for ROBOT, DROWN and standards conformity (for example RFC
  5246, RFC 7627, RFC 7905). Timing side channels (Lucky13, padding oracle,
  timing-based Bleichenbacher) are covered in TIMING.md. USAGE.md explains
  interpreting failures.

## BoGo (BoringSSL ssl/test/PORTING.md)

- The runner drives the stack under test through a "shim": a command-line
  program wrapping the stack. Supply it with `-shim-path`. The shim connects to
  loopback as a TCP client on the `-port` given, sends its `-shim-id` as a
  64-bit little-endian integer, and exits 0 on success or non-zero on
  failure; many tests expect specific error strings.
- Support for non-BoringSSL stacks is described as a work in progress; pin to
  a particular revision rather than `main`.
- Config file via `-shim-config` with `DisabledTests` (pattern to reason,
  documentation only) and `ErrorMap` (runner error to your stack's string;
  `-loose-errors` maps unmapped errors to match anything).
- A shim exits with code 89 for unimplemented features (`-allow-unimplemented`
  stops that failing the whole run). Malloc-failure tests use `-malloc-test=0`
  and are slow (use `-timeout 72h`).

## TLS-Anvil

- Combinatorial-testing suite for RFC compliance of TLS libraries: around 408
  client and server tests for (D)TLS 1.2 and 1.3, based on RFCs including 8446.
- Run via the prebuilt Docker image `ghcr.io/tls-attacker/tlsanvil`; results
  can be viewed in Anvil Web.

## Verify

- [ ] Core tlsfuzzer scripts pass, or exclusions are documented.
- [ ] A conformance suite runs in CI for changes to TLS code.
- [ ] Disabled BoGo tests each carry a reason.

## Checked

Method: docs-checked 2026-11-09 against tlsfuzzer README, BoringSSL ssl/test/PORTING.md, TLS-Anvil README. Removed: the "by Red Hat" attribution, the named TLS 1.3 script list and `-e` / `--timing` options, the claim that BoGo is used by rustls, s2n and Go, the `-num-workers` flag, the claim that wrong alert type is minor while acceptance of invalid input is a security bug, and the rerun-against-OpenSSL advice.
