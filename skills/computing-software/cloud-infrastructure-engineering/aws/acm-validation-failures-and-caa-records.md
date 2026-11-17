---
id: computing-software.cloud-infrastructure-engineering.aws.acm-validation-failures-and-caa-records
name: acm-validation-failures-and-caa-records
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, acm, validation-failure, caa-authorization, pending-validation, dns-validation-troubleshooting, route53]
level: practitioner
status: docs-checked
description: "Fix ACM certificates stuck in Pending validation or Failed: CAA records that exclude Amazon, wrong CNAMEs, 72-hour timeouts and blocked email validation."
sources: ["https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting-DNS-validation.html", "https://docs.aws.amazon.com/acm/latest/userguide/setup.html", "https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting-caa.html", "https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html", "https://docs.aws.amazon.com/acm/latest/userguide/email-validation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACM validation failures and CAA

## 1. Read the status
```bash
aws acm describe-certificate --certificate-arn <arn> \
  --query 'Certificate.{s:Status,reason:FailureReason,dv:DomainValidationOptions[].{d:DomainName,st:ValidationStatus,m:ValidationMethod,rr:ResourceRecord}}'
```
`Status` values: `PENDING_VALIDATION`, `ISSUED`, `INACTIVE`, `EXPIRED`, `VALIDATION_TIMED_OUT`, `REVOKED`, `FAILED`.
If ACM cannot validate within **72 hours** of generating the CNAME value, the status becomes validation timed out;
request a new certificate after reviewing the CNAME instructions. `ValidationMethod` is `DNS`, `EMAIL` or `HTTP`; per
domain `ValidationStatus` is `PENDING_VALIDATION`, `SUCCESS` or `FAILED`.

## 2. FailureReason values
The API returns one of: `CAA_ERROR`, `NO_AVAILABLE_CONTACTS`, `ADDITIONAL_VERIFICATION_REQUIRED`, `DOMAIN_NOT_ALLOWED`,
`INVALID_PUBLIC_DOMAIN`, `DOMAIN_VALIDATION_DENIED`, `PCA_*` values for Private CA requests (for example
`PCA_LIMIT_EXCEEDED`, `PCA_INVALID_STATE`, `PCA_ACCESS_DENIED`), `SLR_NOT_FOUND` and `OTHER`. For the cause and fix of
each, read the ACM "certificate request fails" troubleshooting page (this skill's checked pages cover only the CAA
case). `CAA_ERROR` shows as "One or more domain names have failed validation due to a Certification Authority
Authorization (CAA) error"; update the CAA records and request the certificate again.

## 3. CAA records
CAA is optional. After ACM validates the domain it checks for CAA records. The `value` must contain one of
`amazon.com`, `amazontrust.com`, `awstrust.com` or `amazonaws.com`; if CAA records exist and none names one of them,
ACM cannot issue. A `value` of `;` means no CA may issue. Flags is always `0`; `iodef` is ignored. The value is quoted.
```
example.com.   3600 IN CAA 0 issue "amazon.com"
example.com.   3600 IN CAA 0 issue "letsencrypt.org"
example.com.   3600 IN CAA 0 issuewild "amazon.com"
```
- If an `issuewild` record exists without an Amazon value, ACM cannot issue wildcards. With no `issuewild` but an
  `issue` record for Amazon, wildcards can be issued.
- HTTP validation does not support wildcard certificates; use DNS or email validation for wildcards.
- Check from outside: `dig +short CAA example.com`.

## 4. DNS validation stuck pending
- ACM gives a CNAME name and value per domain; add it once. Renewal works as long as the certificate is in use and the
  CNAME stays in place, so leave it permanently. The same token works in any Region.
- Check the record resolves: `dig _abc123.app.example.com CNAME +short` must return the `acm-validations.aws` target.
- If your DNS provider prohibits a leading underscore in the CNAME value, you can drop it from the value (the name
  must still start with an underscore). If it adds a trailing period automatically, do not add one yourself. Some
  registrars (for example GoDaddy) need the apex domain removed from the end of the NAME field.
- CNAME resolution fails if more than five CNAMEs are chained; use email validation if you need longer chains.
- Route 53 validation fails on private (untrusted) domains, and the console's "Create records in Route 53" button
  may be missing in some cases; see the DNS troubleshooting page.
- Compare `dig NS example.com +short` with the zone's name servers to confirm the zone is the authoritative public one.

## 5. Email validation
Validation emails go to `administrator@`, `hostmaster@`, `postmaster@`, `webmaster@` and `admin@` the validation domain.
For a `www` or wildcard name ACM drops the `www.` or `*.` first. WHOIS email validation is no longer supported for new
certificates or renewals. Tokens expire after 72 hours (you can resend), and ACM emails the same addresses to renew
45 days before expiry. Prefer DNS validation, which needs no repeat approval.

## Verify
- [ ] `dig CAA` on the name and ancestors shows an Amazon CA allowed (or no CAA record at all).
- [ ] The validation CNAME resolves publicly to the `acm-validations.aws` target.
- [ ] A new request reaches `ISSUED`; `RenewalEligibility` (`ELIGIBLE` or `INELIGIBLE`) is ELIGIBLE once in use.

## Checked
Date: 2026-10-27. Documentation release: AWS Certificate Manager User Guide (latest) and botocore acm 2015-12-08
model. Confirmed: status, failure-reason, validation method and renewal-eligibility enums, the 72-hour timeout, CAA
record fields, the four Amazon CA names, `issuewild` behaviour, HTTP validation and wildcards, DNS CNAME
troubleshooting items, email addresses, 72-hour token expiry, 45-day renewal email and WHOIS removal. Removed the
unconfirmed per-reason fix table, CAA tree-walk and CNAME-target behaviour, DNSSEC claim and the CloudFormation
cross-account zone claim.
Method: documentation only; no commands were run.
