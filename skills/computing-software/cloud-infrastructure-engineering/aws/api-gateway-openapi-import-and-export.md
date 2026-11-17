---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-openapi-import-and-export
name: api-gateway-openapi-import-and-export
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, openapi-import, api-export, openapi, swagger, x-amazon-apigateway-integration, api-as-code]
level: practitioner
status: docs-checked
description: "Define API Gateway REST and HTTP APIs in OpenAPI: import with overwrite or merge, x-amazon-apigateway extensions, export with integrations, and unsupported-feature warnings."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api-update.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api-basePath.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-export-api.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-known-issues.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-export.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway OpenAPI import and export

**Goal:** keep the API contract in an OpenAPI file in git, deploy API Gateway from it, and
export an existing console-built API to start that file.

## REST APIs
```bash
# create
aws apigateway import-rest-api --fail-on-warnings \
  --parameters endpointConfigurationTypes=REGIONAL --body fileb://api.yaml
# update: overwrite takes the file's definitions and drops items not in it; merge (the default) keeps both
aws apigateway put-rest-api --rest-api-id "$API" --mode overwrite --fail-on-warnings --body fileb://api.yaml
aws apigateway create-deployment --rest-api-id "$API" --stage-name prod   # changes are live only after deploy
# export with integrations so it can be re-imported
aws apigateway get-export --rest-api-id "$API" --stage-name prod \
  --export-type oas30 --parameters extensions='integrations' --accepts application/yaml api.yaml
```
- `extensions='integrations'` or `'apigateway'` exports the `x-amazon-apigateway-integration` extensions (the documented
  `apigateway` example also keeps `x-amazon-apigateway-request-validator`); `extensions='authorizers'` adds
  `x-amazon-apigateway-authorizer`; `postman` adds Postman extensions.
- `basepath` import parameter: `ignore` (default), `prepend`, `split`. `--fail-on-warnings` stops the import on warnings.
- `--mode` on `put-rest-api` is `merge` (the default) or `overwrite`.

## Extensions you need in the file
```yaml
paths:
  /orders/{id}:
    get:
      parameters: [{name: id, in: path, required: true, schema: {type: string}}]
      x-amazon-apigateway-integration:
        type: aws_proxy
        httpMethod: POST            # always POST for Lambda
        uri: arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/${FnArn}/invocations
x-amazon-apigateway-request-validators: {all: {validateRequestBody: true, validateRequestParameters: true}}
x-amazon-apigateway-request-validator: all
```
Also: `x-amazon-apigateway-authorizer`, `x-amazon-apigateway-gateway-responses`,
`x-amazon-apigateway-binary-media-types`, `x-amazon-apigateway-policy`, `x-amazon-apigateway-endpoint-configuration`.

## HTTP APIs
```bash
aws apigatewayv2 import-api --body file://http-api.yaml
aws apigatewayv2 reimport-api --api-id "$API" --body file://http-api.yaml
aws apigatewayv2 export-api --api-id "$API" --specification OAS30 --output-type YAML \
  --stage-name '$default' out.yaml   # API Gateway extensions are included by default
```

## In IaC
CloudFormation `AWS::ApiGateway::RestApi` with `Body` or `BodyS3Location`; SAM `DefinitionBody`.

## Gotchas
- Models use JSON Schema draft 4. Documented limitations: `discriminator` is not supported in any schema object, the `example` tag is not supported, and `oneOf` is not supported for OpenAPI 2.0 or SDK generation. Run with `--fail-on-warnings` in CI.
- `overwrite` removes existing items that the file does not define.
- API Gateway documents support for OpenAPI 2.0 and 3.0.x (HTTP API export supports `OAS30` only).

## Verify
- [ ] CI imports with `--fail-on-warnings` into a scratch API and fails the build on warnings.
- [ ] Export of prod re-imports cleanly into a test account (round-trip).

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the current botocore `apigateway` and `apigatewayv2` models.
Confirmed: `PutRestApi` modes merge (default) and overwrite; `basepath` values and default `ignore`; `get-export` types `oas30` and `swagger` and the `extensions` values; HTTP API `ExportApi` parameters (`Specification` OAS30 only, `OutputType` JSON or YAML, extensions included by default); known-issue list for discriminator, example and oneOf; JSON Schema draft 4 models.
Fixed: `extensions='apigateway'` exports integration extensions (not all extensions); the HTTP export flag was redundant. Removed unconfirmed claims about `Fn::Transform: AWS::Include`, Lambda permissions, and exports containing account ids.

Method: documentation only; no commands were run.
