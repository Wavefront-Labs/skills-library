---
id: computing-software.web-development.trpc.trpc-error-codes-http-map
name: trpc-error-codes-http-map
category: computing-software
field: web-development
product: trpc
tags: [trpc, trpcerror, error-codes, http-status, gethttpstatuscodefromerror]
level: practitioner
status: docs-checked
description: "The tRPC error code list with HTTP statuses (BAD_REQUEST 400, UNAUTHORIZED 401, FORBIDDEN 403, NOT_FOUND 404 ...) and getHTTPStatusCodeFromError."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each tRPC error code maps to an HTTP status:

- PARSE_ERROR 400 (invalid JSON or parse failure), BAD_REQUEST 400
- UNAUTHORIZED 401 (missing valid credentials), PAYMENT_REQUIRED 402, FORBIDDEN 403
- NOT_FOUND 404, METHOD_NOT_SUPPORTED 405, TIMEOUT 408, CONFLICT 409
- PRECONDITION_FAILED 412, PAYLOAD_TOO_LARGE 413, UNSUPPORTED_MEDIA_TYPE 415
- UNPROCESSABLE_CONTENT 422, PRECONDITION_REQUIRED 428, TOO_MANY_REQUESTS 429
- CLIENT_CLOSED_REQUEST 499
- INTERNAL_SERVER_ERROR 500, NOT_IMPLEMENTED 501, BAD_GATEWAY 502, SERVICE_UNAVAILABLE 503, GATEWAY_TIMEOUT 504

Extract the HTTP code from an error with the helper:

```ts
import { TRPCError } from '@trpc/server';
import { getHTTPStatusCodeFromError } from '@trpc/server/http';

if (error instanceof TRPCError) {
  const httpCode = getHTTPStatusCodeFromError(error);
  console.log(httpCode); // 400 for BAD_REQUEST
}
```

This is useful when you call procedures server-side (the Server Side Calls docs show a custom Next.js API endpoint) and want to forward the matching status to your own HTTP response.

From the table descriptions: UNAUTHORIZED means the request lacks valid authentication credentials, FORBIDDEN means the client is not authorized to access the resource, NOT_FOUND means the server cannot find the resource, CONFLICT means a conflict with the current state of the target resource, and TOO_MANY_REQUESTS means the rate limit has been exceeded.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/error-handling.md (read in full): all 21 rows of the error code table were compared one by one with the skill list (codes and HTTP statuses match), plus the `getHTTPStatusCodeFromError` snippet; www/v11/docs/server/server-side-calls.md (read in full) for the Next.js endpoint example.

Removed or corrected: the "webhook" use case and the unsourced "choose codes deliberately" advice (replaced by the table descriptions), and the invented Verify step.

Method: documentation only; no commands were run.
