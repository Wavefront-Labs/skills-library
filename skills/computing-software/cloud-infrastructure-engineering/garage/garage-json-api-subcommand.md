---
id: computing-software.cloud-infrastructure-engineering.garage.garage-json-api-subcommand
name: garage-json-api-subcommand
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-json-api, admin-api-v2, rpc-proxy, scripting]
level: advanced
status: docs-checked
description: "Call admin API operations without HTTP using garage json-api, which proxies through internal RPC."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/admin-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since v2.0.0 the `garage` binary has a `json-api` subcommand that invokes administration API operations without making an HTTP request. It is intended for scripting deployments.

It proxies calls through Garage's internal RPC protocol, so it needs no authentication token. The RPC connection parameters are discovered automatically to reach the locally running instance, exactly as for any other `garage` CLI command; that means it needs access to the configuration file and metadata directory like the rest of the CLI.

For calls without parameters, pass the operation name:

`garage json-api GetClusterHealth`

The reply is JSON, for example fields such as `connectedNodes`, `knownNodes` and `partitions`.

Operation names are the same as the v2 HTTP endpoints described in the OpenAPI specification (for example `GetClusterStatus` is served at `/v2/GetClusterStatus`). For HTTP use, the page suggests curl for simple calls and an SDK for advanced ones, and points to the "Build your own app" section for the SDKs.

## Checked

2026-11-04. Read the Administration API page in full. Confirmed the v2.0.0 gate, the RPC proxying and no-authentication statement, the GetClusterHealth example, the curl example, the SDK remark and the OpenAPI reference. Removed the closing local-versus-remote recommendation, which the page does not state.
Method: documentation only; no commands were run.
