---
id: computing-software.systems-network-administration.nagios-core.cgi-security-hardening
name: cgi-security-hardening
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, cgi-security, digest-authentication, htdigest, sslrequiressl, apache, ip-lockdown, mod-ssl, web-hardening]
level: advanced
status: docs-checked
description: "Harden the Nagios Core web interface in Apache: Digest auth with htdigest, forcing TLS with SSLRequireSSL, and restricting by IP subnet."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cgisecurity.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced CGI security (Apache)

Edit the Nagios Apache config (typically `/etc/httpd/conf.d/nagios.conf`); apply to BOTH the `sbin` (cgi-bin) and `share` directory blocks; restart Apache.

## 1. Digest instead of Basic
Basic sends credentials on every request.
```
htdigest -c /usr/local/nagios/etc/.digest_pw "Nagios Access" nagiosadmin
```
Then `AuthType Digest`, `AuthName "Nagios Access"` (must match the realm), `AuthDigestFile /usr/local/nagios/etc/.digest_pw`, `Require valid-user`. Digest is not as universally supported as Basic.

## 2. Force TLS
Confirm `https://your.domain/nagios` works with `mod_ssl`, then add `SSLRequireSSL` to both blocks. TLS is still open to man-in-the-middle (phishing, re-signing proxies); verify certificates.

## 3. IP lockdown
`Order deny,allow`, `Deny from all`, then `Allow from` single IPs, network/netmask or CIDR. Use a VPN or SSH tunnel for remote access. Apache rules cover HTTP(S) only; use iptables for system-wide limits.

Treat the monitoring server as critical infrastructure. Overall list: `computing-software.systems-network-administration.nagios-core.security-best-practices`.

## Checked

2026-11-04. Confirmed against the Enhanced CGI Security and Authentication page: htdigest command and realm matching AuthName, the Digest directives, SSLRequireSSL in both the sbin and share blocks, the IP lockdown directives, Apache restart, man-in-the-middle and iptables notes. Removed the unconfirmed mod_auth_digest requirement.

Method: documentation only; no commands were run.
