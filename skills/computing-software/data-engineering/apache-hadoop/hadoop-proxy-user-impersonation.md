---
id: computing-software.data-engineering.apache-hadoop.hadoop-proxy-user-impersonation
name: hadoop-proxy-user-impersonation
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, security, proxy-user, impersonation, doas, delegation-tokens]
level: advanced
status: docs-checked
description: "Hadoop proxy users: hadoop.proxyuser.<superuser>.hosts/groups/users settings, deny-by-default behaviour, wildcards, createProxyUser with doAs, and delegation token caveats."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/Superusers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy users (impersonation)

Lets a superuser with Kerberos credentials submit jobs or access HDFS as another user such as `joe`, who has no credentials of his own. Tasks run as joe and NameNode file access is done as joe, over a connection authenticated with the superuser's Kerberos credentials. The page notes Apache Oozie needs this.

Configure in core-site.xml:
- `hadoop.proxyuser.$superuser.hosts`: IP addresses, CIDR ranges (e.g. `10.222.0.0/16`) and/or host names
- `hadoop.proxyuser.$superuser.groups` and/or `hadoop.proxyuser.$superuser.users`

Set `hosts` together with either or both of `groups` and `users`. If these settings are absent, impersonation is not allowed and the connection fails.

The wildcard `*` allows impersonation from any host or of any user/group; the page calls this the "more lax" option and shows it for `oozie`. A restricted example: `super` only from `host1` and `host2`, impersonating members of `group1` and `group2`.

Code pattern:

```
UserGroupInformation ugi = UserGroupInformation.createProxyUser("joe", UserGroupInformation.getLoginUser());
ugi.doAs(...)
```

Caveats:
- In secure mode the superuser must have Kerberos credentials.
- Delegation tokens cannot be used for impersonation itself. Adding the superuser's own token to the proxy UGI would let the proxy user connect with the superuser's privileges.
- To give `joe` a token, impersonate `joe`, obtain a delegation token for joe that way, and add it to joe's UGI so the token's owner is joe.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (Superusers.md in the apache/hadoop repo). Removed an unsupported "Verify" step (error text not stated on the page) and a "refresh commands" remark about content the page does not discuss.
