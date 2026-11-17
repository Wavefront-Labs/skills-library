---
id: computing-software.networking-hardware-and-wireless.squid.ncsa-basic-auth
name: ncsa-basic-auth
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, ncsa, htpasswd, basic-auth, proxy-auth]
level: intro
status: docs-checked
description: "Authenticate users against an NCSA-style passwords file with the basic_ncsa_auth helper and htpasswd."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Authenticate/Ncsa
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NCSA password-file authentication
Create the file (first user), add and delete users:
```
htpasswd -c -nbm /path/to/passwords username password
htpasswd -nbm /path/to/passwords username password
htpasswd -D -nbm /path/to/passwords username password
```
squid.conf:
```
auth_param basic program /usr/lib/squid/basic_ncsa_auth /path/to/passwords
auth_param basic children 5
auth_param basic credentialsttl 1 minute
acl auth proxy_auth REQUIRED
http_access deny !auth
http_access allow auth
http_access deny all
```
Helpers support DES, MD5 and SHA; Bcrypt may or may not work depending on the crypto libraries Squid was built with.

## Checked

2026-11-04. Read the Authenticate/Ncsa wiki page and confirmed the htpasswd commands, squid.conf lines, ACL rules and supported password formats. Nothing was removed.

Method: documentation only; no commands were run.
