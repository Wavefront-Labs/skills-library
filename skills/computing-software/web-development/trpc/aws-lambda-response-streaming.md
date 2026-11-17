---
id: computing-software.web-development.trpc.aws-lambda-response-streaming
name: aws-lambda-response-streaming
category: computing-software
field: web-development
product: trpc
tags: [trpc, aws-lambda, streaming, streamifyresponse, httpbatchstreamlink]
level: sme
status: docs-checked
description: "Stream tRPC responses from Lambda Function URLs or API Gateway REST (responseTransferMode STREAM) with awsLambdaStreamingRequestHandler wrapped in streamifyResponse."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/aws-lambda.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AWS Lambda supports response streaming through Function URLs and API Gateway REST APIs (configure the integration with `responseTransferMode: STREAM` on REST). The streaming handler signature is different: besides `event` and `context` it receives a writable `responseStream`. You must wrap it with `awslambda.streamifyResponse()`.

```ts
import { awsLambdaStreamingRequestHandler } from '@trpc/server/adapters/aws-lambda';

export const handler = awslambda.streamifyResponse(
  awsLambdaStreamingRequestHandler({ router: appRouter, createContext }),
);
```

The `awslambda` namespace is provided by the Lambda runtime; import types from `@types/aws-lambda` to augment the global namespace. A procedure that returns an async generator (for example a query using `async function*` and `yield`) then sends each value as it is yielded to clients using `httpBatchStreamLink`.

Mistakes listed in the docs:

- Forgetting `awslambda.streamifyResponse()`: Lambda then calls the handler as a regular one, with no response stream to write to.
- Expecting the default `awsLambdaRequestHandler` to stream: it buffers the whole response so `httpBatchStreamLink` results arrive all at once.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters/aws-lambda.md (Response Streaming, Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
