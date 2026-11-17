---
id: computing-software.qa-testing-engineering.jmeter-k6.xk6-custom-k6-builds
name: xk6-custom-k6-builds
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6, xk6, k6-extensions, k6-outputs, custom-binary, k6-sql, k6-kafka]
level: practitioner
status: gated
description: "Extend k6 with xk6: build a custom binary with extensions (Kafka, SQL, Redis, outputs), pin versions, run it in CI via Docker, and know when extensions are unnecessary."
sources:
  - https://grafana.com/docs/k6/latest/extensions/
  - https://github.com/grafana/xk6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom k6 builds with xk6

**Goal:** add protocols or outputs k6 lacks (Kafka, SQL, MQTT, custom outputs) via Go extensions.

## Build
```bash
go install go.k6.io/xk6/cmd/xk6@latest       # the xk6 README now shows go.k6.io/xk6@latest; both installed xk6 1.4.14
xk6 build v0.54.0 \
  --with github.com/mostafa/xk6-kafka@v0.27.0 \
  --with github.com/grafana/xk6-sql@v1.0.0 \
  --output ./k6-custom
./k6-custom version         # lists bundled extensions
```
Run on Windows (Go 1.22.5, xk6 1.4.14): this exact build succeeded in about 2 minutes and `k6-custom version` printed `k6-custom.exe v0.54.0` with `github.com/grafana/xk6-sql v1.0.0, k6/x/sql [js]` and `github.com/mostafa/xk6-kafka v0.27.0, k6/x/kafka [js]`. Both extension tags exist. These pins are old: at check time the latest releases were xk6-kafka v2.2.0, xk6-sql v1.2.3 and k6 v2.3.0 (its `go.mod` requires Go 1.26.0; a build of xk6-kafka v2.2.0 with the default k6 failed on this Go 1.22.5 machine with a compile error, cause not investigated).
Docker (no Go locally) (gated: unconfirmed, source is paywalled or blocked; Docker is not available to run here, the form matches the xk6 README):
```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/xk6" grafana/xk6 build v0.54.0 --with github.com/mostafa/xk6-kafka
```

## Use
```js
import { Writer, SchemaRegistry, SCHEMA_TYPE_STRING } from 'k6/x/kafka'
const writer = new Writer({ brokers: ['kafka:9092'], topic: 'orders' })
const schemaRegistry = new SchemaRegistry()
export default () => writer.produce({ messages: [{
  value: schemaRegistry.serialize({ data: 'order-42', schemaType: SCHEMA_TYPE_STRING }),
}] })
export function teardown() { writer.close() }
```
A plain string `value: 'order-42'` fails in xk6-kafka v0.27.0 with `GoError: illegal base64 data at input byte 5` (run): message keys and values are byte arrays, so serialise them as the README does, as above (`serialize` returned an 8-element array for `order-42`). Against a closed port the fixed script reached the network layer and failed with `Error writing messages., OriginalError: dial tcp ... connection refused`. A real broker round trip (gated: unconfirmed, source is paywalled or blocked; no Kafka broker available here) was not run.
Extensions register JS modules under `k6/x/<name>` or new outputs (`-o xk6-...`).

## Practice
- Pin k6 and extension versions; publish the binary as a CI artifact or container image.
- Check the extension registry for maintenance status; many community extensions lag k6 releases.
- k6 1.2.0 and later resolve extensions automatically: running a script that imports `k6/x/faker` on k6 2.3.0 logged `Automatic extension resolution is enabled`, downloaded a custom binary (k6 v2.3.0 + k6/x/faker v0.5.2, about 10 s) into the user cache and ran. The docs say it works only for official and community extensions; `K6_AUTO_EXTENSION_RESOLUTION=false` disables it (run: then `unknown modules ["k6/x/faker"]`), and `k6 deps script.js` lists what a script needs. Check this before maintaining your own build.

## Gotchas
- An extension compiled against a different k6 API version fails to build or panics; match versions.
- Before building, check whether core k6 already covers it (gRPC, WebSockets, browser, many experimental modules ship built in).

## Verify
`./k6-custom version` shows the extensions; a smoke script using them runs in CI with the custom image.
