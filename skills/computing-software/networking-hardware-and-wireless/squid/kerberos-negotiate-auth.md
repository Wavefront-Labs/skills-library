---
id: computing-software.networking-hardware-and-wireless.squid.kerberos-negotiate-auth
name: kerberos-negotiate-auth
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, kerberos, negotiate, keytab, krb5, single-sign-on]
level: sme
status: docs-checked
description: "Set up Kerberos Negotiate authentication in Squid with a keytab for HTTP/fqdn and the negotiate helper."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Authenticate/Kerberos
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos (Negotiate) authentication
Steps: configure krb5.conf (realm, KDC, encryption types); create a keytab for `HTTP/<fqdn>` (msktutil, Samba `net ads keytab`, or kadmin); make it readable by the Squid user; set the keytab in the startup script.
```
auth_param negotiate program /usr/sbin/squid_kerb_auth
auth_param negotiate children 10
auth_param negotiate keep_alive on
acl auth proxy_auth REQUIRED
http_access deny !auth
http_access allow auth
http_access deny all
```
Startup script:
```
KRB5_KTNAME=/path/to/HTTP.keytab
export KRB5_KTNAME
```
Caveats from the page: avoid the Samba keytab method with winbindd (it resets the machine password); the helper name differs between outline and sample, so confirm the binary; Internet Explorer needs an FQDN proxy name; `KRB5RCACHETYPE=none` cuts CPU but weakens security; tickets expire after about 8 hours.

## Checked

2026-11-04. Read the Authenticate/Kerberos wiki page and confirmed the keytab methods, squid.conf lines, KRB5_KTNAME startup lines, the winbindd warning, the helper name difference, the IE FQDN note, KRB5RCACHETYPE and the 8 hour ticket lifetime. Nothing was removed.

Method: documentation only; no commands were run.
