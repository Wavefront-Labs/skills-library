---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-function-urls-and-response-streaming
name: lambda-function-urls-and-response-streaming
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, function-url, response-streaming, invoke-mode, iam-auth]
level: practitioner
status: docs-checked
description: "Expose a Lambda function through a function URL with the correct auth type and resource policy, and enable response streaming."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html", "https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html", "https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-response-streaming.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda function URLs and response streaming

**Goal:** a dedicated HTTPS endpoint for one function with no API Gateway, correctly secured.

## Create
```bash
aws lambda create-function-url-config --function-name fn --auth-type AWS_IAM --invoke-mode BUFFERED
```
- URL shape: `https://<url-id>.lambda-url.<region>.on.aws`; it never changes once created, is dual stack
  (IPv4 and IPv6), and is reachable over the public internet only (function URLs do not support PrivateLink).
- A function URL attaches to a function alias or to `$LATEST`, not to any other published version. Use `--qualifier`
  for an alias. Not available in every Region.
- The function must already exist before you create the URL with the CLI.
- CORS: `--cors-config AllowOrigins=https://app.example.com,AllowMethods=GET`. Properties: `AllowOrigins`,
  `AllowMethods`, `AllowHeaders`, `ExposeHeaders`, `AllowCredentials`, `MaxAge`. When CORS is set on the URL, Lambda
  adds the headers to all responses, so do not also send them from the function (duplicate values such as `*, *`
  break browsers on non-preflight requests).

## Auth and the resource policy
- Notice at the top of the AWS page: starting in October 2025, new function URLs require both
  `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` permissions.
- `AWS_IAM`: callers sign every request with SigV4 and need both permissions. Same account: identity policy or
  resource policy is enough. Cross account: both an identity policy and a resource-based policy on the function.
- `NONE`: no authentication, but the function's resource-based policy is always evaluated and must grant public
  access, otherwise callers get 403 Forbidden. The console and AWS SAM create that policy for you; the CLI,
  CloudFormation and the API do not. Add two statements, each in its own command:
```bash
aws lambda add-permission --function-name fn --statement-id UrlPolicyInvokeURL \
  --action lambda:InvokeFunctionUrl --principal '*' --function-url-auth-type NONE
aws lambda add-permission --function-name fn --statement-id UrlPolicyInvokeFunction \
  --action lambda:InvokeFunction --principal '*' --invoked-via-function-url
```
- Condition keys: `lambda:FunctionUrlAuthType` (AWS_IAM or NONE) and `lambda:InvokedViaFunctionUrl`, which limits
  `lambda:InvokeFunction` to calls through the URL. AWS recommends the latter with NONE. An SCP can deny
  `lambda:CreateFunctionUrlConfig` and `lambda:UpdateFunctionUrlConfig` unless the auth type is `AWS_IAM`.

## Request/response
Events use the API Gateway payload format version 2.0. Return `{statusCode, headers, body, cookies, isBase64Encoded}`.
If you return valid JSON without a `statusCode`, Lambda assumes 200, `application/json` and the value as the body.
Return cookies in the `cookies` array, not as `set-cookie` headers.

## Response streaming
Set `--invoke-mode RESPONSE_STREAM`. Benefits: lower time to first byte, and payloads up to 200 MB versus 6 MB for
buffered responses. The first 6 MB streams uncapped; the remainder is capped at 2 MBps. Native streaming is
supported on Node.js managed runtimes; other languages need a custom runtime with a custom Runtime API integration, or
the Lambda Web Adapter. See the AWS page "Writing response streaming-enabled Lambda functions" for the handler code.
- Streaming is billed for the full function duration even if the client disconnects, so watch long timeouts.
- The Lambda console always shows streamed responses as buffered.
- Function URLs do not support response streaming inside a VPC; use `InvokeWithResponseStream` through the SDK with
  an interface VPC endpoint for Lambda.

## Gotchas
- Throttle a function URL with reserved concurrency: maximum request rate is 10 times the reserved concurrency, and
  excess requests get HTTP 429. Setting reserved concurrency to 0 deactivates the URL (429 for everything).
- Deleting a URL with auth type `NONE` does not delete its resource-based policy statements; delete them yourself.
- Deleting a URL is not recoverable: a new URL gets a different address.

## Verify
`curl -i` the URL. For `AWS_IAM` the request must be SigV4-signed; for `NONE` any HTTP client works. A 403 means the
resource-based policy does not grant `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction`.

## Checked
2026-11-08. Confirmed against the AWS Lambda Developer Guide pages for function URL configuration, access control,
invocation and response streaming, and the CLI flags against the botocore model. Removed: the Node.js
`streamifyResponse` snippet and the claims about WAF, API keys, CloudFront front-ends and the `curl --aws-sigv4`
flag, which the pages do not state.
Method: docs-only read of cited pages, 2026-11-08
