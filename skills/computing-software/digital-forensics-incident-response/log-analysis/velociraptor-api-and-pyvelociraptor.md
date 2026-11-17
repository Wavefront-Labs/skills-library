---
id: computing-software.digital-forensics-incident-response.log-analysis.velociraptor-api-and-pyvelociraptor
name: velociraptor-api-and-pyvelociraptor
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-api, pyvelociraptor, velociraptor, grpc-api, automation, dfir]
level: advanced
status: docs-checked
description: "Drive Velociraptor programmatically: create an API client config, grant least-privilege roles, run VQL over gRPC with pyvelociraptor, and fetch results for SOAR or case tools."
sources: ["https://docs.velociraptor.app/docs/server_automation/server_api/", "https://github.com/Velocidex/pyvelociraptor", "https://docs.velociraptor.app/docs/deployment/references/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Velociraptor API and pyvelociraptor

Velociraptor exposes a gRPC API on which you send VQL and stream results back. Everything the GUI does is VQL, so the API can schedule collections, launch hunts, read results and manage users from SOAR playbooks, case platforms or scripts. The pyvelociraptor project documents two endpoints: `Query` (run VQL, receive JSON results) and `VFSGetBuffer` (read buffers from the server file store).

## Enable and create a client
1. In `server.config.yaml`, the `API` section sets `bind_address` and `bind_port` (8001 in the docs example). By default the API listens only on 127.0.0.1; set `bind_address` to expose it to external callers, and firewall it. The API connection string written into the client config is built from the server's API hostname and bind settings, so set them correctly before generating the client config.
2. Create an API client certificate and config:
```bash
velociraptor --config server.config.yaml config api_client --name soar-bot --role investigator,api api.config.yaml
```
`--role` assigns roles at creation (and creates the user if missing; the docs say a new user needs a server restart before the server recognises it). The minimum role for an external connection is `api`; add roles for the permissions the program needs. The docs advise against giving external programs `administrator`; choose the least-permission role (documented roles include `reader`, `analyst`, `investigator`, `administrator`).
3. Change roles later with `velociraptor --config server.config.yaml acl grant soar-bot --role investigator,api`. `acl grant` replaces existing roles rather than adding, and CLI role changes need a service restart (GUI or VQL changes do not). Inspect with `acl show <name>`. If credentials leak, `acl grant <name> --role ""` removes all roles.
4. Protect `api.config.yaml`: it holds key material that authenticates as that identity. The client certificate is valid for 1 year; issue a new config before it expires.

## pyvelociraptor
```bash
pip install pyvelociraptor
pyvelociraptor --config api.config.yaml "SELECT * FROM info()"
```
The package ships a command line tool plus sample programs in its repository: `client_example.py` (run a query and print results and logs), `fetch.py` (fetch a file from the file store in chunks via `VFSGetBuffer`) and `fetch_flow_uploads.py` (create a flow export and download it). Start from those rather than writing gRPC setup by hand. The velociraptor binary also has a built-in API client: `velociraptor --api_config api.config.yaml query "SELECT * FROM info()" --format jsonl`.

## Passing data safely
Do not interpolate data into the VQL string (the docs call this VQL injection). Pass values as environment variables, for example `--env MyVar=value` on the built-in client, and refer to the variable by name in the query. A constant query can live in a file passed with `-f`.

## Typical automations
- Schedule a collection with `collect_client()`, which returns a flow id because collection is asynchronous; wait with `watch_monitoring(artifact='System.Flow.Completion')`; read results with `source()`. The server API page shows this as a single query.
- Nightly export of hunt results to a data lake.
- Bulk user or label management from an asset feed.

## Gotchas
- API actions are audited as the API identity; name identities per integration so audit trails make sense.
- Long-running queries stream; handle partial responses and timeouts.
- The `api_connection_string` in the client config must name an address reachable from the automation host.

## Verify
`SELECT * FROM info()` succeeds with the API config, a test collection scheduled via API appears in the GUI, and the identity cannot perform actions above its role.

## Checked
2026-11-01. Confirmed against the Velociraptor Server API page, the pyvelociraptor README and the configuration reference: default 127.0.0.1 bind, port 8001 in examples, `config api_client --name --role`, `api` minimum role, `acl grant --role` replace semantics and restart note, `acl show`, one-year certificate, `--api_config query`, `--env`, `collect_client`/`watch_monitoring`/`source` flow, sample program names, role names. Removed: the hand-written Python gRPC snippet, the `clients(search=...)` example and the `flows()` polling claim (not on the fetched pages).
Method: documentation only; no commands were run.
