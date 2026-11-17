---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-updater-signing-keys
name: tauri-updater-signing-keys
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-updater-signing-keys, tauri-updater, tauri, tauri2, updater, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Generate Tauri updater signing keys, set pubkey and endpoints, and build with createUpdaterArtifacts."
sources:
  - https://v2.tauri.app/plugin/updater/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri updater signing keys

**Goal:** signed updates only.

```bash
npm run tauri signer generate -- -w ~/.tauri/myapp.key
export TAURI_SIGNING_PRIVATE_KEY="Path or content of your private key"
export TAURI_SIGNING_PRIVATE_KEY_PASSWORD=""        # optional
npm run tauri build
```

```json
// tauri.conf.json
{
  "bundle": { "createUpdaterArtifacts": true },
  "plugins": { "updater": {
    "pubkey": "CONTENT FROM PUBLICKEY.PEM",
    "endpoints": ["https://releases.myapp.com/{{target}}/{{arch}}/{{current_version}}"]
  } }
}
```

**Gotcha:** losing the private key means you cannot publish updates to apps already installed, so store it safely and never share it. `pubkey` must be the key content, not a file path, and `.env` files do not supply the private key variable. The signature field in the update JSON must be the contents of the `.sig` file, not a path or URL. Endpoints must use TLS in production, and the next endpoint is tried only after a non-2XX status.

## Verify
- A build produces `.sig` files next to the update bundles and the app accepts the update.

## Checked
2026-11-03. Confirmed in the Tauri updater plugin page: `signer generate -w`, the two environment variables, `createUpdaterArtifacts`, `pubkey` as content not a path, `endpoints` with `{{target}}`, `{{arch}}` and `{{current_version}}`, TLS enforcement and fall-through on non-2XX, `.env` not working, the lost-key warning, and the `signature` rule. Removed: the "secret manager" advice (the page only says to store the key somewhere safe).
Method: documentation only; no commands were run.
