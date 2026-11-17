---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-custom-domains-and-mtls
name: api-gateway-custom-domains-and-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, custom-domain, base-path-mapping, apigw-mtls, api-mappings, acm, route53]
level: practitioner
status: docs-checked
description: "Put API Gateway behind a custom domain: regional vs edge, ACM certificates, base path and API mappings, Route 53 aliases, mutual TLS truststores, default endpoint off."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mappings.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-mappings.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-disable-default-endpoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway custom domains, base path mapping and mTLS

**Goal:** `https://api.example.com/v1` stable across API rebuilds, optionally requiring
client certificates.

## 1. Regional custom domain (default choice)
```bash
aws apigatewayv2 create-domain-name --domain-name api.example.com \
  --domain-name-configurations CertificateArn=$CERT_ARN,EndpointType=REGIONAL,SecurityPolicy=TLS_1_2
aws apigatewayv2 create-api-mapping --domain-name api.example.com --api-id $API --stage prod --api-mapping-key v1
```
- Certificate: ACM in the **same region** for regional; **us-east-1** for edge-optimized.
- Route 53: alias A/AAAA to the domain's `ApiGatewayDomainName` + `HostedZoneId` (from
  `get-domain-name`), *not* to the `execute-api` URL.
- The `apigatewayv2` mapping API works for REST and HTTP APIs; multi-level keys (for example `orders/v1/items`)
  need a regional custom domain with the TLS 1.2 security policy and the `apigatewayv2` API (or `AWS::ApiGatewayV2`).
- Older REST-only command: `aws apigateway create-base-path-mapping --domain-name ... --base-path v1 --rest-api-id ... --stage prod`.

## 2. Mapping strategy
- `v1` → API A, `v2` → API B lets you replace a whole API without clients changing hosts.
- The mapping key is stripped before the request reaches the API: `/v1/orders` hits route `/orders`.
- One API stage can be mapped from several domains.

## 3. Mutual TLS
```bash
aws s3 cp truststore.pem s3://my-truststores/api/truststore.pem   # PEM bundle of client CA certs
aws apigatewayv2 create-domain-name --domain-name api.example.com \
  --domain-name-configurations CertificateArn=$CERT_ARN,EndpointType=REGIONAL,SecurityPolicy=TLS_1_2 \
  --mutual-tls-authentication TruststoreUri=s3://my-truststores/api/truststore.pem,TruststoreVersion=<S3_VERSION_ID>
```
- REST mTLS needs a Regional custom domain with minimum TLS 1.2; use S3 versioning for the truststore and pin `TruststoreVersion`.
- Truststore: a `.pem` file with the full chain from issuing CA to root, maximum chain length four.
- Client cert details reach the backend in `$context.identity.clientCert.*` (for example `subjectDN`, `issuerDN`,
  `clientCertPem`); API Gateway forwards the certificates to Lambda authorizers.
- API Gateway does not check revocation: use a Lambda authorizer to check whether a certificate has been revoked.
- When you point the domain at a new truststore version, API Gateway returns warnings if certificates are invalid.

## 4. Lock down the default endpoint
Set `disableExecuteApiEndpoint=true` on the API so clients cannot bypass the custom domain
(and its mTLS) by calling `execute-api` directly. For REST APIs, deploy the API for the change to take effect.

## Gotchas
- Wildcard custom domains (wildcard as the first label, for example `*.api.example.com`) are supported and avoid exceeding the custom-domain quota (120 per account per Region by default).

## Verify
- [ ] `curl -v https://api.example.com/v1/health` presents your ACM certificate and returns 200.
- [ ] With mTLS: a client without a trusted certificate is rejected; a valid certificate returns 200.
- [ ] The default `execute-api` URL stops working after disabling it and deploying.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the current botocore `apigatewayv2` model.
Confirmed: ACM certificate region rule (us-east-1 for edge-optimized); multi-level API mappings need regional domain, TLS 1.2 and `apigatewayv2`; REST mTLS needs Regional domain with TLS 1.2; S3-versioned truststore and `truststoreVersion` patch; truststore chain rules; `$context.identity.clientCert.*` fields; revocation via Lambda authorizer; disabling the default endpoint needs a deployment; wildcard domains.
Removed as unconfirmed: the WAF-on-edge claim, the one-region-per-domain claim and the `DomainNameStatusMessage` field name.

Method: documentation only; no commands were run.
