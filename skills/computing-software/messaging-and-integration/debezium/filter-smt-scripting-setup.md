---
id: computing-software.messaging-and-integration.debezium.filter-smt-scripting-setup
name: filter-smt-scripting-setup
category: computing-software
field: messaging-and-integration
product: debezium
tags: [smt, filter, scripting, jsr223]
level: advanced
status: docs-checked
description: "Install and secure the Debezium filter SMT, and enable scripting in Debezium Server with ENABLE_DEBEZIUM_SCRIPTING."
sources:
  - https://debezium.io/documentation/reference/stable/transformations/filtering.html
  - https://debezium.io/documentation/reference/stable/operations/debezium-server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `Filter` SMT lets you drop events that do not meet an expression, instead of delivering every change to the broker. It supports JSR 223 languages (Groovy, GraalVM JavaScript) and an incubating Go option via TinyGo and WebAssembly.

Why not custom Java: it must be compiled and deployed, and every change needs a rebuild.

Setup for Kafka Connect:

1. Download the separate `debezium-scripting-<version>.tar.gz` artifact; the SMT is intentionally absent from connector archives.
2. Extract it into the Debezium plug-in directories.
3. Add a JSR 223 script engine and its libraries (Groovy needs `groovy`, `groovy-jsr223`, optionally `groovy-json`; JavaScript needs `graalvm.js` and `graalvm.js.scriptengine`), or place the compiled `.wasm` file on disk.
4. Restart Kafka Connect.

Important: after installation, any user allowed to add a connector to the instance can run scripting expressions. Secure Kafka Connect and its configuration interface before you install it.

Go option: `go get github.com/debezium/debezium-smt-go-pdk`, export a `process` function, keep an empty `main()` for the Wasm target, and compile with TinyGo (the docs use `tinygo/tinygo:0.34.0` with `-target=wasm-unknown`).

Debezium Server: scripting is disabled by default. Set the environment variable before starting the server:

```
ENABLE_DEBEZIUM_SCRIPTING=true
```

The startup script then adds the scripting JAR and the Groovy and GraalVM JavaScript engines from the distribution's `opt_lib` directory, which keeps them off the default classpath. Enable it only where configuration access is restricted.

Check: send one matching and one non-matching test event and confirm only the intended one arrives.

## Checked

2026-11-08. Confirmed against the Debezium page transformations/filtering (read in full: setup, security note, Go PDK command, TinyGo 0.34.0 build line, libraries) and the Enabling message filtering section of operations/debezium-server (ENABLE_DEBEZIUM_SCRIPTING, opt_lib, off by default). The Debezium Server page was read in part. Nothing removed.

Method: documentation only; no commands were run.
