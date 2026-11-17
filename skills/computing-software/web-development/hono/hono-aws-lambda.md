---
id: computing-software.web-development.hono.hono-aws-lambda
name: hono-aws-lambda
category: computing-software
field: web-development
product: hono
tags: [hono, aws-lambda, cdk, serverless, streaming]
level: practitioner
status: docs-checked
description: "Deploy Hono to AWS Lambda with @hono/aws-lambda and CDK: handle, function URL, binary responses, event and context bindings, response streaming."
sources:
  - https://github.com/honojs/website/blob/main/docs/getting-started/aws-lambda.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono on AWS Lambda

Node.js 18+ runtime. Scaffold with CDK:

```sh
mkdir my-app && cd my-app
cdk init app -l typescript
npm i hono @hono/aws-lambda
npm i -D esbuild
mkdir lambda && touch lambda/index.ts
```

```ts
// lambda/index.ts
import { Hono } from 'hono'
import { handle } from '@hono/aws-lambda'
const app = new Hono()
app.get('/', (c) => c.text('Hello Hono!'))
export const handler = handle(app)
```

## CDK stack (lib/my-app-stack.ts)
```ts
const fn = new NodejsFunction(this, 'lambda', {
  entry: 'lambda/index.ts',
  handler: 'handler',
  runtime: lambda.Runtime.NODEJS_22_X,
})
const fnUrl = fn.addFunctionUrl({ authType: lambda.FunctionUrlAuthType.NONE })
new cdk.CfnOutput(this, 'lambdaUrl', { value: fnUrl.url! })
```
Deploy with `cdk deploy`.

## Binary responses
Set a binary `Content-Type` and Hono base64-encodes automatically:

```ts
c.status(200)
c.header('Content-Type', 'image/png')
return c.body(buffer)
```

## Lambda event and context
```ts
import type { LambdaEvent, LambdaContext } from '@hono/aws-lambda'
type Bindings = { event: LambdaEvent; lambdaContext: LambdaContext }
const app = new Hono<{ Bindings: Bindings }>()
app.get('/info', (c) => c.json({ awsRequestId: c.env.lambdaContext.awsRequestId }))
```
Request context: `c.env.event.requestContext`. The older `ApiGatewayRequestContext` binding (`c.env.requestContext`) is deprecated before v3.10.0.

## Response streaming
Add `invokeMode: lambda.InvokeMode.RESPONSE_STREAM` to `addFunctionUrl`, and export `streamHandle(app)` instead of `handle(app)`; handlers use `streamText` from `hono/streaming`.

## Gotcha
For streaming the page changes two things: `invokeMode: lambda.InvokeMode.RESPONSE_STREAM` on the function URL, and `streamHandle` instead of `handle`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/getting-started/aws-lambda.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the "not interchangeable" inference (reworded to what the page shows).

Method: documentation only; no commands were run.
