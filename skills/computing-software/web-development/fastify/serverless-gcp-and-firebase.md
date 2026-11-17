---
id: computing-software.web-development.fastify.serverless-gcp-and-firebase
name: serverless-gcp-and-firebase
category: computing-software
field: web-development
product: fastify
tags: [fastify, serverless, google-cloud-functions, firebase, content-type-parser]
level: advanced
status: docs-checked
description: "Run Fastify on Google Cloud Functions and Firebase by emitting request on fastify.server and fixing the pre-parsed body."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Serverless.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Google Cloud Functions parses the body before Fastify sees it. Add a JSON parser that returns that body:

```js
fastify.addContentTypeParser('application/json', {}, (req, body, done) => {
  done(null, body.body)
})
```

Export a function that waits for readiness and hands the raw request to Fastify:

```js
const fastifyFunction = async (request, reply) => {
  await fastify.ready()
  fastify.server.emit('request', request, reply)
}
exports.fastifyFunction = fastifyFunction
```

Local: `npx @google-cloud/functions-framework --target=fastifyFunction`. Deploy: `gcloud functions deploy fastifyFunction --runtime <supported-nodejs-runtime> --trigger-http --region $GOOGLE_REGION --allow-unauthenticated`. Logs: `gcloud functions logs read`.

Firebase: wrap with `onRequest` from `firebase-functions/v2/https` and export `exports.app = onRequest(fastifyApp)`. Its parser also keeps the raw body for HMAC checks:

```js
fastify.addContentTypeParser('application/json', {}, (req, payload, done) => {
  req.rawBody = payload.rawBody
  done(null, payload.body)
})
```

Run with `firebase emulators:start --only functions`, deploy with `firebase deploy --only functions`.

Per-route observability: all traffic shows under one function. Emit structured logs from an `onResponse` hook with `request.routeOptions.url`, `request.method`, `reply.statusCode`, `reply.elapsedTime`.

Gotcha: without the Firebase content type parser the Fastify process can get stuck and stop processing requests after an `application/json` request.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Serverless.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
