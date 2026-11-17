---
id: computing-software.cloud-infrastructure-engineering.aws.acm-certificates-on-alb-cloudfront-and-api-gateway
name: acm-certificates-on-alb-cloudfront-and-api-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, acm, acm-us-east-1, certificate-association, sni-multiple-certificates, cloudfront, alb, api-gateway]
level: practitioner
status: docs-checked
description: "Attach ACM certificates to ALB listeners, CloudFront (us-east-1 only) and API Gateway custom domains, with SNI certificate lists and in-use checks before replacement."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/https-listener-certificates.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-specify-certificate-for-custom-domain-name.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html", "https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using ACM certificates with ALB, CloudFront and API Gateway

## 1. Region rules
| Consumer | Certificate must be in |
|---|---|
| CloudFront viewer HTTPS | **us-east-1** (request or import there) |
| CloudFront to an Elastic Load Balancing origin | any Region |
| API Gateway edge-optimized custom domain | **us-east-1** |
| API Gateway Regional custom domain | the same Region as the API |
| ALB listener | the load balancer's Region |
| Cognito user pool custom domain | **us-east-1** (Cognito creates a CloudFront distribution) |
A global app on CloudFront plus regional ALB origins therefore needs two certificates for the same names: one in
us-east-1, one per origin Region. The DNS validation CNAME token works in any Region, so one validation record serves
both certificates while it stays in place.

## 2. ALB
```bash
aws elbv2 create-listener --load-balancer-arn <alb> --protocol HTTPS --port 443 \
  --certificates CertificateArn=<default-cert> \
  --ssl-policy ELBSecurityPolicy-TLS13-1-2-2021-06 \
  --default-actions Type=forward,TargetGroupArn=<tg>
aws elbv2 add-listener-certificates --listener-arn <listener> \
  --certificates CertificateArn=<cert-b> CertificateArn=<cert-c>
```
- Quota: 25 certificates per Application Load Balancer, excluding the default certificate; adjustable (read on the
  ELB quotas page, 2026-10-27). SNI chooses a certificate by hostname and the default certificate is the fallback.
- `ELBSecurityPolicy-TLS13-1-2-2021-06` is listed on the ALB security policies page.

## 3. CloudFront
```bash
aws cloudfront update-distribution --id E123 --if-match <etag> --distribution-config file://dc.json
```
In `dc.json`, `Aliases` must list every hostname, and
```json
"ViewerCertificate": {"ACMCertificateArn": "arn:aws:acm:us-east-1:<ACCOUNT_ID>:certificate/<ID>",
  "SSLSupportMethod": "sni-only", "MinimumProtocolVersion": "TLSv1.2_2021"}
```
- `SSLSupportMethod` is `sni-only`, `vip` or `static-ip`; `MinimumProtocolVersion` includes `TLSv1.2_2021`.
- When you add an alternate domain name CloudFront checks the attached certificate covers it: the SAN must contain
  an exact match or a wildcard at the same level. Otherwise the update fails (`InvalidViewerCertificate`).
- An alias already used by another distribution fails with `CNAMEAlreadyExists`; `associate-alias` is the API for
  moving an alias between distributions.

## 4. API Gateway custom domains
```bash
aws apigatewayv2 create-domain-name --domain-name api.example.com \
  --domain-name-configurations CertificateArn=<regional-cert>,EndpointType=REGIONAL,SecurityPolicy=TLS_1_2
aws apigatewayv2 create-api-mapping --domain-name api.example.com --api-id <id> --stage prod
```
- `EndpointType` is `REGIONAL` or `EDGE`; `SecurityPolicy` is `TLS_1_0` or `TLS_1_2`. An edge-optimized domain uses
  CloudFront, hence the us-east-1 certificate.
- If ACM is not available in the API's Region you can import a certificate into API Gateway there instead.
- Point DNS (for example a Route 53 alias) at the domain name's target returned for the custom domain.
- Mutual TLS needs a Regional custom domain, an ACM certificate and a truststore uploaded to S3.

## 5. Before replacing a certificate
- To replace a certificate (new SANs), request the new one, attach it, then remove the old one. Find users first:
```bash
aws acm describe-certificate --certificate-arn <arn> --query 'Certificate.InUseBy'
```
- Deleting a certificate that is in use fails with `ResourceInUseException`.
- ACM managed renewal depends on the certificate being in use and, for DNS validation, the CNAME remaining in place.

## Verify
- [ ] `openssl s_client -connect app.example.com:443 -servername app.example.com` shows the intended certificate.
- [ ] Every hostname on CloudFront and each ALB listener is covered by a certificate.
- [ ] `InUseBy` matches the intended consumers.

## Checked
Date: 2026-10-27. Documentation release: ACM User Guide, CloudFront Developer Guide, ELB User Guide, API Gateway
Developer Guide, Cognito Developer Guide (latest) and botocore cloudfront, acm and apigatewayv2 models. Confirmed:
per-service certificate Region rules, the 25-certificate ALB quota and its adjustability, the TLS13-1-2-2021-06
policy name, CloudFront SAN rule, `ViewerCertificate` enums, `CNAMEAlreadyExists`, `InvalidViewerCertificate`,
`associate-alias`, API Gateway endpoint types and security policies, mTLS prerequisites and `ResourceInUseException`.
Removed AppSync, NLB and Private CA browser-trust claims, the imported-certificate renewal and CloudFront
log-field advice, and the "up to 25 per listener" wording (the quota is per load balancer).
Method: documentation only; no commands were run.
