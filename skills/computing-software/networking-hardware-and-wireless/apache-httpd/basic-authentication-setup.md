---
id: computing-software.networking-hardware-and-wireless.apache-httpd.basic-authentication-setup
name: basic-authentication-setup
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, authentication, basic-auth, htpasswd, authuserfile, authtype, require]
level: intro
status: docs-checked
description: "Protect a directory with Basic auth: htpasswd file creation and hash options, AuthType/AuthName/AuthUserFile, groups, valid-user and alternate providers."
sources:
  - https://httpd.apache.org/docs/2.4/howto/auth.html
  - https://httpd.apache.org/docs/2.4/programs/htpasswd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic authentication setup
Needs `mod_auth_basic`, an authn provider (`mod_authn_file` ...) and `mod_authn_core`/`mod_authz_core`. In `.htaccess` also `AllowOverride AuthConfig`.

```
htpasswd -c /path/to/passwords rbowen
```
```apache
AuthType Basic
AuthName "Restricted Files"
AuthBasicProvider file
AuthUserFile "/path/to/passwords"
Require user rbowen
```
`AuthName` is the realm; clients reuse credentials per realm and host. Keep the password file outside the web root.

## Groups and users
```apache
AuthGroupFile "/path/to/groups"
Require group GroupName
```
Group file line: `GroupName: rbowen dpitts sungo`. `Require valid-user` admits anyone in the file.

## htpasswd
`-c` creates and truncates an existing file. `-b` puts the password on the command line (use `-i` for scripts). `-m` MD5 is default; `-B` bcrypt (`-C` cost 4-17, default 5); `-D` deletes; `-v` verifies. `-d` crypt, `-s` SHA-1 and `-p` plaintext are insecure.

## Scale and providers
Plain files slow past a few hundred entries; use `AuthBasicProvider dbm` or dbd. `AuthBasicProvider file ldap` tries providers in order. `mod_authn_socache` caches credentials.

## Security
Basic sends passwords in plaintext; use mod_ssl. Digest is no longer considered more secure.

## Checked

2026-11-08. AuthType, AuthName, AuthBasicProvider, AuthUserFile, group files, valid-user, providers, scale warning and socache note confirmed on the full auth how-to; htpasswd options (-c, -b, -i, -m default, -B with -C 4 to 17 default 5, -D, -v, -d, -s, -p) confirmed on the full htpasswd page.

Method: documentation only; no commands were run.
