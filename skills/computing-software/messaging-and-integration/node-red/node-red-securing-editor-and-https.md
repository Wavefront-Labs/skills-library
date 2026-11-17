---
id: computing-software.messaging-and-integration.node-red.node-red-securing-editor-and-https
name: node-red-securing-editor-and-https
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, security, adminauth, https, bcrypt, hash-pw, httpnodeauth, tls, settings-js]
level: advanced
status: docs-checked
description: "Secure Node-RED: HTTPS with key and cert, certificate refresh, adminAuth users with bcrypt hashes from hash-pw, OAuth strategies, and httpNodeAuth for HTTP nodes."
sources: ["https://nodered.org/docs/user-guide/runtime/securing-node-red"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Securing Node-RED

By default the editor is not secured: anyone who can reach its address can open it and deploy changes, which suits only a trusted network. The guide has three parts: HTTPS, securing the editor and admin API, and securing the HTTP nodes and Dashboard.

HTTPS: set `https` in the settings file to an options object with at least `key` (private key, PEM, String or Buffer) and `cert` (cert chain, PEM), for example loaded with `require("fs").readFileSync('privkey.pem')`. Since 1.1.0 `https` may be a function returning the options, optionally a Promise. To refresh certificates without a restart (since 1.1.0) you need Node.js 11 or later, `https` as a function, and `httpsRefreshInterval` set in hours. The function should generate new certificates if the current ones expire within that interval, or return `undefined` or `null` if no update is needed.

Editor and admin API: username/password or an OAuth/OpenID provider. Enable `adminAuth` with `type: "credentials"` and a `users` array of `{ username, password, permissions }`; `permissions: "*"` is everything and `"read"` is read-only. Passwords are bcrypt hashes; generate with `node-red admin hash-pw` (1.1.0 or later) or `node-red-admin hash-pw` on older versions, and paste into the settings file. A `default` property gives everyone not logged in a level of access, for example `{ permissions: "read" }`. Tokens expire after 7 days unless `sessionExpiryTime` (seconds) is set in `adminAuth`. The old `httpAdminAuth` basic-auth setting is deprecated.

External identity: `type: "strategy"` uses Passport strategies; Node-RED authentication modules exist for Twitter and GitHub. The strategy object takes `name`, `strategy`, `label`, `icon`, `options`, `verify` and `autoLogin` (redirect straight to the provider). `callbackURL` must be your editor URL plus `/auth/strategy/callback`; set `callbackMethod` to POST to use POST. The `users` list maps usernames to permissions.

HTTP In nodes: `httpNodeAuth: {user: "user", pass: "<bcrypt hash>"}` defines a single username and password for the routes; `httpStaticAuth` uses the same format for `httpStatic` content. MD5 hashes in `pass` are still accepted but not recommended.

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Securing Node-RED. Removed: the unsupported claim that adminAuth does not cover HTTP nodes (kept as a separate httpNodeAuth section) and the loose wording on editor basic authentication.

Method: documentation only; no commands were run.
