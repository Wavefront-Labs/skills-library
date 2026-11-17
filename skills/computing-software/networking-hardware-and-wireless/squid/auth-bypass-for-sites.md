---
id: computing-software.networking-hardware-and-wireless.squid.auth-bypass-for-sites
name: auth-bypass-for-sites
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, authentication-bypass, http-access, proxy-auth, whitelist]
level: practitioner
status: docs-checked
description: "Let selected sites skip proxy authentication by placing their allow rules before the proxy_auth rules."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Authenticate/Bypass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bypass authentication for some sites
The key is that every `http_access` rule allowing unauthenticated users sits before the rules that require knowledge of the user's identity. Example from the page (authentication already configured with `auth_param`):
```
acl whitelist dstdomain .whitelist.com .goodsite.com .partnerssite.com
acl http proto http
acl port_80 port 80
acl port_443 port 443
acl CONNECT method CONNECT
acl authenticated_users proxy_auth REQUIRED

# rules allowing non-authenticated users
http_access allow http port_80 whitelist
http_access allow CONNECT port_443 whitelist

# rules allowing authenticated users
http_access allow http port_80 authenticated_users
http_access allow CONNECT port_443 authenticated_users

http_access deny all
```
Whitelisted sites pass without credentials; other traffic on the standard ports needs a login. Order matters, also within each rule: putting `deny authenticated_users` as the last rule instead of `deny all` makes users get a password prompt before being denied.

## Checked

2026-11-04. Read the Authenticate/Bypass wiki page and confirmed the rule-order principle. Replaced the invented sketch with the page's own example and added the page's note on rule order.

Method: documentation only; no commands were run.
