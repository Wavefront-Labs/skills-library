---
id: computing-software.cloud-infrastructure-engineering.aws.acm-certificates-and-private-ca
name: acm-certificates-and-private-ca
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, acm, certificate-manager, aws-certificate-manager, private-ca, aws-private-ca, tls-certificates, dns-validation, certificate-renewal, wildcard-certificate, san-certificate, imported-certificates, certificate-expiry, ca-hierarchy, subordinate-ca, crl, ocsp, caa-record, us-east-1, cloudfront-certificate, alb-certificate, sni, ecdsa, tls]
level: practitioner
status: docs-checked
description: "Issue, validate, renew and monitor TLS certificates with AWS Certificate Manager, import third-party certs, and run AWS Private CA hierarchies for internal TLS and mTLS."
sources: ["https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html", "https://docs.aws.amazon.com/acm/latest/userguide/dns-renewal-validation.html", "https://docs.aws.amazon.com/acm/latest/userguide/acm-certificate-characteristics.html", "https://docs.aws.amazon.com/acm/latest/userguide/acm-limits.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ACM certificates and AWS Private CA — TLS that renews itself

**Goal:** every public endpoint serves a certificate that renews without a human, every
internal service can get a cert from a CA you control, and nothing expires unnoticed.
Where certificates attach (ALB listeners, CloudFront) is in `...aws.elastic-load-balancing`
and `...aws.cloudfront-distributions`.

## 1. Public certificates
```
aws acm request-certificate --domain-name api.example.com \
  --subject-alternative-names "*.api.example.com" \
  --validation-method DNS --key-algorithm EC_prime256v1 \
  --idempotency-token api-prod-1
aws acm describe-certificate --certificate-arn <ARN> \
  --query 'Certificate.DomainValidationOptions[].ResourceRecord'
```
- **DNS validation, always.** Create the returned CNAME and **leave it in place**: it lets you
  request further certificates for the same name without repeating validation, and ACM uses it
  to renew. Renewal is fully automated for DNS-validated certificates. At 45 days before
  expiry ACM checks that the certificate is **in use by an AWS service** and that the
  ACM-provided CNAME for each unique name is publicly resolvable (certificates issued with the
  older 395-day validity renew 60 days out). If it cannot validate, ACM sends AWS Health and
  EventBridge events at 30, 15, 7, 3 and 1 days before expiry. The CNAME chain must be five
  CNAMEs or fewer.
- A wildcard and its base domain (`*.example.com`, `example.com`) share the same validation
  record, so put both names on one cert; other names get unique records. The validation token
  works in any Region, so you can re-create the same certificate in several Regions.
- **Region matters:** a cert is usable only by resources in its Region, except
  **CloudFront, which needs the certificate requested or imported in us-east-1**. Request the
  same names twice when you need both an ALB in another Region and CloudFront.
- Key algorithms: `RSA_1024`, `RSA_2048` (default), `RSA_3072`, `RSA_4096`, `EC_prime256v1`,
  `EC_secp384r1`, `EC_secp521r1`. ECDSA keys are smaller and more computationally efficient
  than RSA of comparable strength but not all clients support them; ALB listeners can hold both.
  For private certificates the signing algorithm family must match the CA's key family.
- Quotas (defaults, from the ACM quotas page): 2,500 ACM certificates (expired and revoked ones
  count; certificates from Private CA do not), 5,000 per year per Region and account, 2,500
  imported certificates, and 10 domain names per ACM certificate (raisable to 100 through
  Service Quotas; the limit applies to ACM-issued, not imported, certificates). Public ACM
  certificates are valid for 198 days.
- Public ACM certificates are normally not exportable; the ACM API has an `ExportCertificate`
  operation, so check the ACM docs and pricing page for which certificates qualify and at what cost.

## 2. Imported and third-party certificates
`aws acm import-certificate --certificate fileb://cert.pem --private-key fileb://key.pem --certificate-chain fileb://chain.pem`
- No managed renewal: re-import to the **same ARN** before expiry (`--certificate-arn`
  on import) so attached listeners keep working without re-pointing.
- Set the expiry-event lead time with
  `aws acm put-account-configuration --expiry-events DaysBeforeExpiry=<DAYS> --idempotency-token <TOKEN>`
  and route the ACM expiry events (AWS Health, EventBridge) to a ticket.

## 3. Private CA
- `aws acm-pca create-certificate-authority --certificate-authority-type ROOT
  --certificate-authority-configuration file://ca.json --usage-mode GENERAL_PURPOSE
  --revocation-configuration file://crl.json`; types are `ROOT` and `SUBORDINATE`, usage
  modes `GENERAL_PURPOSE` and `SHORT_LIVED_CERTIFICATE`. Then issue the CA's own certificate
  and `import-certificate-authority-certificate` to activate it.
- **Hierarchy:** a root used only to sign subordinates plus one or more **subordinate CAs**
  that issue end-entity certs. Short-lived mode suits workload identity. Billing differs by
  mode; see the AWS Private CA pricing page.
- **Issue through ACM** (`request-certificate --certificate-authority-arn <CA_ARN>`) for
  resources ACM integrates with: these private certificates are managed in ACM with the same
  restrictions as public ones. Issue directly from Private CA (`acm-pca issue-certificate`
  with a CSR) for things ACM cannot attach to, and handle renewal yourself. A Private CA quota
  of 200 CAs and 1,000,000 certificates per CA (lifetime) applies by default.
- Revocation: decide on CRL and/or OCSP before issuing, because the revocation endpoints are
  embedded in the certificates you issue.
- Trust distribution is your problem: push the root cert into OS trust stores and into
  client truststores for mTLS.

## Gotchas
- If ACM cannot validate the domain within 72 hours of generating the CNAME, the certificate
  status becomes "Validation timed out"; fix DNS and request a new certificate.
- Renewal fails if the validation CNAME is missing or not public, or if the certificate is
  not in use by an AWS service. Check `RenewalSummary` in `describe-certificate`.
- The first domain name submitted becomes the certificate's subject common name; all names
  go in the Subject Alternative Name extension.

## Verify
- [ ] Every public cert is DNS-validated, in use, and the validation CNAME is in the zone's IaC.
- [ ] CloudFront certs live in us-east-1; regional certs in the resource's Region.
- [ ] Expiry events route to a ticket queue.
- [ ] Private CA: root signs only the subordinate; subordinate issues end-entity certs; `openssl verify -CAfile root.pem -untrusted sub.pem leaf.pem` passes.
- [ ] `openssl s_client -connect host:443 -servername host` shows the intended chain and an ECDSA or RSA key as planned.

## Checked
2026-10-31. Confirmed against the ACM User Guide pages on DNS validation (CNAME reuse, wildcard record sharing, any-Region token, five-CNAME chain limit, 72-hour timeout), renewal for DNS-validated domains (45/60 days, in-use criterion, 30/15/7/3/1-day events), certificate characteristics (key algorithms, 198-day validity, algorithm family match) and quotas (2,500 / 5,000 / imported / 10 domain names / 200 Private CAs / 1,000,000 certificates per CA), the CloudFront HTTPS requirements page (us-east-1), and the botocore `acm` and `acm-pca` models (`RequestCertificate` options, `PutAccountConfiguration.ExpiryEvents.DaysBeforeExpiry`, CA types and usage modes, `ExportCertificate`). Removed as unconfirmed: the exportable-certificate launch date and fee, CAA domain list, import key and chain format rules, the default expiry-event lead time, Config rule name, root template ARN and template names, RAM sharing, CRL bucket and OCSP details, CloudFormation and cert-manager remarks, the name-length remark and Private CA validity capping. Prices were never kept.
Method: documentation only; no commands were run.
