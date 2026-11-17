---
id: computing-software.collaboration-platform-administration.exchange-online.basic-auth-modern-auth
name: basic-auth-modern-auth
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [basic-auth-modern-auth, exo-client-access]
level: advanced
status: draft
description: Move clients to modern authentication and block legacy protocols.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disable basic authentication
**Goal:** Move clients to modern authentication and block legacy protocols.

- Basic auth for most protocols is already disabled by Microsoft; SMTP AUTH is the common exception.
- Disable per mailbox: `Set-CASMailbox <id> -SmtpClientAuthenticationDisabled $true`.
- Use authentication policies (`New-AuthenticationPolicy`) or Conditional Access to block legacy auth.
- Find use via Entra sign-in logs, filter client app 'Other clients'.

## Gotchas
- Devices and printers scanning to email may rely on SMTP AUTH or a connector; migrate to connector/relay.
- Test before blocking tenant-wide.

## Self-check
Sign-in logs show no legacy auth clients for 14 days before the block.
