---
id: computing-software.web-development.sveltekit.sveltekit-adapter-node-lifecycle-and-custom-server
name: sveltekit-adapter-node-lifecycle-and-custom-server
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-node, graceful-shutdown, socket-activation, custom-server]
level: advanced
status: docs-checked
description: "Handle shutdown events, systemd socket activation and a custom Express server using adapter-node build output."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/40-adapter-node.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control how an `adapter-node` server starts, stops and is embedded.

## Graceful shutdown
On `SIGTERM` or `SIGINT` the server: (1) rejects new requests (`server.close`), (2) waits for in-flight requests and closes idle connections (`server.closeIdleConnections`), (3) after `SHUTDOWN_TIMEOUT` seconds closes whatever remains (`server.closeAllConnections`).

Listen for `sveltekit:shutdown`, emitted after all connections close. Unlike Node's `exit`, it supports async work and always fires, even with dangling work such as open DB connections:

```js
process.on('sveltekit:shutdown', async (reason) => {
	await jobs.stop();
	await db.close();
});
```
`reason` is `SIGINT`, `SIGTERM`, or `IDLE` (triggered by `IDLE_TIMEOUT`).

## systemd socket activation
The OS passes `LISTEN_PID` and `LISTEN_FDS`; the adapter listens on file descriptor 3, which refers to a socket unit you create (only a single socket is accepted). `envPrefix` still works, but those two are always read without a prefix.

1. Service unit. With `IDLE_TIMEOUT` the app sleeps after that many seconds without requests and systemd restarts it on demand; if unset the app runs continuously:
```ini
[Service]
Environment=NODE_ENV=production IDLE_TIMEOUT=60
ExecStart=/usr/bin/node /usr/bin/myapp/build
```
2. Socket unit:
```ini
[Socket]
ListenStream=3000

[Install]
WantedBy=sockets.target
```
3. Run `sudo systemctl daemon-reload`, then `sudo systemctl enable --now myapp.socket`. The app starts on the first request to `localhost:3000`.

## Custom server
The build directory has `index.js` (starts the server; `node build`) and `handler.js`, which exports a handler for Express, Connect, Polka or `http.createServer`:

```js
import { handler } from './build/handler.js';
import express from 'express';

const app = express();

// add a route that lives separately from the SvelteKit app
app.get('/healthcheck', (req, res) => {
	res.end('ok');
});

// let SvelteKit handle everything else, including prerendered pages and static assets
app.use(handler);

app.listen(3000, () => {
	console.log('listening on port 3000');
});
```

## Gotcha
With `handler.js` only `PROTOCOL_HEADER`, `HOST_HEADER`, `PORT_HEADER`, `ADDRESS_HEADER`, `XFF_DEPTH` and `BODY_SIZE_LIMIT` take effect. `PORT`, `HOST`, `SOCKET_PATH`, `SHUTDOWN_TIMEOUT`, `IDLE_TIMEOUT`, `KEEP_ALIVE_TIMEOUT`, `HEADERS_TIMEOUT`, `LISTEN_PID` and `LISTEN_FDS` only apply to `node build`; implement them yourself (the snippet above listens on a hardcoded 3000).

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/40-adapter-node.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
