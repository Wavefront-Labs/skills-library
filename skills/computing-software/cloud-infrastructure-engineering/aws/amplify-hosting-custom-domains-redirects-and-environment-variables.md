---
id: computing-software.cloud-infrastructure-engineering.aws.amplify-hosting-custom-domains-redirects-and-environment-variables
name: amplify-hosting-custom-domains-redirects-and-environment-variables
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, amplify, amplify-hosting, amplify-redirects, amplify-custom-domain, spa-rewrites, amplify-environment-variables]
level: practitioner
status: gated
description: "Configure Amplify Hosting: custom domains and branch subdomains, rewrites and redirects (SPA rule, 301s, proxies), and build-time environment variables and secrets."
sources: ["https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html", "https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html", "https://docs.aws.amazon.com/amplify/latest/userguide/environment-variables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amplify Hosting: custom domains, redirects and environment variables

## Custom domains
- Domain in Route 53 in the same account: Amplify adds records and an ACM certificate automatically. (gated: unconfirmed, source is paywalled or blocked)
- External DNS: add the verification CNAME and a CNAME per subdomain at your DNS provider, as shown in the Amplify console. (gated: unconfirmed, source is paywalled or blocked)
- Map branches to subdomains (`main` -> `www`, `dev` -> `dev`); enable automatic subdomains for
  pattern-based branches (feature previews). (gated: unconfirmed, source is paywalled or blocked)

## Rewrites and redirects (console JSON or `customRules`)
```json
[
 {"source":"https://example.com","target":"https://www.example.com","status":"301"},
 {"source":"/docs/<*>","target":"/guide/<*>","status":"301"},
 {"source":"/api/<*>","target":"https://api.example.com/<*>","status":"200"},
 {"source":"</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|woff2|ttf|map|json|webp)$)([^.]+$)/>",
  "target":"/index.html","status":"200"}
]
```
- Order matters: first match wins; put specific rules above the SPA catch-all.
- `200` is a rewrite (content shown without changing the URL), `301` a permanent redirect, `404` a not-found page.
- The SPA regex rule sends deep links like `/orders/42` to `index.html` without catching assets. (gated: unconfirmed, source is paywalled or blocked)
- SSR (Next.js) apps handle routing in the framework; use framework config there.

## Environment variables and secrets
- Set per app or per branch in the console or `aws amplify update-branch --environment-variables KEY=v`.
- Available at build time; a static site only gets what the build bakes in. Never put secrets in client-bundled variables. (gated: unconfirmed, source is paywalled or blocked)
- Secrets: do not store secrets in environment variables; for a Gen 2 app use the Secret management feature in the Amplify console. For SSR runtime, write only needed non-secret values into `.env.production` during build: (gated: unconfirmed, source is paywalled or blocked)
```yaml
build:
  commands:
    - env | grep -e DB_URL >> .env.production
    - npm run build
```
- Variable names with an `AWS` prefix cannot be created (reserved for Amplify internal use); a variable value can't exceed 5500 characters.

## Verify
- [ ] `curl -I https://example.com` returns 301 to www; deep link refresh returns the app, not 404.
- [ ] Branch subdomains resolve with valid certificates.
- [ ] Secret values are absent from the built JS bundle (`grep` the artifacts).

## Checked

2026-10-28

Confirmed: Amplify default domain and custom domain connection, 301 permanent redirect, 200 rewrite, 404 rewrite rule, <*> wildcard syntax, redirect order matters, AWS prefix reserved, 5500-character value limit, secrets must not live in environment variables (Amplify User Guide pages); update-branch --environment-variables (check_commands).

Removed: SSM Parameter Store secret path and process.env.secrets (contradicted by the guide), CAA/pending-verification troubleshooting, apex ALIAS/ANAME claim, 302 and 404-200 types, NEXT_PUBLIC_/VITE_ names, amplify.yml wording.

Gated: Route 53 auto-configuration, external DNS records, branch subdomains, the SPA regex rule and the build-time variable detail: the custom-domain and redirect pages fetched are short and do not state them.

Method: documentation only; no commands were run.
