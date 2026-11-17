---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-mapping-templates-vtl
name: api-gateway-mapping-templates-vtl
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, mapping-template, vtl-mapping, integration-request, direct-integration, rest-api, dynamodb]
level: practitioner
status: gated
description: "Write VTL mapping templates for API Gateway REST integration requests and responses: $input, $util, $context, direct DynamoDB/SQS integrations and passthrough behaviour."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/integration-passthrough-behaviors.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-known-issues.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway mapping templates (VTL)

**Goal:** call AWS services straight from a REST API (no Lambda) or reshape requests/responses
for a legacy backend. HTTP APIs do not support VTL — only parameter mapping.

## 1. Direct SQS integration (POST /orders → SendMessage) (gated: unconfirmed, source is paywalled or blocked)
The SQS and DynamoDB recipes below are patterns not found in the documentation snapshot checked.
Integration: type `AWS`, service `sqs`, path override `<ACCOUNT_ID>/orders-queue`, HTTP
method POST, execution role with `sqs:SendMessage`. Request parameter
`integration.request.header.Content-Type = 'application/x-www-form-urlencoded'`.
Request template for `application/json`:
```velocity
Action=SendMessage&MessageBody=$util.urlEncode($input.body)&MessageAttribute.1.Name=tenant&MessageAttribute.1.Value.DataType=String&MessageAttribute.1.Value.StringValue=$util.urlEncode($context.authorizer.tenantId)
```

## 2. Direct DynamoDB integration (GET /items/{id}) (gated: unconfirmed, source is paywalled or blocked)
Action `GetItem`; request template:
```velocity
{
  "TableName": "items",
  "Key": {"pk": {"S": "$util.escapeJavaScript($input.params('id'))"}}
}
```
Integration response template (200):
```velocity
#set($item = $input.path('$.Item'))
#if("$item" == "")
#set($context.responseOverride.status = 404)
{"message": "not found"}
#else
{"id": "$item.pk.S", "name": "$util.escapeJavaScript($item.name.S)"}
#end
```

## 3. Variables you will use
- `$input.body`, `$input.json('$.path')` (JSON string), `$input.path('$.path')` (object),
  `$input.params('name')` (path, query or header), `$input.params()` (map of all request parameters).
- `$context.requestId`, `$context.identity.sourceIp`, `$context.authorizer.<key>`,
  `$context.responseOverride.status` / `.header.<name>`.
- `$stageVariables.<name>`.
- `$util.escapeJavaScript()`, `$util.urlEncode()`, `$util.base64Encode()`, `$util.parseJson()`.

## 4. Passthrough behaviour
`WHEN_NO_MATCH` passes a request with no matching template through untransformed;
`WHEN_NO_TEMPLATES` passes through only if no templates are defined (otherwise 415);
`NEVER` rejects unmatched content types with 415. When no `Content-Type` header is sent, `application/json` is assumed.
Choose `NEVER` on direct service integrations so callers cannot send raw payloads to the service.

## Gotchas
- Forgetting `$util.escapeJavaScript` on user input lets quotes break (or inject into) the
  JSON you send to the service.
- Map service errors explicitly in the integration responses (selection pattern per status), or callers can see an unexpected status.
- Maximum mapping template size is 300 KB and a `#foreach` loop is limited to 1000 iterations; keep logic minimal.
- Deploy the API to the stage after changes.

## Verify
- [ ] `aws apigateway test-invoke-method --rest-api-id ... --resource-id ... --http-method GET --path-with-query-string /items/1` shows the transformed request in `log` and the expected body.
- [ ] Missing item returns 404; malformed input with quotes is escaped correctly.
- [ ] An unsupported `Content-Type` gets 415 when passthrough is `NEVER`.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot).
Confirmed: `$input.body`, `json()`, `path()`, `params()` functions; `$util` functions (`escapeJavaScript`, `urlEncode`, `base64Encode`, `parseJson`); `$context.responseOverride.status` and `.header`; passthrough behaviours and the 415 outcomes; default `application/json` when no Content-Type; 300 KB template limit and 1000 `#foreach` iterations; HTTP APIs offer parameter mapping only.
Gated: the direct SQS and DynamoDB recipes. The documentation snapshot has no REST API tutorial for them and the live page could not be read, so the path override, header mapping and templates are unconfirmed.

Method: documentation only; no commands were run.
