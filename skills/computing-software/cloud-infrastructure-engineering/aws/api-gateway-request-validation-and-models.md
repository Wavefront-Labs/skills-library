---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-request-validation-and-models
name: api-gateway-request-validation-and-models
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, request-validation, json-schema-models, request-validator, openapi, rest-api]
level: practitioner
status: docs-checked
description: "Reject bad requests at the edge with API Gateway REST request validators and JSON Schema models: required params, body schemas, OpenAPI definitions and useful error messages."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-validation-set-up.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-known-issues.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/supported-gateway-response-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway request validation and models

Request validation is a **REST API** feature (HTTP APIs do not support request validation and ignore
`requestBody` schemas on import; validate in the backend there).

## 1. Validators
Three modes: validate body, validate query string parameters and headers, or both.
```bash
aws apigateway create-request-validator --rest-api-id a1b2c3 --name body-and-params \
  --validate-request-body --validate-request-parameters
```

## 2. Models (JSON Schema draft 4)
```bash
aws apigateway create-model --rest-api-id a1b2c3 --name CreateOrder --content-type application/json \
  --schema '{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object", "additionalProperties": false,
    "required": ["customerId", "items"],
    "properties": {
      "customerId": {"type": "string", "pattern": "^c-[0-9a-f]{8}$"},
      "items": {"type": "array", "minItems": 1, "maxItems": 50,
        "items": {"type": "object", "required": ["sku", "qty"],
          "properties": {"sku": {"type": "string"}, "qty": {"type": "integer", "minimum": 1}}}}}}'
```
Draft 4 only: no `const`, `if/then`, `$defs`; use `definitions` and `$ref` to
`https://apigateway.amazonaws.com/restapis/<id>/models/<name>` for reuse.

## 3. Attach to a method
```bash
aws apigateway update-method --rest-api-id a1b2c3 --resource-id <res> --http-method POST \
  --patch-operations op=replace,path=/requestValidatorId,value=<validator-id>
aws apigateway create-deployment --rest-api-id a1b2c3 --stage-name prod
```
Request models (`requestModels`) and required parameters (`requestParameters`, for example
`method.request.querystring.x=true`) are method properties; set them when you define the method or through OpenAPI (section 4).

## 4. OpenAPI form (preferred in IaC)
```yaml
x-amazon-apigateway-request-validators:
  all: {validateRequestBody: true, validateRequestParameters: true}
x-amazon-apigateway-request-validator: all
paths:
  /orders:
    post:
      parameters:
        - {name: Idempotency-Key, in: header, required: true, schema: {type: string}}
      requestBody:
        required: true
        content: {application/json: {schema: {$ref: '#/components/schemas/CreateOrder'}}}
```
Import with `aws apigateway put-rest-api --mode overwrite --body fileb://openapi.yaml` or
SAM/CDK `SpecRestApi`.

## 5. Error responses
Failures return 400 with gateway response `BAD_REQUEST_BODY` or `BAD_REQUEST_PARAMETERS`;
the documented default body message is `Invalid request body`. Expose the validator detail:
```bash
aws apigateway put-gateway-response --rest-api-id a1b2c3 --response-type BAD_REQUEST_BODY \
  --response-templates '{"application/json":"{\"message\":\"$context.error.validationErrorString\"}"}'
```

## Gotchas
- Validation is input hygiene, not security: keep authorization in authorizers/IAM and
  still validate inside the backend for anything security-relevant.
- Lambda proxy integrations still receive the raw body; validation does not transform it.

## Verify
- [ ] Missing required field returns 400 with the validation error string; valid request passes.
- [ ] Missing required header/query parameter returns 400 `BAD_REQUEST_PARAMETERS`.
- [ ] OpenAPI in Git is the source of truth; exported API matches it.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot).
Confirmed: models use JSON Schema draft 4; `requestValidatorId` method property; `$context.error.validationErrorString`; `BAD_REQUEST_BODY` and `BAD_REQUEST_PARAMETERS` gateway responses and the `Invalid request body` message; HTTP APIs do not support request validation (OpenAPI `requestBody` and `schema` fields are ignored).
Removed as unconfirmed: the `requestModels` and `requestParameters` JSON-patch paths, the content-type fallback rule, the model-size remark and the Lambda-authorizer validation suggestion.

Method: documentation only; no commands were run.
