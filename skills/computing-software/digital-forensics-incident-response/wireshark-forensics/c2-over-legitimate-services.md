---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.c2-over-legitimate-services
name: c2-over-legitimate-services
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [c2-over-legitimate-services, telegram-bot-api, discord-webhooks, cloud-storage-c2, c2-detection, dfir]
level: advanced
status: draft
description: "Investigate C2 and exfiltration over legitimate services (Telegram Bot API, Discord webhooks, cloud storage, paste sites): network signals, process context, token recovery and takedown."
sources: ["https://attack.mitre.org/techniques/T1102/", "https://attack.mitre.org/techniques/T1567/", "https://core.telegram.org/bots/api", "https://discord.com/developers/docs/resources/webhook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# C2 over legitimate services

Infostealers and RATs increasingly use web services for C2 and exfiltration (T1102 Web Service, T1567 Exfiltration Over Web Service): Telegram bots, Discord webhooks, Slack, GitHub, Google Drive/Dropbox/OneDrive, Pastebin. Traffic goes to trusted domains over TLS, so blocklists and reputation fail.

## Network signals
| Service | Indicator (SNI / URL if inspected) |
|---|---|
| Telegram | `api.telegram.org`, paths `/bot<token>/sendMessage`, `/sendDocument`, `/getUpdates` |
| Discord | `discord.com/api/webhooks/<id>/<token>`, `cdn.discordapp.com` attachment downloads |
| Cloud storage | `content.dropboxapi.com`, `www.googleapis.com/upload/drive`, `graph.microsoft.com` from non-Office processes |
| Paste / code | `pastebin.com/raw/`, `raw.githubusercontent.com`, `gist.githubusercontent.com` for stage or config retrieval |
Hunt for these from hosts and processes that have no business reason: servers, `powershell.exe`, `rundll32.exe`, unsigned binaries in user folders. Telegram API access from corporate endpoints where Telegram is not approved is high signal.

## Process context
- EDR network events / Sysmon 3 and 22 (DNS) give process image and command line for the connection.
- Polling patterns (`getUpdates` long-polling every few seconds) look like beacons; webhooks look like one-shot POSTs with large bodies (stolen data archives).

## Recovering tokens and scope
- Sample analysis (strings, config extraction) usually yields the bot token or webhook URL. With inspection logs, the token is in the URL path.
- A Telegram bot token identifies the bot; do not use the token to read the attacker's chat (legal and operational risk; may also alert them). Report to the platform.
- Webhook/token reuse across samples links campaigns; share via ISAC under TLP.

## Response
- Block the specific paths/tokens at the proxy where inspection exists; block the service entirely for servers.
- Report abuse: Telegram (abuse@telegram.org / in-app), Discord Trust & Safety, cloud providers' abuse forms; include token/URL and sample hashes.
- Treat data sent as exfiltrated; scope by request sizes and sample capabilities (browser credentials, wallets, files).

## Gotchas
- Blocking a popular SaaS for users causes outages; target by process or host role.
- Some malware falls back to alternate channels when one is blocked; watch for new destinations after blocking.

## Verify
Each C2 channel identified has process attribution, timing, data volume estimate and a recorded abuse report or block.
