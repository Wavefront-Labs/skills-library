---
id: computing-software.cryptography-implementation.secure-implementation.formal-protocol-analysis-with-tamarin-and-proverif
name: formal-protocol-analysis-with-tamarin-and-proverif
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, tamarin-prover, proverif, formal-verification, protocol-analysis, symbolic-model]
level: sme
status: draft
description: "Model and verify cryptographic protocols with Tamarin and ProVerif: writing rules and processes, secrecy and authentication lemmas, interpreting attacks, and scope limits."
sources: ["https://tamarin-prover.com/manual/master/book/", "https://bblanche.gitlabpages.inria.fr/proverif/", "https://eprint.iacr.org/2019/779"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formal protocol analysis with Tamarin and ProVerif

Symbolic (Dolev-Yao) tools explore all interleavings of an active network attacker controlling messages. They find
logic flaws: missing bindings, reflection, identity misbinding, downgrade.

## ProVerif
Applied pi calculus; automatic, fast, may report false attacks or not terminate.
```
free c: channel.
type key.
fun senc(bitstring, key): bitstring.
reduc forall m: bitstring, k: key; sdec(senc(m, k), k) = m.
free secret_msg: bitstring [private].
query attacker(secret_msg).
process new k: key; (out(c, senc(secret_msg, k)))
```
Queries: `attacker(x)` secrecy, `event(end(x)) ==> event(begin(x))` correspondence (authentication).

## Tamarin
Multiset rewriting rules and lemmas in first-order temporal logic; supports DH, bilinear pairings, XOR; can be
interactive. Used for TLS 1.3, 5G AKA, EMV, Signal/PQXDH, WPA2.
```
rule Send: [ Fr(~k), !Pk($B, pkB) ] --[ Secret(~k) ]-> [ Out(aenc(~k, pkB)) ]
lemma secrecy: "All k #i. Secret(k) @ i ==> not (Ex #j. K(k) @ j)"
```

## Workflow
1. Model the spec, not the code: messages, keys, compromise capabilities (long-term key reveal, session key reveal).
2. State properties: secrecy, forward secrecy, mutual authentication, agreement on transcript.
3. Run; for each attack trace, decide if it is a real flaw or a modelling artifact.
4. Iterate as the design changes; keep models in the repo.

## Limits
Symbolic models assume perfect primitives and ignore side channels, implementation bugs and computational
bounds. Pair with computational proofs (CryptoVerif, EasyCrypt) for high assurance.

## Verify
- [ ] Model checked into the repo with lemmas for each claimed property; CI runs it on changes.
