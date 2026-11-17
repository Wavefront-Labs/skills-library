---
id: computing-software.networking-hardware-and-wireless.squid.auth-param-schemes
name: auth-param-schemes
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, auth-param, basic, digest, negotiate, ntlm]
level: practitioner
status: docs-checked
description: "Configure authentication schemes with auth_param: Basic, Digest, Negotiate and NTLM parameters and their ordering."
sources:
  - https://www.squid-cache.org/Doc/config/auth_param/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# auth_param schemes
Form: `auth_param scheme parameter [setting]`; needs `--enable-auth`. Defining a scheme does not enable authentication: use an ACL such as `proxy_auth` in `http_access`. It cannot be used on intercept or tproxy ports.

- Basic: external helper; `credentialsttl`, `casesensitive`; default realm Squid proxy-caching web server
- Digest: needs `realm`; nonce settings such as `nonce_max_duration`
- Negotiate and NTLM: ignore `realm`; `reservation-timeout`, `keep_alive`

Parameters: `program` (scheme inactive until set), `children` (`startup`, `idle`, `concurrency`, `queue-size`), `realm`, `utf8` (Basic and Digest).

Scheme order in the file is the order offered; Internet Explorer may pick Basic if listed first.
```
auth_param basic children 5 startup=5 idle=1
auth_param basic credentialsttl 2 hours
auth_param negotiate children 20 startup=0 idle=1
```

## Checked

2026-11-04. Read the auth_param directive page and confirmed the build option, scheme ordering and IE note, common and per-scheme parameters, defaults, the intercept and tproxy limit and the example lines. Nothing was removed.

Method: documentation only; no commands were run.
