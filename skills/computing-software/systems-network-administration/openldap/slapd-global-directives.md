---
id: computing-software.systems-network-administration.openldap.slapd-global-directives
name: slapd-global-directives
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, global-directives, idletimeout, referral, rootdn, suffix, readonly]
level: practitioner
status: docs-checked
description: "Set OpenLDAP global and database directives: idletimeout, referral, sizelimit, timelimit, suffix order, rootdn and rootpw, readonly, updateref, with defaults."
sources:
  - https://www.openldap.org/doc/admin26/slapdconfig.html
  - https://www.openldap.org/doc/admin26/slapdconf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapd global and database directives
slapd.conf keyword / cn=config attribute, with defaults:
- `idletimeout <s>` / `olcIdleTimeout`: close idle clients; default 0 (disabled).
- `referral <URI>` / `olcReferral`: returned when no local database handles the request, e.g. `ldap://root.openldap.org`.
- `sizelimit` 500, `timelimit` 3600 (see the limits skill).
- `readonly on|off` / `olcReadonly`: default off. When on, writes return "unwilling to perform" but syncrepl updates still apply.
- `suffix <dn>` / `olcSuffix`: at least one; if one suffix is a prefix of another, the longer must come first.
- `rootdn <DN>` / `olcRootDN`: exempt from ACLs and administrative limits; it need not exist. May be a SASL identity: `rootdn "uid=root,cn=example.com,cn=digest-md5,cn=auth"`.
- `rootpw` / `olcRootPW`: plaintext or RFC 2307 hash from slappasswd, e.g. `{SSHA}...`.
- `updateref <URL>` / `olcUpdateref`: returned to clients that send updates to a replica; repeatable.
- `include <file>`: read another config file.

With no `access` rules the default is read for all (`access to * by * read`).

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide slapd.conf chapter and slapd-config(5): idletimeout default 0, referral, sizelimit 500, timelimit 3600, readonly behaviour with syncrepl, suffix ordering, rootdn exemption and SASL form, rootpw hashes, updateref, include, default access to * by * read, and the olc attribute names. Removed the Verify line, whose slaptest and ldapsearch invocations were not confirmed on the fetched pages.

Method: documentation only; no commands were run.
