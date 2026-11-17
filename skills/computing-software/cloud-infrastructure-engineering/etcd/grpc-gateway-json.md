---
id: computing-software.cloud-infrastructure-engineering.etcd.grpc-gateway-json
name: grpc-gateway-json
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [grpc-gateway, json, http, v3, base64, rest, curl, no-grpc-client]
level: practitioner
status: docs-checked
description: "Call etcd over HTTP/JSON through the built-in gRPC gateway at /v3/*, with base64 keys and values and curl examples."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/api_grpc_gateway/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

For languages without gRPC support, etcd provides a JSON gRPC gateway: a RESTful proxy that translates HTTP/JSON requests into gRPC messages. It accepts a JSON mapping of etcd's protocol buffer messages. `key` and `value` are byte arrays and must be base64 encoded in JSON.

Endpoint history: v3.2 and earlier use only `[CLIENT-URL]/v3alpha/*`; v3.3 uses `/v3beta/*` and keeps `/v3alpha/*`; v3.4 uses `/v3/*` and keeps `/v3beta/*` (`/v3alpha/*` deprecated); v3.5 and later use only `/v3/*`. The gateway does not support authentication using TLS Common Name.

```bash
# foo is Zm9v and bar is YmFy in base64
curl -L http://localhost:2379/v3/kv/put -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
curl -L http://localhost:2379/v3/kv/range -X POST -d '{"key": "Zm9v"}'
# prefix "foo": range_end is the base64 of "fop"
curl -L http://localhost:2379/v3/kv/range -X POST -d '{"key": "Zm9v", "range_end": "Zm9w"}'
curl -N http://localhost:2379/v3/watch -X POST -d '{"create_request": {"key":"Zm9v"} }'
```

- Services in the guide: `/v3/kv/range`, `/v3/kv/put`, `/v3/kv/txn`, `/v3/watch` and the `/v3/auth/*` calls (`user/add`, `role/add`, `user/grant`, `enable`, `authenticate`).
- Transactions use `compare` entries (for example target `CREATE` with `createRevision`, or `VERSION` with `EQUAL`) plus `success` blocks such as `requestPut` or `requestRange`.
- Watch responses stream back wrapped in a `result` object, with `created` set on the first and `events` on later ones.
- Authentication: enable auth after creating a root user and role, call `/v3/auth/authenticate` with name and password, then pass the returned `token` in the `Authorization` header.
- In the examples, int64 values such as revisions appear as strings.
- Generated Swagger definitions are published with the docs (`rpc.swagger.json`).

## Checked

2026-11-08. Read the v3.5 gRPC gateway page in full. Confirmed: base64 requirement, endpoint history by version, no TLS Common Name auth, put, range, watch, txn and auth examples, Swagger. Corrected: the version history (v3.4 uses /v3, v3.5 only /v3). Removed: deleterange, lease and maintenance endpoint claims, the -L redirect reason and the gRPC-faster remark.

Method: documentation only; no commands were run.
