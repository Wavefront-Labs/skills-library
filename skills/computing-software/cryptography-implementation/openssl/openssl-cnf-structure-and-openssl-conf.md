---
id: computing-software.cryptography-implementation.openssl.openssl-cnf-structure-and-openssl-conf
name: openssl-cnf-structure-and-openssl-conf
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-cnf, providers, openssl-conf, ssl-conf, config-diagnostics, openssl-3]
level: advanced
status: docs-checked
description: "Understand openssl.cnf: default section, openssl_conf init chain, .include, variables, ssl_conf system defaults, OPENSSL_CONF and per-app config like Node's nodejs_conf."
sources: ["https://docs.openssl.org/master/man5/config/", "https://docs.openssl.org/master/man3/SSL_CONF_cmd/", "https://docs.openssl.org/master/man7/openssl-env/", "https://nodejs.org/api/cli.html#--openssl-shared-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openssl.cnf structure and OPENSSL_CONF

The OpenSSL config file controls providers, algorithm defaults and system-wide TLS settings for
every program linked against libcrypto/libssl that loads it. Most "works in curl but not in my
app" puzzles are about which config got loaded.

## Which file is used
- `OPENSSL_CONF=/path/file.cnf` names the config file (and `OPENSSL_CONF_INCLUDE` the include directory); both are
  treated as security-sensitive environment variables.
- Otherwise `OPENSSLDIR/openssl.cnf`; find the directory with `openssl version -d` or `openssl info -configdir`.
- Language runtimes may link their own OpenSSL: Node.js documents that the location of its default config file depends on
  how OpenSSL is linked into it.
- Node.js reads the section `nodejs_conf` by default; `--openssl-shared-config` (added v18.5.0, v16.17.0, v14.21.0) makes
  it read `openssl_conf` instead, and `--openssl-config=file` names the file.

## Anatomy
```
# default (unnamed) section: must come first
openssl_conf = openssl_init
.include /etc/ssl/openssl.d/          # file or directory of *.cnf
config_diagnostics = 1                # a configuration error blocks use instead of being ignored

[openssl_init]
providers   = provider_sect
alg_section = algorithm_sect
ssl_conf    = ssl_sect
random      = random_sect

[provider_sect]
default = default_sect
[default_sect]
activate = 1

[algorithm_sect]
default_properties = ?fips=yes        # prefer, not require

[ssl_sect]
system_default = system_default_sect
[system_default_sect]
MinProtocol = TLSv1.2
CipherString = DEFAULT:@SECLEVEL=2
Groups = X25519:P-256:P-384
```
- Only the init chain named by `openssl_conf` is applied at library init; other sections are used by
  commands (`[req]`, `[ca]`) that ask for them.
- `system_default` keys are `SSL_CONF_cmd` names (`MinProtocol`, `CipherString`, `Ciphersuites`,
  `Groups`, `SignatureAlgorithms`, `Options`). They apply to every `SSL_CTX` created afterwards.
- Variables: `$name` / `${name}` in the same section, `${sect::name}`, `$ENV::VAR`.
- `.pragma dollarid:true` treats `$` in names literally; `.pragma abspath:true` requires absolute include paths.
- An included directory contributes its `.cnf` and `.conf` files only.

## Debugging
```
openssl list -providers                                      # did activation work?
openssl version -d                                           # where OPENSSLDIR is
```
Without `config_diagnostics = 1`, in the presence of a configuration error access is allowed but the desired
configuration is not used. With it, the error blocks access to the service entirely, so test before enabling it in
production.

## Gotchas
- Applications that call `OPENSSL_init_crypto` with `OPENSSL_INIT_NO_LOAD_CONFIG`, or create their
  own `OSSL_LIB_CTX`, don't see these settings; libraries can load a config into a context with
  `OSSL_LIB_CTX_load_config`.
- The `openssl.cnf` shipped in each base image or host may differ, so the same app can behave differently between them.
- Editing the system file affects every service on the host; prefer an app-specific
  `OPENSSL_CONF` that `.include`s the system file and adds overrides.

## Verify
- [ ] You can state the config path, OpenSSL version and active providers for each service.
- [ ] `config_diagnostics = 1` is set where settings are security-relevant.
- [ ] TLS policy in `system_default` matches what `s_client` against the service shows.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in config(5) (default section and `openssl_conf`, `.include` and `.pragma` semantics, `$ENV::` and `${sect::name}` variables, `config_diagnostics` behaviour, `providers`, `alg_section`, `ssl_conf` with `system_default` applied to every `SSL_CTX`, random section), openssl-env(7), openssl-info(1) `-configdir`, openssl-version(1) `-d`, OPENSSL_init_crypto(3) `OPENSSL_INIT_NO_LOAD_CONFIG`, the existence of `OSSL_LIB_CTX_load_config`, and the Node.js CLI docs for `--openssl-shared-config` and `nodejs_conf`. Removed unconfirmed claims about `/dev/null` as an empty config, Python and Java runtimes, Debian image defaults, strace usage and the hybrid ML-KEM group in the example.

Method: documentation only; no commands were run.
