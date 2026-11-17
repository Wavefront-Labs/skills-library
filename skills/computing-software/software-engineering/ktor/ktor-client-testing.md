---
id: computing-software.software-engineering.ktor.ktor-client-testing
name: ktor-client-testing
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, testing, mockengine, unit-tests]
level: practitioner
status: docs-checked
description: "Test a Ktor client with MockEngine from ktor-client-mock: share config via an engine-taking wrapper, mock multiple endpoints, sequence responses with reuseHandlers and Queue."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing the Ktor client with MockEngine

`MockEngine` simulates HTTP calls without contacting a real endpoint. Add the `io.ktor:ktor-client-mock` artifact to your test dependencies.

## Share configuration with the production client

Wrap the client in a class that takes an `HttpClientEngine` in its constructor and holds the shared configuration (for example the JSON `ContentNegotiation` setup). Production passes `CIO`; tests pass a `MockEngine`.

## Write a test

Create a `MockEngine` with a handler that checks request parameters and responds with the content you need (a JSON object in the page's example). Pass it to the wrapper class and assert on the result.

## Mock multiple endpoints

Use a single reusable handler and branch on the request, for example `request.url.encodedPath` or `request.url.host`. This keeps mocks independent of call order. In the `else` branch, fail on unexpected URLs so tests do not silently accept a missing mock.

## Mock a call chain

For different responses on consecutive calls in a fixed order, register several handlers with `addHandler()` and set `reuseHandlers = false`.

- `reuseHandlers` defaults to `true`, and handlers are reused in a cycle.
- With `false`, each handler is used once; when all are used, the next request is rejected by throwing an error.

If the client is built first and responses are enqueued later, use `MockEngine.Queue`.

Full example: `client-testing-mock` in the ktor-documentation code snippets.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-testing.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
