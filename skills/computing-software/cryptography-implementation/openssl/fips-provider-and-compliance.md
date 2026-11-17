---
id: computing-software.cryptography-implementation.openssl.fips-provider-and-compliance
name: fips-provider-and-compliance
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, fips-140, fips-provider, cmvp, self-tests, compliance, restricted-algorithms, openssl-3, fipsinstall, module-validation]
level: sme
status: docs-checked
description: "Activating and operating OpenSSL 3's FIPS provider: fipsinstall, self-test behavior, the restricted algorithm set, and the gap between 'FIPS-capable' and 'validated'."
sources: ["https://docs.openssl.org/master/man7/fips_module/", "https://docs.openssl.org/master/man5/fips_config/", "https://docs.openssl.org/master/man1/openssl-fipsinstall/", "https://csrc.nist.gov/projects/cryptographic-module-validation-program"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSL FIPS provider and compliance

A regulatory requirement to "use FIPS-validated cryptography" is a
narrower and more specific thing than "use OpenSSL." This skill covers the
gap between those two, specifically for OpenSSL 3's FIPS provider.

## "FIPS-capable" is not "FIPS-validated"

Only specific versions of the OpenSSL FIPS module appear on NIST CMVP certificates, and the module's security policy
states exactly which version and configuration were validated. The OpenSSL manual says that checking whether the default
configuration uses a validated module needs many additional checks and tells you to consult the security policy of the
module you use. Treat a build you made yourself as FIPS-capable until you can tie the exact binary to a certificate
number. If compliance sign-off is required, use a pre-validated build tied to a specific certificate, and confirm the
version and build against that certificate's security policy.

## Activating the provider: `fipsinstall` and config

1. `openssl fipsinstall -out fipsmodule.cnf -module
   /path/to/fips.so` — this generates a config file holding a MAC of the module file and a test-status indicator, and
   runs the known-answer self-tests (KATs) once at install time.
2. Reference that config file from `openssl.cnf`: `.include fipsmodule.cnf`, a `[provider_sect]` listing `fips = fips_sect`
   and `base = base_sect` (with `activate = 1` in `base_sect`), `config_diagnostics = 1` (recommended to catch
   mistaken configuration), and optionally `default_properties = fips=yes` in an `alg_section`. The manual's
   example is in fips_module(7).
3. **The module verifies its MAC (checksum) every time it is used.** The KATs normally run only once, at installation,
   unless `fipsinstall -self_test_onload` sets them up to run on each load. If a self test fails, the module enters an
   internal error mode and offers no algorithms. Treat a fipsinstall failure or a load-time failure as a hard stop, not
   something to work around by regenerating the config against a changed binary.

## The FIPS provider has a deliberately restricted algorithm set

The approved algorithm list differs by module version, so check the specific module's security policy for the exact
list rather than assuming. Practical fallout:
- Code written against `choosing-primitives-and-modes` guidance may need a **FIPS-compliant fallback algorithm
  selection path** when running under the FIPS provider, because not every modern primitive is on every certified
  module's approved list.
- Test your application's actual crypto call paths with the FIPS provider
  loaded, not just with `default` — a call to an unapproved algorithm under
  strict FIPS mode can fail at runtime in a way that never appears in
  normal (non-FIPS) testing, so FIPS-mode testing needs to be a distinct CI
  lane, not assumed to be covered by regular tests.

## Patching tension (cross-reference)

Changing the FIPS module binary can change its validation status. See
`computing-software.cryptography-implementation.crypto-libraries.dependency-and-cve-hygiene`
for the operational trade-off between patch-immediately and stay-validated, and take the rules for what can change
from NIST CMVP and the module's security policy (not covered by the OpenSSL manual pages).

## Verify

- [ ] The deployed FIPS provider binary is traceable to a specific CMVP
      certificate number, not a locally reproduced from-source build
      without that traceability.
- [ ] `fipsinstall` was run against the actual deployed module binary, and
      its self-test/integrity check passes on every environment (dev, CI,
      prod), not just one reference machine.
- [ ] A FIPS-mode CI lane actually exercises the application's crypto call
      paths with the FIPS provider loaded, confirming no call depends on a
      non-approved algorithm.
- [ ] Any gap between desired primitives (per
      `applied-cryptography.choosing-primitives-and-modes`) and the FIPS
      module's approved list has an explicit fallback decision, not a
      runtime surprise.
- [ ] Patch policy for the FIPS module aligns with current CMVP guidance.

The approved algorithm list and patching rules change as CMVP issues new guidance and certificates; verify against the
specific module's current security policy document rather than this summary. This skill is not compliance advice; the
authority is NIST CMVP and your auditor.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-fipsinstall(1), fips_config(5) and fips_module(7): `fipsinstall -out/-module/-self_test_onload`, the generated file holds a MAC of the module file and a test-status indicator, the MAC is verified on every use while KATs normally run once at install, the error mode on self-test failure, and the `.include`, `provider_sect`, `base_sect activate`, `config_diagnostics` and `default_properties = fips=yes` configuration. Corrected the earlier claim that self-tests re-run on every load. Removed unconfirmed statements about CMVP certificate contents, Ed25519/X25519 approval and NIST patch guidance, which are deferred to the CMVP site and the module security policy.

Method: documentation only; no commands were run.
