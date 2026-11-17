---
id: computing-software.collaboration-platform-administration.zulip.realm-hosts-root-domain-and-social-auth
name: realm-hosts-root-domain-and-social-auth
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [realm-hosts, social-auth-subdomain, root-domain, oauth-callback]
level: advanced
status: docs-checked
description: "Customise hosting of multiple Zulip realms: REALM_HOSTS custom hostnames, mixing a root-domain organization with subdomains, and SOCIAL_AUTH_SUBDOMAIN callbacks."
sources: ["https://zulip.readthedocs.io/en/latest/production/multiple-organizations.html", "https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REALM_HOSTS, the root domain and social auth

**Non-subdomain hostnames.** To serve an organization on a hostname that is not a subdomain of your main one, set `REALM_HOSTS` in `/etc/zulip/settings.py` to a dictionary:

```
REALM_HOSTS = {
    "mysubdomain": "hostname.example.com",
}
```

This makes `hostname.example.com` the host for the realm that would otherwise be `mysubdomain.zulip.example.com`. When creating the realm, enter `mysubdomain` as its subdomain. Users never see that value, but you can no longer create a different realm at `mysubdomain.zulip.example.com`. The project expects to move this setting into the database eventually. Tornado sharding by hostname uses these full hostnames for such realms.

**Root domain.** A single organization on `zulip.example.com` internally has the empty string as its subdomain. Mixing a root organization with others on subdomains only works well if no user belongs to both, since root-domain auth cookies are visible to subdomains and one browser cannot log into both. The documentation does not recommend it.

**Authentication callbacks.** Google, GitHub, SAML and similar providers want callback URLs registered, sometimes just one. If the vendor takes a whitelist, list each organization's callback. The cleaner approach is to register a dedicated subdomain, such as `auth.zulip.example.com`, with the provider and set:

```
SOCIAL_AUTH_SUBDOMAIN = 'auth'
```

in `/etc/zulip/settings.py`, so Zulip uses that subdomain for all authentication callbacks.

## Checked

Confirmed against the Other hostnames, The root domain and Authentication sections of the multiple-organizations page, and the tornado_sharding section of the system-configuration page (REALM_HOSTS organizations are sharded by full hostname). Removed the closing certificate remark (not on the page).

Method: docs-checked 2026-11-09 against docs/production/multiple-organizations.md and docs/production/system-configuration.md in the zulip/zulip repository (main), the sources of the cited pages.
