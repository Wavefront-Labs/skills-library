---
id: computing-software.collaboration-platform-administration.zulip.multiple-organizations-subdomains
name: multiple-organizations-subdomains
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [multiple-organizations, realm-subdomains, open-realm-creation, wildcard-certificate]
level: practitioner
status: docs-checked
description: "Host several Zulip organizations on one server using one subdomain per realm: certificates, nginx, generate_realm_creation_link, wildcard certs and open realm creation."
sources: ["https://zulip.readthedocs.io/en/latest/production/multiple-organizations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hosting multiple organizations (subdomains)

Most servers host one organization (a "realm" in the code). To host several, give each its own subdomain, such as `org1.zulip.example.com` and `org2.zulip.example.com`. Web security standards require one subdomain per organization for a user to be logged into several at once.

To add an organization:

1. Make sure a certificate covers every subdomain. With Zulip's Certbot wrapper you can list multiple hostnames in one request. For many organizations, a wildcard certificate is easier; Certbot can get one free, but the stricter checks mean the generic `setup-certbot` script cannot, so you do manual steps with your DNS provider.
2. Adjust the nginx configuration to use the new certificates if needed.
3. Run `./manage.py generate_realm_creation_link` and use the link, as in the install guide.
4. For GitHub or other social authentication, see the `SOCIAL_AUTH_SUBDOMAIN` skill.

Existing organizations can change subdomain through a management command, but understand the disruption to users first.

A hidden extra realm named `zulipinternal` exists on every server. It holds system bots such as Notification Bot and Welcome Bot; list them with `./scripts/get-django-setting INTERNAL_BOTS`.

Moving from a root-domain setup to subdomains: clear cookies in browsers that were logged in on the root domain, or they hit confusing redirects.

Services like Zulip Cloud that let anyone create organizations set `OPEN_REALM_CREATION = True` in `/etc/zulip/settings.py`. The documentation warns this carries significant responsibility for security, abuse and spam, and legal compliance such as GDPR and CCPA.

## Checked

Confirmed against the Hosting multiple organizations page: one subdomain per organization, the certificate and wildcard notes, generate_realm_creation_link, subdomain changes, the zulipinternal realm and INTERNAL_BOTS, the cookie advice and OPEN_REALM_CREATION. Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/multiple-organizations.md in the zulip/zulip repository (main), the source of the cited page.
