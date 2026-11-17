---
id: computing-software.cloud-infrastructure-engineering.aws.transfer-family-web-apps
name: transfer-family-web-apps
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transfer-family, transfer-web-apps, s3-access-grants, identity-center, browser-file-transfer]
level: practitioner
status: docs-checked
description: "Give business users browser-based upload and download to S3 with Transfer Family web apps: Identity Center sign-in, S3 Access Grants permissions, CORS, branding and custom URLs."
sources: ["https://docs.aws.amazon.com/transfer/latest/userguide/web-app.html", "https://docs.aws.amazon.com/transfer/latest/userguide/webapp-access-grant.html", "https://docs.aws.amazon.com/transfer/latest/userguide/webapp-configure.html", "https://docs.aws.amazon.com/transfer/latest/userguide/webapp-customize.html", "https://docs.aws.amazon.com/transfer/latest/userguide/webapp-cloudtrail.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer Family web apps

**Goal:** non-technical users browse, upload and download files in S3 from a branded web page,
signed in with corporate identity, without SFTP clients or IAM users.

## Pieces
1. **IAM Identity Center** (account or organization instance) as the federated identity provider; its identity
   source can be an Identity Center directory, AWS Directory Service for Microsoft AD, or an external IdP.
2. **S3 Access Grants** instance (create one if you do not have one in that Region): grants map users and groups to S3
   locations and prefixes with READ, WRITE or READWRITE, and S3 Access Grants vends temporary credentials.
   An access grant is required for identity propagation.
3. **Web app** in Transfer Family pointing at Identity Center, with an IAM role.
4. **CORS** on every bucket the web app accesses, allowing the web app's access endpoint.

## Set up
```bash
aws s3control create-access-grants-instance --account-id <ACCOUNT_ID> \
  --identity-center-arn arn:aws:sso:::instance/ssoins-123
aws s3control create-access-grants-location --account-id <ACCOUNT_ID> \
  --location-scope s3://partner-files/ --iam-role-arn arn:aws:iam::<ACCOUNT_ID>:role/AccessGrantsLocationRole
aws s3control create-access-grant --account-id <ACCOUNT_ID> \
  --access-grants-location-id default --access-grants-location-configuration S3SubPrefix=finance/* \
  --grantee GranteeType=DIRECTORY_GROUP,GranteeIdentifier=<identity-store-group-id> --permission READWRITE
aws transfer create-web-app --identity-provider-details \
  'IdentityCenterConfig={InstanceArn=arn:aws:sso:::instance/ssoins-123,Role=arn:aws:iam::<ACCOUNT_ID>:role/TransferWebAppRole}'
```
- Bucket CORS: copy the exact CORS JSON from the Transfer Family web app guide, with your web app's access endpoint as
  the allowed origin; add each additional web app's endpoint to every bucket's CORS policy.
- Assign users or groups to the web app (paste the Identity Center user/group ID); with an Identity Center directory
  you can also add users from the web app itself.
- Branding: optional title (default "Transfer Web App"), logo and favicon images; an optional custom URL is served
  through Amazon CloudFront.
- Capacity in **web app units**: one unit allows web app activity from up to 250 unique sessions; provision for peak load.

## Gotchas
- Each bucket the web app uses needs a CORS policy, or the browser blocks the calls.
- Logging: enable CloudTrail S3 data events on the buckets to track file operations made through the web app; web app
  CloudTrail entries carry the Identity Center `userIdentity`.

## Verify
- [ ] Test user signs in, sees only what the grants allow, uploads and downloads.
- [ ] CloudTrail data events show the file operations.

## Checked

2026-10-28. Confirmed against the Transfer Family User Guide pages web-app, webapp-access-grant, webapp-configure, webapp-customize and webapp-cloudtrail: Identity Center plus S3 Access Grants design, READ/WRITE/READWRITE permissions, CORS requirement per bucket, 250 sessions per web app unit, branding and CloudFront custom URL, CloudTrail S3 data events.
Removed: the sample CORS JSON and exact origin pattern, the billing-per-unit-hour claim, KMS-location-role gotcha, the "grant on finance/* hides bucket root" claim, and made-up account IDs. The prose-only `sources` were replaced with real URLs.
Method: documentation only; no commands were run.
