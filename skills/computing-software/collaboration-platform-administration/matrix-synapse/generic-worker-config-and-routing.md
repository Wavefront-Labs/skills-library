---
id: computing-software.collaboration-platform-administration.matrix-synapse.generic-worker-config-and-routing
name: generic-worker-config-and-routing
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, generic-worker, worker-app, worker-name, worker-listeners, routing, historical-apps]
level: advanced
status: docs-checked
description: "Configure a synapse.app.generic_worker with worker_app, worker_name and worker_listeners, route endpoint groups via the proxy, and migrate legacy apps."
sources:
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each worker has its own config file that must give three things: the worker type in `worker_app`, a unique `worker_name`, and, if it serves HTTP, a `worker_listeners` entry with an `http` listener. A listener that handles client and federation traffic needs both the `client` and `federation` resources. On Synapse 1.72 and older, workers handling `^/_matrix/client/v3/keys/upload` also needed `worker_main_http_uri`; newer versions ignore it. The docs include a full generic worker example file, exposing plain HTTP on port 8083, and your reverse proxy must route the relevant endpoints to it.

`synapse.app.generic_worker` can serve any of these groups, listed in the docs as regular expressions:

- sync requests (`/sync`, `/events`, `initialSync`);
- federation requests (`/_matrix/federation/v1/...` such as `state`, `backfill`, `make_join`, `send_join`, `invite`), plus the inbound transaction path `^/_matrix/federation/v1/send/`;
- client API calls (`createRoom`, `publicRooms`, `members`, `state`, `devices`, `search`, `capabilities`);
- the admin endpoint `^/_synapse/admin/v1/rooms/[^/]+$`;
- encryption key endpoints, registration and login, event sending, and user directory search.

Some endpoints may be handled by workers only for GET requests: push rules, account data and tags, presence, and `^/_synapse/admin/v2/users/[^/]+$`. Pagination (`/messages`) can also be moved, but all requests for one room must reach the same instance, and the purge history admin API must not be used while pagination requests are in flight.

SSO endpoints (redirect, `pick_idp`, `pick_username`, OIDC callback, SAML `authn_response`, CAS ticket) are needed only when SSO is configured and delegated authentication is off. All SSO logins must go to a single process.

Several old apps are now equivalent to the generic worker: `client_reader`, `event_creator`, `federation_reader`, `federation_sender`, `frontend_proxy`, `pusher`, `synchrotron`. To migrate, change `worker_app` in worker configs and in service files; no other config change is needed.

## Checked

Method: docs-checked 2026-11-09 against docs/workers.md (Synapse develop branch, raw markdown, read in full).
