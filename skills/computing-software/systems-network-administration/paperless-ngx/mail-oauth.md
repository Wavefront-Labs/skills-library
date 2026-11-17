---
id: computing-software.systems-network-administration.paperless-ngx.mail-oauth
name: mail-oauth
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, email-oauth, gmail, outlook, paperless-url, oauth-callback]
level: advanced
status: docs-checked
description: "Connect Gmail or Outlook mail accounts to Paperless-ngx with OAuth2, including the callback URL setting and token-as-password option."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/administration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email OAuth

Paperless supports OAuth2 for Gmail and Outlook accounts.

## Steps
1. Create a developer app with the provider (Google or Microsoft). The docs leave exact instructions to the provider and a community wiki page.
2. Put the client ID and secret into `PAPERLESS_GMAIL_OAUTH_CLIENT_ID` and `PAPERLESS_GMAIL_OAUTH_CLIENT_SECRET`, or `PAPERLESS_OUTLOOK_OAUTH_CLIENT_ID` and `PAPERLESS_OUTLOOK_OAUTH_CLIENT_SECRET`.
3. Set either `PAPERLESS_OAUTH_CALLBACK_BASE_URL` or `PAPERLESS_URL` to the address the instance is accessible at; the flow needs a correct value. The callback setting defaults to `PAPERLESS_URL`.
4. Open the email settings page and add a Gmail or Outlook account, then authenticate.
5. Enter and save your email address on the newly created account. After that it behaves like any other account and tokens refresh automatically.

## Using a token as a password
For other providers where you obtain an access token yourself, tick the box on the mail account that says the password is actually a token. Creating the token depends on the provider.

## Related settings
- `PAPERLESS_EMAIL_CERTIFICATE_LOCATION` adds a trusted certificate for self-signed local IMAP servers.
- Mail is fetched every 10 minutes by default, configurable with `PAPERLESS_EMAIL_TASK_CRON`; trigger a run with the `mail_fetcher` command.

## Checked
2026-11-04. Compared with OAuth Email Setup and Mail rules in usage, the Email OAuth and certificate settings in configuration, and Fetching e-mail in administration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: steps, provider instructions left to the wiki, callback setting and PAPERLESS_URL fallback, token-as-password box, certificate setting purpose, 10 minute fetch and mail_fetcher. Named the four OAuth variables from configuration. Removed: the security remark on the certificate setting and the closing secret-handling advice (not on the pages).

Method: documentation only; no commands were run.
