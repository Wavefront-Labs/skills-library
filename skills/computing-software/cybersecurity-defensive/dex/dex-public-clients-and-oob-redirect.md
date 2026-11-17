---
id: computing-software.cybersecurity-defensive.dex.dex-public-clients-and-oob-redirect
name: dex-public-clients-and-oob-redirect
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [public-clients, redirect-uri, static-clients, oob]
level: practitioner
status: docs-checked
description: "Declare public Dex clients with public true, and handle the localhost and urn:ietf:wg:oauth:2.0:oob redirect rules."
sources:
  - https://dexidp.io/docs/configuration/custom-scopes-claims-clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Public clients are modelled on Google's "Installed Applications" and impose restrictions on apps that cannot keep a client secret private. Declare one with the `public` option:

```yaml
staticClients:
- id: cli-app
  public: true
  name: 'CLI app'
  redirectURIs:
  - ...
```

If no `redirectURIs` are specified, a public client only supports redirects that begin with `http://localhost`, or the special out-of-browser URL `urn:ietf:wg:oauth:2.0:oob`.

The out-of-browser URL makes Dex display the OAuth2 code in the browser so the user copies it into the app. The client must supply a screen or prompt to receive the code, then exchange it for a token.

Gotcha: with the out-of-browser flow, an ID token nonce is strongly recommended.

## Checked

2026-11-08: Read the Dex Scopes and Claims page in full. Confirmed public clients, the `public` option, the localhost and out-of-browser redirect rules, the code display behaviour and the nonce recommendation. Removed the token exchange and password grant paragraphs, which that page does not state.
Method: documentation only; no commands were run.
