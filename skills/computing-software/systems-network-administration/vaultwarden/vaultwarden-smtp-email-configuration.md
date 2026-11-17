---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-smtp-email-configuration
name: vaultwarden-smtp-email-configuration
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, smtp, email, smtp-security, starttls, force-tls, invitations, gmail, sendgrid]
level: practitioner
status: docs-checked
description: "Configure Vaultwarden outbound email: SMTP_HOST, port, SMTP_SECURITY modes, credentials, auth mechanism, HELO name, provider notes and connectivity troubleshooting."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/SMTP-Configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden SMTP configuration

Variables: `SMTP_HOST`, `SMTP_FROM`, `SMTP_PORT`, `SMTP_SECURITY`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_AUTH_MECHANISM`, `HELO_NAME` (default machine hostname). Omit username and password for servers accepting unauthenticated mail. `DOMAIN` must be set for invitation links. `USE_SENDMAIL=true` uses a local sendmail on non-Docker installs.

`SMTP_SECURITY` (replaced an older mislabelled variable in v1.25.0):

- `starttls` (default): port 587, upgrades after connecting; TLSv1.1 and TLSv1.2 only.
- `force_tls`: implicit TLS, typically port 465.
- `off`: port 25, opportunistic encryption; described as very insecure.

Port 25 is often blocked by ISPs; 587 is submission and needs credentials.

```
docker run -d --name vaultwarden   -e SMTP_HOST=smtp.domain.tld -e SMTP_FROM=vaultwarden@domain.tld   -e SMTP_PORT=587 -e SMTP_SECURITY=starttls   -e SMTP_USERNAME=myusername -e SMTP_PASSWORD='MyPassw0rd'   -v /vw-data/:/data/ -p 80:80 vaultwarden/server:latest
```

Providers: Gmail needs an App Password (`smtp.gmail.com` 465 `force_tls` or 587 `starttls`); SendGrid uses username `apikey`, the `SG.` API key as password and `SMTP_AUTH_MECHANISM=Login`; Stalwart can use `Xoauth2`. Outlook/Office365 basic auth is marked as no longer working because Microsoft requires OAuth2. The error "No compatible authentication mechanism was found" usually means the provider requires OAuth2, which Vaultwarden does not support; the wiki suggests email-oauth2-proxy. Quote passwords with special characters. Test reachability with `nc -vz host port`.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: SMTP-Configuration.
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
