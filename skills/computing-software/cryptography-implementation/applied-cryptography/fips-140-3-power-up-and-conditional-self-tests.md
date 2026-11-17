---
id: computing-software.cryptography-implementation.applied-cryptography.fips-140-3-power-up-and-conditional-self-tests
name: fips-140-3-power-up-and-conditional-self-tests
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, fips-140, fips-140-3, fips-self-tests, known-answer-test, pairwise-consistency-test, error-state]
level: advanced
status: draft
description: "Handle FIPS 140-3 pre-operational and conditional self-tests: integrity check, CASTs, pairwise consistency tests, error state, and how to test failure paths."
sources: ["https://csrc.nist.gov/pubs/fips/140-3/final", "https://docs.openssl.org/master/man1/openssl-fipsinstall/", "https://docs.openssl.org/master/man3/OSSL_SELF_TEST_set_callback/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FIPS 140-3 power-up and conditional self-tests

ISO 19790 section 7.10 defines the tests a validated module runs. Integrators need to know which
ones can fail at runtime, what the module does then, and how the application must react.

## Pre-operational self-tests (before the module offers any service)
- **Software/firmware integrity test**: an approved MAC or signature over the module image
  (OpenSSL's FIPS provider checks an HMAC-SHA-256 recorded in `fipsmodule.cnf`).
- **Pre-operational bypass test** (modules with a bypass capability) and critical functions test.
- FIPS 140-3 lets a module run each **CAST** (cryptographic algorithm self-test, usually a
  known-answer test) before the first use of that algorithm instead of all at load; OpenSSL 3.x
  runs its KATs when the provider is first loaded.

## Conditional self-tests
- **CAST** before first use of an algorithm, if not done at load.
- **Pairwise consistency test (PCT)** on every asymmetric key generation: sign/verify or
  encrypt/decrypt with the new pair; a failure discards the key and enters the error state.
  PCTs make RSA/ML-DSA key generation measurably slower; do not "optimise" around them.
- Software/firmware load test, manual entry test, conditional bypass test where applicable.
- **Continuous entropy-source health tests** (SP 800-90B repetition count, adaptive proportion)
  inside the entropy source.

## Error state
On any self-test failure the module enters an error state and must not output data through
the data output interface. In OpenSSL the provider becomes unusable: every fetch/operation fails
and `ERR_get_error` reports a self-test or "module in error state" reason. The process must be
restarted; there is no API to clear it. Application rule: treat it as fatal, alert, and exit.
Never fall back to a non-FIPS provider.

## Observing and testing self-tests (OpenSSL 3)
```
openssl fipsinstall -out fipsmodule.cnf -module "$MODULESDIR/fips.so"   # runs all KATs
openssl fipsinstall -module "$MODULESDIR/fips.so" -in fipsmodule.cnf -verify
# deliberately corrupt one test to prove your error handling:
openssl fipsinstall -out /tmp/bad.cnf -module "$MODULESDIR/fips.so" \
   -corrupt_desc "SHA2" -corrupt_type "KAT_Digest"
```
- `OSSL_SELF_TEST_set_callback(libctx, cb, arg)` reports each test's phase (`Start`, `Pass`,
  `Fail`, `Corrupt`), type and description; log `Fail` and stop.
- Rebuilding or patching `fips.so` invalidates the integrity MAC. Regenerating `fipsmodule.cnf`
  against a modified binary makes the check pass but leaves you outside the validated module.
- Generate `fipsmodule.cnf` on each target machine or at image build from the shipped binary,
  per the security policy of your OpenSSL FIPS release.

## On-demand self-tests
The module must allow periodic self-tests on demand (often by reloading the provider or a
dedicated service). Long-running daemons in regulated environments sometimes schedule a restart
or a provider reload for this.

## Verify
- [ ] A forced self-test failure (corrupt option or tampered config) makes the service exit with a clear alert.
- [ ] Startup logs record self-test pass and module version.
- [ ] No code path catches crypto failures and retries with a different provider.
