---
id: computing-software.cryptography-implementation.applied-cryptography.operating-in-fips-approved-mode
name: operating-in-fips-approved-mode
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, fips-140, fips-140-3, fips-approved-mode, service-indicator, openssl-fips, crypto-policies]
level: advanced
status: docs-checked
description: "Run software in FIPS 140-3 approved mode: enable it at OS and library level, use only approved services, and check service indicators so non-approved calls fail."
sources: ["https://docs.openssl.org/3.0/man7/fips_module/", "https://docs.openssl.org/master/man7/OSSL_PROVIDER-FIPS/", "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/switching-rhel-to-fips-mode_security-hardening"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operating in FIPS approved mode

A validated module only gives FIPS assurance when it is used **as the Security Policy says**:
approved algorithms, approved key sizes, approved modes, after self-tests pass. FIPS 140-3 also
requires an **approved service indicator** so a caller can tell whether a given service was
approved. Your job is to make non-approved use impossible or at least loud.

## OS level
- RHEL: `fips-mode-setup --enable` then reboot (it adds `fips=1` to the kernel command line); the
  docs also describe enabling FIPS at install time with `fips=1`. Check with `fips-mode-setup --check`;
  RHEL core crypto components use FIPS-approved implementations only when
  `/proc/sys/crypto/fips_enabled` contains 1.
- Other operating systems: follow the vendor's FIPS enablement guide and confirm the module's validation certificate.

## OpenSSL 3 FIPS provider
```
# openssl.cnf
openssl_conf = openssl_init
.include /usr/local/ssl/fipsmodule.cnf
[openssl_init]
providers = provider_sect
alg_section = algorithm_sect
[provider_sect]
fips = fips_sect
base = base_sect
[base_sect]
activate = 1
[algorithm_sect]
default_properties = fips=yes
```
- Load `base` alongside `fips` rather than `default`: `base` supplies non-cryptographic algorithms
  such as encoders and decoders, and `default_properties = fips=yes` makes fetches match only FIPS algorithms.
- Newer OpenSSL releases expose a FIPS service indicator; read the OSSL_PROVIDER-FIPS page for your
  release and log any call that relaxes an approved-mode check.

## What breaks in approved mode
- Algorithms, key sizes and modes that the module's Security Policy does not approve. Take the
  exact list for your module version from its Security Policy; it differs between modules.
- Expect fetches of non-approved algorithms to fail with "unsupported" errors; that is the intended outcome.

## Verify
- [ ] `fips_enabled`/policy flag is on in every environment that claims FIPS, including CI hosts.
- [ ] Only approved providers are loadable; a test that fetches a non-approved algorithm fails.
- [ ] The service indicator is checked in tests for each crypto entry point.

## Checked

- Date: 2026-11-02.
- Confirmed against: Red Hat RHEL security hardening guide (fips-mode-setup adds fips=1 and regenerates the initramfs, /proc/sys/crypto/fips_enabled semantics, fips=1 at install) and the OpenSSL 3.0 fips_module page (fipsmodule.cnf, provider sections, alg_section, default_properties = fips=yes, base provider loaded alongside fips).
- Removed: Ubuntu Pro, Windows registry, container, Go, Java and .NET lines, the OpenSSL 3.4 indicator parameter names, the EVP function names and the list of algorithms that break (none of these appeared in the fetched pages).

Method: documentation only; no commands were run.
