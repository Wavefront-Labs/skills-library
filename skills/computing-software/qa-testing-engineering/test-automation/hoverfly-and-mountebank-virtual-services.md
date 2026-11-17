---
id: computing-software.qa-testing-engineering.test-automation.hoverfly-and-mountebank-virtual-services
name: hoverfly-and-mountebank-virtual-services
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [hoverfly, mountebank, service-virtualization, http-stubbing, capture-simulate, imposters]
level: practitioner
status: verified
description: "Virtualise dependencies with Hoverfly (capture and simulate modes, middleware) and Mountebank (imposters, predicates, multi-protocol), and choose between them and WireMock."
sources:
  - https://docs.hoverfly.io/
  - https://www.mbtest.dev/
  - https://wiremock.org/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hoverfly and Mountebank virtual services

**Goal:** stand in for unavailable, costly or unstable dependencies with virtual services that tests and teams can share.

## Hoverfly
A proxy-based tool (Go) controlled by `hoverctl`.
```bash
hoverctl start
hoverctl mode capture                  # record real traffic passing through the proxy
curl --proxy http://localhost:8500 https://api.partner.example/rates
hoverctl export simulation.json        # save request/response pairs
hoverctl import simulation.json
hoverctl mode simulate                 # replay without the real service
```
- Modes: capture, simulate, spy (simulate matched, pass through unmatched), synthesize (middleware generates responses), modify, diff (compare real responses with the simulation, useful for drift).
- Hoverfly also has request matchers, state, templating and middleware; see https://docs.hoverfly.io/ for the current list (not checked here). Run with Hoverfly v1.12.16 on Windows: `hoverctl start` (proxy 8500, admin 8888), `mode capture`, a request through `--proxy http://localhost:8500`, `export`, `mode simulate`, `import`, replay: all worked; an unmatched request in simulate mode returned 502, and in spy mode it passed through to the real server.

## Mountebank
Node-based, multi-protocol (HTTP/HTTPS/TCP/SMTP) "imposters" configured via REST on port 2525.
```bash
mb &            # npm i mountebank (v2.9.1 tested); stop with `mb stop`
curl -X POST localhost:2525/imposters -H 'Content-Type: application/json' -d '{
  "port": 4545, "protocol": "http",
  "stubs": [{ "predicates": [{ "equals": { "method": "GET", "path": "/rates" } }],
              "responses": [{ "is": { "statusCode": 200, "body": {"usd": 1.0} } },
                            { "is": { "statusCode": 503 } }] }]
}'
```
- Responses in an array cycle in order (checked: 200, 503, 200 on three calls); a request that matches no stub gets the default 200 with an empty body, so it does NOT fail loudly unless you set `"defaultResponse": {"statusCode": 404}` on the imposter (checked); `proxy` responses can record; `_behaviors` add `wait` (latency; 500 ms added about 0.5 s), `decorate` and `copy` (`decorate` is injection and needs `mb --allowInjection`; without it the imposter POST returned 400). `tcp` and `smtp` imposters were created successfully.
- Delete imposters between tests: `curl -X DELETE localhost:2525/imposters/4545`.

## Choosing
- WireMock: richest HTTP features and ecosystem, Java and standalone.
- Hoverfly: proxy-based capture/simulate and diff mode for fast recording of many endpoints.
- Mountebank: non-HTTP protocols (TCP) and language-agnostic REST control.

## Verify
Tests pass with the real dependency disconnected, simulations are versioned with the tests, and unmatched requests fail loudly (Hoverfly simulate mode: 502; Mountebank: set `defaultResponse`).
