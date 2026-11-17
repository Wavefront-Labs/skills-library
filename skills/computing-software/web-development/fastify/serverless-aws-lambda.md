---
id: computing-software.web-development.fastify.serverless-aws-lambda
name: serverless-aws-lambda
category: computing-software
field: web-development
product: fastify
tags: [fastify, serverless, aws, lambda, api-gateway]
level: practitioner
status: docs-checked
description: "Deploy Fastify on AWS Lambda with @fastify/aws-lambda while keeping local node app.js development."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Serverless.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two options: `@fastify/aws-lambda` (API Gateway only, optimized for Fastify) or `@h4ad/serverless-adapter` (slower because it builds an HTTP request per event, supports SQS, SNS and more).

app.js exports the builder when required and listens when run directly:

```js
const fastify = require('fastify')
function init () {
  const app = fastify()
  app.get('/', (request, reply) => reply.send({ hello: 'world' }))
  return app
}
if (require.main === module) {
  init().listen({ port: 3000 }, (err) => { if (err) console.error(err) })
} else {
  module.exports = init
}
```

lambda.js:

```js
const awsLambdaFastify = require('@fastify/aws-lambda')
const init = require('./app')
const proxy = awsLambdaFastify(init(), { binaryMimeTypes: ['application/octet-stream'] })
exports.handler = proxy
```

Install `npm i @fastify/aws-lambda`.

Limits: API Gateway does not support streams, so you cannot return a stream reply. API Gateway has a 29 second timeout, so reply within it. Netlify Functions reuse this: re-export `handler` from `lambda.js` in `functions/server.js`, add a webpack config using `webpack-node-externals`, and a `build:functions` script.

Gotcha: the bigger the app, the slower the cold start. Prefer container platforms (Cloud Run, Fargate, Azure Container Instances, Vercel) which handle concurrent requests.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Serverless.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
