---
id: computing-software.cloud-infrastructure-engineering.openbao.userpass-auth
name: userpass-auth
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, userpass, login, users, policies]
level: intro
status: docs-checked
description: "Enable the OpenBao userpass auth method, create users with policies, and log in via CLI or HTTP API."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/auth/userpass.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Userpass auth

```
bao auth enable userpass
bao auth enable -path=<path> userpass
```

## Create a user

```
bao write auth/userpass/users/mitchellh \
    password=foo \
    policies=admins
```

If you mounted elsewhere, use `auth/<path>/users/<name>`.

## Log in

```
bao login -method=userpass username=mitchellh password=foo
```

```
curl --request POST \
    --data '{"password": "foo"}' \
    http://127.0.0.1:8200/v1/auth/userpass/login/mitchellh
```

## Notes

- The method lowercases submitted usernames, and cannot read users from an external source.
- User lockout applies (userpass, ldap, approle only): see user-lockout.

## Checked

2026-11-04. Confirmed against the Userpass auth method page: enabling at the default or a custom path, creating a user with password and policies, CLI and API login, username lowercasing, no external user source, and the userpass, ldap and approle lockout limitation. Removed an unsupported claim about shell history.

Method: documentation only; no commands were run.
