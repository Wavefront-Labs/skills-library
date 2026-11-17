---
id: computing-software.cryptography-implementation.applied-cryptography.sp800-90a-drbg-mechanisms
name: sp800-90a-drbg-mechanisms
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, random-generation, drbg, sp-800-90a, ctr-drbg, hmac-drbg, hash-drbg, reseed, prediction-resistance, openssl]
level: advanced
status: docs-checked
description: "Choose and operate an SP 800-90A DRBG: CTR, HMAC or Hash DRBG, reseed intervals, prediction resistance, personalisation, and OpenSSL 3's DRBG tree."
sources: ["https://csrc.nist.gov/pubs/sp/800/90/a/r1/final", "https://docs.openssl.org/3.0/man7/EVP_RAND/", "https://docs.openssl.org/3.0/man5/config/#random-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing and operating SP 800-90A DRBGs

Most applications should call the OS (`getrandom`, `BCryptGenRandom`) or
their crypto library's RNG. You meet DRBG choices when building a FIPS
module, configuring OpenSSL, or writing firmware.

## Mechanisms

SP 800-90A Rev. 1 specifies deterministic generators built on hash functions or block ciphers.
OpenSSL 3 offers three: CTR-DRBG (block cipher; `cipher` setting, default AES-256-CTR), HASH-DRBG and
HMAC-DRBG (both take a `digest` setting).

## Lifecycle

- **Instantiate** with entropy input from a trusted source; a personalisation
  string (device id, process id) separates instances.
- **Reseed** before the reseed counter reaches its limit. OpenSSL reseeds
  automatically when the DRBG is not yet seeded, after `reseed_interval` generate
  requests, or after `reseed_time_interval`; setting either to 0 disables that trigger.
- **Prediction resistance**: setting the prediction resistance parameter to 1 on
  `EVP_RAND_generate` forces a reseed from a live entropy source (SP 800-90C section 5.5.2);
  you must make sure such a source is configured. Request it for long-term keys.
- **Uninstantiate**: zeroise state.
- For per-request size limits, the reseed counter limit and the derivation-function rules,
  read the tables in SP 800-90A Rev. 1 itself.

## OpenSSL 3

OpenSSL has three shared DRBGs: a global `<primary>` that reseeds the others, and
per-thread `<public>` and `<private>` instances used by `RAND_bytes` and
`RAND_priv_bytes` respectively (use `priv` for keys). The CTR-DRBG cipher defaults to
AES-256-CTR, and the seed source defaults to SEED-SRC outside the FIPS provider.
Configure in `openssl.cnf`:

```ini
[openssl_init]
random = random_sect
[random_sect]
random = CTR-DRBG
cipher = AES-256-CTR
```

`RAND_add` with a positive randomness argument (or `RAND_seed`) immediately reseeds the
`<primary>` DRBG, so never feed it weak data.

## Pitfalls

- A DRBG is only as good as its seed: low entropy at boot breaks all output.
- Cloned state (fork, VM snapshot) repeats output; see the reseed skill.
- Implementing your own DRBG outside a validated module.

## Verify

- [ ] CAVP DRBG vectors pass if you implemented one.
- [ ] Key generation uses the private DRBG or prediction resistance.
- [ ] Seed source is documented and health-tested.

## Checked

2026-10-31. Confirmed in the OpenSSL 3.0 `EVP_RAND` page (primary/public/private DRBGs, automatic reseed triggers,
prediction resistance, `RAND_add` reseeding the primary) and `config` random section (CTR-DRBG, HASH-DRBG, HMAC-DRBG,
`cipher` default AES-256-CTR, `digest`, `seed` default SEED-SRC). The NIST page confirms Rev. 1 is based on hash
functions or block ciphers. Removed because the SP 800-90A text could not be read here (PDF not extractable): the
Dual_EC_DRBG removal, the 2^19-bit per-request limit, the 2^48 reseed limit, and the speed/simplicity comparisons.
Method: documentation only; no commands were run.
