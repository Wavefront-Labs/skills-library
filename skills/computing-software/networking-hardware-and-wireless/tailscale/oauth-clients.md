---
id: computing-software.networking-hardware-and-wireless.tailscale.oauth-clients
name: oauth-clients
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [oauth-clients, api-scopes, token-endpoint]
level: advanced
status: docs-checked
description: "Create scoped OAuth clients and request short-lived API access tokens."
sources: ["https://tailscale.com/kb/1215"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OAuth clients

Goal: give automation scoped API access without a personal API key.

**Create.** Owner, Admin, Network admin or IT admin: Trust credentials page, Credential, OAuth, pick Read or Write for each scope, Generate credential. Copy the client ID and secret immediately; the secret cannot be viewed after you close the page. Secrets are case-sensitive.

**Permissions.** Owners and Admins can pick any scope and tag. Other roles can only grant scopes and tags they hold themselves.

**Tokens.**

- Token endpoint: `https://api.tailscale.com/api/v2/oauth/token`.
- Access tokens expire after one hour; request a new one shortly before expiry. Client libraries can do this.
- Implementation follows OAuth 2.0.
- Scopes limit tokens to needed endpoints; `dns:read` can call only the DNS nameservers, preferences and searchpaths GETs plus `keys/:keyID` for itself.

**Lifetime.** A client keeps working after the creating user loses access to the tailnet. Admins can view all clients on the Trust credentials page.

OAuth clients can be used with the API to create auth keys programmatically.

**Checklist**

1. Minimum scopes.
2. Secret in a secret store.
3. Renew tokens before the hour is up.

## Checked

2026-11-03. Read OAuth clients (kb/1215) and confirmed creation roles, one-hour token expiry, token endpoint and scope restriction rules. Nothing else was removed.

Method: documentation only; no commands were run.
