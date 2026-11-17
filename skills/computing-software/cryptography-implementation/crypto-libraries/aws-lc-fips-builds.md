---
id: computing-software.cryptography-implementation.crypto-libraries.aws-lc-fips-builds
name: aws-lc-fips-builds
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, boringssl, aws-lc, aws-lc-rs, fips-140-3, fips-mode, rustls, cmake, golang-toolchain]
level: advanced
status: docs-checked
description: "Build and use AWS-LC and aws-lc-rs in FIPS mode: picking a validated module version, platform limits, checking FIPS mode at runtime, and where aws-lc-rs fits."
sources: ["https://github.com/aws/aws-lc/blob/main/crypto/fipsmodule/FIPS.md", "https://github.com/aws/aws-lc-rs", "https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search?SearchMode=Basic&ModuleName=AWS-LC"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS-LC and aws-lc-rs FIPS builds

AWS-LC is a general-purpose cryptographic library maintained by the AWS Cryptography team, based on code from
BoringSSL and OpenSSL. aws-lc-rs is a Rust library that strives to be API-compatible with `ring` (v0.16) and calls
AWS-LC through the `aws-lc-sys` or `aws-lc-fips-sys` FFI crates.

## Use a validated version

FIPS.md lists the validation certificates NIST has awarded to the AWS-LC FIPS module as a FIPS 140-3 level 1
cryptographic module, one per FIPS version and build type (static or dynamic library), plus newer versions that
are only "submitted" or "in review". A module that is merely submitted is not validated. Pick the FIPS version
and build type that holds a certificate, take its security policy as the build rule, and do not assume `main`
is the validated code. Look up current status on the NIST CMVP page (modules in process and validated lists) and
in FIPS.md; versions change.

The FIPS version number is independent of the AWS-LC release number and is incremented each time a new FIPS
branch is cut from mainline.

## Build (C)

Build in FIPS mode by following `crypto/fipsmodule/FIPS.md` and the security policy for the version you chose;
this skill does not repeat the CMake flags because they were not verified here. Platform limits stated in
FIPS.md:
- Static FIPS builds are supported only on Linux.
- Shared library FIPS builds are supported on Linux and Windows.
- Windows Debug builds are not supported with FIPS.
- Randomness uses CTR-DRBGs instantiated with AES-256; entropy comes from the operating system, which is not
  FIPS-validated.

## Runtime check

`FIPS_version()` (declared in `openssl/crypto.h`) returns 0 when AWS-LC is not built in FIPS mode, and
`FIPS_module_name()` returns "AWS-LC FIPS" in FIPS builds and "AWS-LC" otherwise. Assert one of these at startup.

## Rust (aws-lc-rs)

aws-lc-rs uses `aws-lc-fips-sys` for FIPS support, which provides bindings to AWS-LC-FIPS 3.x and uses the
static build on Linux targets. Read the aws-lc-rs README for the Cargo feature that selects it and for the
operating environments supported at your version. For rustls, check rustls's documentation for how it exposes a
FIPS provider and whether the resulting configuration reports itself as FIPS.

## Verify

- [ ] The FIPS version and build type you ship hold a NIST certificate, and the build follows its security policy.
- [ ] A startup assertion on `FIPS_version()` (C) fails the process in a non-FIPS build.
- [ ] Negotiated TLS cipher suites and algorithms are limited to those the security policy approves.

## Checked

2026-10-28. Confirmed against the AWS-LC FIPS.md, the AWS-LC README and the aws-lc-rs README: FIPS 140-3 level 1
certificates by version and build type, submitted-versus-validated wording, FIPS version independent of the
release number, platform limits, `FIPS_version()` and `FIPS_module_name()` behaviour, DRBG design, aws-lc-rs
ring compatibility and `aws-lc-fips-sys`. Removed (not on these pages or not verified): the `-DFIPS=1` build
commands, the `fips-YYYY-MM-DD` tag format, Go and Perl prerequisites, `FIPS_mode()`, power-on self-test
abort, the Cargo and rustls code and feature names, `ClientConfig::fips()`, s2n-tls, Python and Node and Go
remarks, and the default-rustls-provider claim.
Method: documentation only; no commands were run.
