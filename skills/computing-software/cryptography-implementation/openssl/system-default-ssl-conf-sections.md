---
id: computing-software.cryptography-implementation.openssl.system-default-ssl-conf-sections
name: system-default-ssl-conf-sections
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, ssl-conf-module, openssl-cnf, system-default, minprotocol, cipherstring, crypto-policies, tls-configuration]
level: practitioner
status: docs-checked
description: "Set process-wide TLS defaults with openssl.cnf ssl_conf system_default: MinProtocol, CipherString, Ciphersuites, Groups, SignatureAlgorithms and how apps inherit them."
sources: ["https://docs.openssl.org/master/man5/config/", "https://docs.openssl.org/master/man3/SSL_CTX_config/", "https://docs.openssl.org/master/man3/SSL_CONF_cmd/", "https://nodejs.org/api/cli.html#--openssl-shared-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# system_default ssl_conf sections

OpenSSL's `ssl_conf` module applies the `system_default` section whenever an `SSL_CTX` object is created, for
applications that load the configuration file (in most applications the default `openssl.cnf` is loaded automatically as
part of library initialisation).

## Example
```
openssl_conf = openssl_init

[openssl_init]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
MinProtocol = TLSv1.2
CipherString = DEFAULT:@SECLEVEL=2
Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256
Groups = X25519MLKEM768:X25519:P-256:P-384
SignatureAlgorithms = ECDSA+SHA256:ECDSA+SHA384:ed25519
Options = -SessionTicket
```
Keys are `SSL_CONF_cmd` file option names (case-insensitive): `MinProtocol`, `MaxProtocol`, `CipherString`,
`Ciphersuites`, `Groups` (`Curves` is the older name), `SignatureAlgorithms`, `ClientSignatureAlgorithms`, `Options`
(comma-separated flags, a leading `-` disables one, for example `-SessionTicket`), `VerifyMode`. `X25519MLKEM768` in
`Groups` needs OpenSSL 3.5 or later.

## Where it lives
- The default file is `openssl.cnf` under OPENSSLDIR (`openssl version -d`); distributions may generate parts of it, so
  check your distribution's documentation before editing it by hand.
- Per-application: point `OPENSSL_CONF` at a different file.

## Precedence
The section is applied when the context is created, so application calls made afterwards (`SSL_CTX_set_cipher_list`,
`SSL_CTX_set_min_proto_version`) override these defaults. Other named sections (for example `server` or `client`
entries beside `system_default`) are applied only when the application calls `SSL_CTX_config` or `SSL_config` with that
name.

## Gotchas
- Without `config_diagnostics = 1` a configuration error leaves access allowed but the desired configuration unused; with
  it the error blocks the service (see config(5)).
- Node.js reads its own `nodejs_conf` section by default instead of `openssl_conf`.
- Lowering settings system-wide for one legacy peer weakens every app; scope it with `OPENSSL_CONF` instead.

## Verify
- [ ] `openssl s_client -connect legacy:443 -tls1_1` fails after setting MinProtocol.
- [ ] Each application that should be covered reports the restrictions (applications that do not load the default config
      are unaffected).

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in config(5) (ssl_conf section, `system_default` applied whenever an `SSL_CTX` is created, `config_diagnostics`), SSL_CTX_config(3) (default openssl.cnf loaded automatically in most applications, named sections via `SSL_CTX_config`), SSL_CONF_cmd(3) (file option names and case-insensitivity, `Options` syntax with a leading `-`, `SessionTicket`, `Curves`, `Groups`, X25519MLKEM768 from 3.5) and the Node.js CLI docs for `nodejs_conf`. Removed the Debian and RHEL path claims, the nginx, Postgres, Python and Ruby statements and the unchecked `rsa_pss_rsae_*` scheme names.

Method: documentation only; no commands were run.
