---
id: computing-software.cryptography-implementation.openssl.listing-algorithms-and-capabilities
name: listing-algorithms-and-capabilities
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-cnf, providers, openssl-list, openssl-version, cipher-list, capabilities]
level: practitioner
status: docs-checked
description: "Find out what an OpenSSL build can do: openssl version -a, list -providers/-cipher-algorithms/-kem-algorithms and more, ciphers -v, and checking for PQC and FIPS support."
sources: ["https://docs.openssl.org/3.0/man1/openssl-list/", "https://docs.openssl.org/3.0/man1/openssl-ciphers/", "https://docs.openssl.org/3.0/man1/openssl-version/", "https://docs.openssl.org/3.0/man1/openssl-info/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing algorithms and capabilities

Before debugging "unsupported algorithm", confirm what the OpenSSL in front of you actually
contains. Several copies on one machine are normal.

## Which OpenSSL, built how
```
openssl version -a        # version, build date, compiler flags, OPENSSLDIR, MODULESDIR, CPUINFO
openssl info -configdir   # 3.0+: also -modulesdir, -cpusettings, -seeds
which -a openssl          # more than one on PATH?
```

## What algorithms are available
```
openssl list -providers -verbose
openssl list -cipher-algorithms
openssl list -digest-algorithms
openssl list -mac-algorithms
openssl list -kdf-algorithms
openssl list -signature-algorithms
openssl list -kem-algorithms               # ML-KEM in 3.5+
openssl list -key-exchange-algorithms
openssl list -key-managers                 # key types genpkey can make
openssl list -public-key-algorithms
openssl list -encoders ; openssl list -decoders
openssl list -disabled                     # features, protocols and algorithms compiled out
```
Entries name the provider that serves them.

## TLS-specific views
```
openssl ciphers -v -s 'DEFAULT'            # suites actually usable at current settings
openssl ciphers -v -s -tls1_3              # TLS 1.3 suites
openssl ciphers -v 'ECDHE+AESGCM:@SECLEVEL=2'
openssl list -tls-groups                   # TLS named groups
openssl ecparam -list_curves
```
`-s` filters by what the security level and protocol settings allow; without it you see
everything the string matches.

## Commands and options
```
openssl list -commands
openssl list -options pkcs12               # flags supported by this build's pkcs12
openssl help req
```
`-options` is the fastest way to tell whether a flag like `-copy_extensions` or `-jdktrust` exists
in the installed version.

## Checks to script in CI
```
openssl list -kem-algorithms | grep -qi ML-KEM-768 || echo "no ML-KEM"
openssl list -providers | grep -q fips || echo "fips provider not active"
openssl version | grep -qE '^OpenSSL 3\.' || echo "not OpenSSL 3"
```

## Gotchas
- Capabilities of the CLI binary are not necessarily those of the library your app links;
  check the app's runtime too.

## Verify
- [ ] You recorded version, providers and needed algorithms for each environment.
- [ ] CI fails if a required algorithm (e.g. ML-KEM) is missing.

## Checked
2026-11-01. Confirmed in the OpenSSL man pages and CHANGES.md: `openssl list` options (`-providers`, `-cipher-algorithms`, `-digest-algorithms`, `-mac-algorithms`, `-kdf-algorithms`, `-signature-algorithms`, `-kem-algorithms`, `-key-exchange-algorithms`, `-key-managers`, `-public-key-algorithms`, `-encoders`, `-decoders`, `-disabled`, `-tls-groups`, `-commands`, `-options`, `-verbose`); `openssl info` `-configdir`, `-modulesdir`, `-cpusettings`, `-seeds`; `openssl version` `-a` and the OPENSSLDIR/MODULESDIR/CPUINFO settings; `openssl ciphers` `-v`, `-s`, `-tls1_3` and `@SECLEVEL=n`; `ecparam -list_curves`; ML-KEM added in OpenSSL 3.5.0. Removed: propquery/FIPS filter claim, example disabled feature names, hardware feature list, LibreSSL/BoringSSL claims, language-runtime version attributes.
Method: documentation only; no commands were run.
