---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-fips-mode
name: nodejs-fips-mode
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, node-fips, nodejs, fips-140-3, openssl-fips-provider, compliance]
level: advanced
status: gated
description: "Run Node.js in FIPS mode: building or obtaining a FIPS-capable Node with OpenSSL 3 FIPS provider, --enable-fips and crypto.setFips, config files, and checking getFips."
sources: ["https://nodejs.org/api/crypto.html#cryptosetfipsbool", "https://github.com/nodejs/node/blob/main/BUILDING.md#building-nodejs-with-fips-compliant-openssl", "https://docs.openssl.org/3.0/man7/fips_module/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js FIPS mode

## Getting a FIPS-capable Node
Official binaries do not ship the FIPS provider (on the Windows build tested, `node --enable-fips` failed with an OpenSSL error because `fips.dll` could not be loaded). With OpenSSL 3, BUILDING.md says it is not necessary to rebuild Node.js: install the OpenSSL 3 FIPS provider and load it through the OpenSSL configuration that Node reads (`nodejs_conf` section). Only OpenSSL 1.1.1 needs a Node built against a FIPS-capable OpenSSL. `./configure --openssl-is-fips` exists ("specifies that the OpenSSL library is FIPS compatible") for custom builds. Node itself is not FIPS validated; validation belongs to the OpenSSL module. Distribution and vendor builds (RHEL/UBI, Chainguard) honouring system FIPS mode (gated: unconfirmed, source is paywalled or blocked).

## Enable
```sh
node --enable-fips app.js          # fails at startup if the fips provider cannot load; --force-fips also stops script from turning it off
OPENSSL_CONF=/etc/ssl/openssl-fips.cnf node app.js
```
```js
const crypto = require('node:crypto');
crypto.setFips(true);              // OpenSSL 3: only adds fips=yes to the default property query
console.log(crypto.getFips());     // 1 means that query is set, not that a validated provider is loaded
```
On Node 20 without a FIPS provider, `setFips(true)` did not throw and `getFips()` returned 1; a later `createHash('md5')` threw `error:0308010C:digital envelope routines::unsupported`. Per the Node docs, the provider must be loaded (usually via the OpenSSL config activating `fips` and `base`, with `openssl fipsinstall` producing `fipsmodule.cnf`), and `setFips(true)` should run before other OpenSSL-backed code; `--enable-fips` or the config's `default_properties = fips=yes` are not equivalent and are preferred.

## Effects
- With the `fips=yes` query active, MD5 is refused (seen above). Which other algorithms and key sizes are refused depends on the loaded provider (gated: unconfirmed, no FIPS provider available to test).
- `crypto.createHash('md5')` used for non-security checksums breaks; switch to SHA-256 or a non-crypto hash.
- npm packages bundling their own crypto (pure-JS bcrypt, tweetnacl, WASM libs) are outside the boundary and
  must be reviewed.

## Verify
- [ ] Startup check asserts `crypto.getFips() === 1` and that a real FIPS-provider-only operation works; MD5 call throws in a test. Because `getFips()` can return 1 without a loaded provider, do not rely on it alone.
