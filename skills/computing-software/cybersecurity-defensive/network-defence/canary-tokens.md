---
id: computing-software.cybersecurity-defensive.network-defence.canary-tokens
name: canary-tokens
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [deception-technology, canarytokens, canary-tokens, web-bug, dns-token, decoy-documents, breach-detection, thinkst-canary]
level: practitioner
status: draft
description: "Use canary tokens (DNS, web bug, document, AWS key, cloned-site) to detect access to files, repositories and systems, with self-hosting and alert hygiene."
sources: ["Thinkst Canarytokens documentation (canarytokens.org, open source canarytokens-docker)", "MITRE D3FEND Decoy Object techniques", "CompTIA Security+ SY0-701 objective 1.2"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Canary tokens

**Goal:** cheap tripwires that tell you when someone opens a file, reads a config, uses a
credential or clones your login page.

## Token types (Thinkst Canarytokens)
| Token | Trigger | Use |
|---|---|---|
| DNS | Resolution of a unique hostname | Embed in configs, scripts, connection strings |
| Web bug (URL) | HTTP request | Docs, emails, internal wiki pages |
| MS Word / PDF document | Opening the file (remote resource callback) | Decoy "passwords" or "M&A" documents on shares |
| AWS API key | Any API call with the key | CI configs, developer laptops, Git repos |
| Cloned website (JS) | Your login page served from another domain | Phishing kit detection |
| SQL Server / MySQL dump | Restoring/loading the dump | Database backup theft |
| Windows folder (desktop.ini) | Browsing the folder | Sensitive shares |
| Kubeconfig, WireGuard config, credit card | Use of the fake item | Various |

## Deploy
- Generate at canarytokens.org (free, alerts by email/webhook) or **self-host** with
  `canarytokens-docker` so tokens use your own domain and alert data stays internal.
- Name and place tokens where attackers look: `backup-creds.docx` on file servers, `.aws/credentials` on admin laptops, fake keys in private repos.
- Record each token: location, type, memo (the memo is included in the alert).

## Alerts
Send webhooks to the SIEM/SOAR. Each alert shows source IP and user agent (for HTTP), or
resolver IP (for DNS - resolver, not attacker, unless they resolve directly).

## Gotchas
- Document tokens fire when anyone opens the file: backup scanners, DLP, search indexers and AV previews can trigger them. Expect initial noise, tune placements.
- Office protected view and offline readers block the callback, so document tokens do not always fire.
- DNS tokens leak your token domain; self-hosting on a neutral-looking domain avoids revealing them as canaries.

## Verify
- [ ] Each deployed token has been triggered once in a test and the alert reached the SOC.
- [ ] Register of tokens with locations kept current.
