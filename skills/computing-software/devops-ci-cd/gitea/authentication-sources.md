---
id: computing-software.devops-ci-cd.gitea.authentication-sources
name: authentication-sources
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-ldap-bind-dn, gitea, ldap-simple-auth, pam-auth, smtp-auth, sspi, reverse-proxy-auth, oauth2-client, openid-connect-source, x-webauth-user]
level: advanced
status: docs-checked
description: "Configure Gitea external login sources: LDAP BindDN or simple, PAM, SMTP, FreeIPA, SSPI, reverse proxy header auth, OAuth2/OIDC with callback URL and group claims."
sources: ["https://docs.gitea.com/administration/authentication/", "https://docs.gitea.com/administration/command-line/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# External authentication sources

Add under Site Administration, Authentication Sources (or `gitea admin auth ...` on the CLI, see `gitea-admin-user-create`).

## LDAP
Shared fields: name, host (required), port (389 LDAP, 636 LDAPS), TLS, admin filter (e.g. `(objectClass=adminAccount)`, AD: `(memberOf=CN=admin-group,OU=example,DC=example,DC=org)`), username attribute (`uid`; AD `sAMAccountName`; empty means the login name typed is used), first-name `givenName`, surname `sn`, and **email attribute (required)** `mail`.
- **Via BindDN**: bind DN/password (empty bind DN means anonymous search; password is stored encrypted with `SECRET_KEY`, so give the bind account minimal rights), **user search base** and **user filter** (both required). The filter uses `%[1]s` for the typed login and can repeat it: `(&(objectClass=Person)(|(uid=%[1]s)(mail=%[1]s)(mobile=%[1]s)))`. User synchronisation runs as a cron task (default every 24 h, section `cron.sync_external_users`); the first run creates every matching LDAP user, so be careful with big directories.
- **Simple auth**: **User DN template** with `%s`, e.g. `uid=%s,ou=Users,dc=mydomain,dc=com`, plus a required user filter.
- **Group verification** (optional): group search base DN, group attribute listing members (`memberUid` or `member`), user attribute referenced in the group (`uid`, or `dn`), and a group filter such as `(|(cn=gitea_users)(cn=admins))`.
CLI example: `gitea admin auth add-ldap --name ldap --security-protocol unencrypted --host mydomain.org --port 389 --user-search-base "ou=Users,dc=mydomain,dc=org" --user-filter "(&(objectClass=posixAccount)(|(uid=%[1]s)(mail=%[1]s)))" --email-attribute mail` (`add-ldap-simple` takes `--user-dn`).

## PAM
Needs a PAM-enabled build (official binaries lack it; `pam` build tag). Pick the service file under `/etc/pam.d/` (Debian "Bullseye" example `common-session-noninteractive`) and a **PAM email domain**, required: user `gituser` with domain `mail.com` gets email `gituser@mail.com` but still logs in as `gituser`. The Gitea user needs read access to `/etc/shadow` for plain Linux passwords. SSH keys already added in Gitea may bypass the PAM check, so also disable the user in Gitea when removing them.

## SMTP
Gitea logs in to an SMTP server as the user. Type PLAIN or LOGIN, host, port (587), allowed domains (comma list), Force SMTPS (port 465 uses SMTPS by default, otherwise STARTTLS if offered), skip TLS verify, active flag. (The CLI also lists CRAM-MD5.)

## FreeIPA
Create a bind account via LDIF (`dn: uid=gitea,cn=sysaccounts,cn=etc,dc=example,dc=com`, `userPassword`, `passwordExpirationTime: 20380119031407Z`, `nsIdleTimeout: 0`) imported with `ldapmodify -h localhost -p 389 -x -D "cn=Directory Manager" -W -f gitea.ldif`, add group `ipa group-add --desc="Gitea Users" gitea_users`, then add an LDAP source. Run `kinit admin` if IPA credential errors appear.

## SPNEGO/SSPI (Windows only)
Run `gitea.exe` as a dedicated AD account, register one SPN: `setspn -A HTTP/host.domain.local domain\user` (host only, no port; `ROOT_URL` must use that FQDN). Add an `SPNEGO with SSPI` source, browse from a different domain-joined client with the URL in the Local intranet zone. Clocks within 5 minutes; same-machine client falls back to NTLM.

## Reverse proxy header login
```ini
[service]
ENABLE_REVERSE_PROXY_AUTHENTICATION = true
ENABLE_REVERSE_PROXY_AUTO_REGISTRATION = true
```
Headers: `X-WEBAUTH-USER` (change with `REVERSE_PROXY_AUTHENTICATION_USER`), `X-WEBAUTH-EMAIL` (`REVERSE_PROXY_AUTHENTICATION_EMAIL`, disable with `ENABLE_REVERSE_PROXY_EMAIL`), `X-WEBAUTH-FULLNAME` with `ENABLE_REVERSE_PROXY_FULL_NAME=true`. Covers web, Git over HTTP, LFS and packages. Gitea trusts these on every request: it must only be reachable through the proxy, which must set or strip them everywhere; `REVERSE_PROXY_TRUSTED_PROXIES` does not restrict them. `ENABLE_REVERSE_PROXY_AUTHENTICATION_API = true` extends it to `/api/v1`, and then the proxy owns CSRF protection.

## OAuth2 / OpenID Connect (client)
Provider `OpenID Connect` (needs the discovery URL, usually `.../.well-known/openid-configuration`) or a built-in one (Gitea, GitHub, GitLab, Google, Discord, Bitbucket, Dropbox, Facebook, Mastodon, Nextcloud, Twitter, Yandex, Azure AD v2). The source name is part of the callback, so renaming means re-registering. Redirect URI: `{ROOT_URL}/user/oauth2/{name}/callback`; a wrong one is the most common failure. Optional: scopes (`openid` always added for OIDC; `OPENID_CONNECT_SCOPES` in `app.ini`), required claim name/value, group claim name with admin-group, restricted-group and org-team mapping (all need the claim name), icon URL. Account policy lives in `[oauth2_client]`: `ENABLE_AUTO_REGISTRATION`, `USERNAME` (e.g. `nickname`), `ACCOUNT_LINKING` (e.g. `login`). Unrelated to the older `[openid]` OpenID 2.0 sign-in.

## Checked

2026-11-03: read https://docs.gitea.com/administration/authentication/, https://docs.gitea.com/administration/command-line/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
