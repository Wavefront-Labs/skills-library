---
id: computing-software.web-development.trpc.aws-lambda-adapter
name: aws-lambda-adapter
category: computing-software
field: web-development
product: trpc
tags: [trpc, aws-lambda, api-gateway, awslambdarequesthandler, serverless]
level: advanced
status: docs-checked
description: "Run tRPC on API Gateway REST or HTTP API and Lambda Function URLs; mind payload version 1 vs 2 and one greedy resource for batch links."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/aws-lambda.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The AWS Lambda adapter supports API Gateway REST API (v1), HTTP API (v2) and Lambda Function URLs.

```ts
import { awsLambdaRequestHandler } from '@trpc/server/adapters/aws-lambda';
import type { CreateAWSLambdaContextOptions } from '@trpc/server/adapters/aws-lambda';

const createContext = ({ event, context }: CreateAWSLambdaContextOptions<APIGatewayProxyEventV2>) => ({});

export const handler = awsLambdaRequestHandler({ router: appRouter, createContext });
```

Payload format: REST APIs use version 1.0 (`APIGatewayProxyEvent`); HTTP APIs can choose 1.0 or 2.0 (`APIGatewayProxyEventV2`). Supply the matching event type to `CreateAWSLambdaContextOptions<...>` so `event` is typed correctly.

`httpBatchLink` requires the router to live on a single API Gateway resource. A batch puts several procedures in one path (`/getUser,createUser`), which per-procedure resources do not match. Use one greedy resource such as `/trpc/{proxy+}`, from which tRPC reads the procedure path, or use `httpLink` instead if you want a resource per procedure.

The default `awsLambdaRequestHandler` buffers the whole response before returning it. See the response streaming skill for streaming.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters/aws-lambda.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
