---
id: computing-software.cloud-infrastructure-engineering.aws.acm-certificate-in-use-and-replacement
name: acm-certificate-in-use-and-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, acm, certificate-in-use, replace-certificate, resourceinuseexception, certificate-expiry]
level: practitioner
status: docs-checked
description: "Replace ACM certificates attached to ALBs, CloudFront and API Gateway, fix ResourceInUseException on delete, and reimport renewed certs in place."
sources: ["https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-delete.html", "https://docs.aws.amazon.com/acm/latest/userguide/import-reimport.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate in-use errors and replacing certificates

## 1. Find what uses it
```bash
aws acm describe-certificate --certificate-arn <CERT_ARN> --query 'Certificate.{inUse:InUseBy,exp:NotAfter,type:Type}'
```
ACM cannot delete a certificate that another AWS service is using: remove the association with that service's console or CLI first, then `aws acm delete-certificate`. Deletion is eventually consistent, so a deleted certificate may still appear in lists briefly. Deleting a certificate from a private CA does not delete or stop billing for the CA.

## 2. Swap per integration
```bash
# ALB/NLB default cert
aws elbv2 modify-listener --listener-arn <LISTENER_ARN> --certificates CertificateArn=<NEW_ARN>
# SNI extra certs
aws elbv2 add-listener-certificates --listener-arn <LISTENER_ARN> --certificates CertificateArn=<NEW_ARN>
aws elbv2 remove-listener-certificates --listener-arn <LISTENER_ARN> --certificates CertificateArn=<OLD_ARN>
# API Gateway custom domain (regional)
aws apigateway update-domain-name --domain-name api.example.com \
  --patch-operations op=replace,path=/regionalCertificateArn,value=<NEW_ARN>
```
CloudFront: `get-distribution-config`, change `ViewerCertificate.ACMCertificateArn`, then `update-distribution --if-match <ETag>` (check the CloudFront documentation for the Region the certificate must be in).

## 3. Imported certificates: reimport instead
```bash
aws acm import-certificate --certificate-arn <EXISTING_ARN> \
  --certificate fileb://cert.pem --private-key fileb://key.pem --certificate-chain fileb://chain.pem
```
Reimporting before expiry keeps the original certificate's ARN and its service associations, so no integration changes are needed. Rules:
- You can add or remove domain names but not all of them.
- Existing Key Usage and Extended Key Usage values cannot be removed (new values can be added); exceptions: `keyEncipherment` on ECDSA certificates and the Client Authentication EKU. ACM does not support rollback to a previously imported certificate.
- The key type and size cannot change.
- You cannot apply resource tags when reimporting.

## 4. Verify the swap
- [ ] `openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null | openssl x509 -noout -dates -serial` shows the new cert.
- [ ] Old certificate's `InUseBy` is empty, then delete it.

## Checked
2026-10-28. Confirmed on the gs-acm-delete and import-reimport pages: in-use deletion rule, eventual consistency, private CA note, reimport preservation of ARN and associations, and the reimport conditions above. Fixed: the old text said domain names must match on reimport, but you may add or remove them. Removed as unconfirmed: the us-east-1 requirement for CloudFront, stale `InUseBy` timing advice, the 45-day EventBridge expiry event and `DaysToExpiry` metric, "imported certs never auto-renew".
Method: documentation only; no commands were run.
