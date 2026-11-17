---
id: computing-software.cryptography-implementation.protocol-implementation.tls-client-interop-matrix-testing
name: tls-client-interop-matrix-testing
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, protocol-conformance, tls-interop-testing, client-matrix, testssl-client-simulation, java-tls, android, curl, compatibility-testing]
level: advanced
status: docs-checked
description: "Test a TLS configuration change against the clients you serve: log negotiated parameters in nginx and use testssl.sh client simulation, with its limits."
sources: ["https://github.com/testssl/testssl.sh/blob/3.2/doc/testssl.1.md", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS client interop matrix testing

Tightening TLS (dropping cipher suites, changing certificates or key exchange groups, enabling client authentication) can break real clients that a scanner never represents. Build the test matrix from your own traffic and check it before and after the change.

## Build the matrix from logs
nginx exposes the negotiated parameters as variables in the SSL module: `$ssl_protocol`, `$ssl_cipher` and `$ssl_curve` (the curve used for the key exchange). Log them with the user agent:

```nginx
log_format tls '$remote_addr "$http_user_agent" $ssl_protocol $ssl_cipher $ssl_curve';
```

Aggregate over a representative period to see which protocol, cipher and curve combinations occur and from which clients.

## Simulate
testssl.sh `-c` / `--client-simulation` simulates a handshake with a set of standard clients (a hand-selected set retrieved from the SSL Labs API) to show which can or cannot connect, displaying the protocol, cipher and curve and whether forward secrecy applies. It is also part of the default run. The environment variable `ALL_CLIENTS=true` runs all clients (126 in the version documented).

- Client simulation data lives in the file `etc/client-simulation.txt`.
- The `--ssl-native` option makes results less accurate, especially for client simulation, so avoid it for this purpose.
- Simulation shows what would be negotiated; it does not exercise certificate validation or trust stores of those clients, so also test real client stacks against staging.

## Verify
- [ ] The matrix derives from production logs, with an owner for each legacy client.
- [ ] Client simulation runs against staging before every TLS configuration change.

## Checked
Method: docs-checked 2026-11-09 against the testssl.sh 3.2 man page (client simulation option, ALL_CLIENTS, ssl-native, data file) and the nginx ngx_http_ssl_module page (embedded variables).
Removed as unconfirmed: the "about 100 profiles" figure, JA3/JA4 and Zeek advice, the container harness table, canary rollout steps and metric names, and the Mozilla Server Side TLS source (page could not be read). The claim that simulation does not test trust stores is retained as a limitation implied by the tool's description (handshake simulation) rather than a quoted statement.
