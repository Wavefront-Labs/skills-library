---
id: computing-software.cloud-infrastructure-engineering.aws.instance-metadata-tags-and-identity-document
name: instance-metadata-tags-and-identity-document
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, instance-metadata, tags-in-metadata, dynamic-data, instance-identity-document, signature-verification, bootstrap]
level: practitioner
status: docs-checked
description: "Read instance tags and dynamic data from IMDS, use the signed instance identity document to prove an instance's identity to a third party, and verify its signature."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/work-with-tags-in-IMDS.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/verify-iid.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance tags in metadata and the instance identity document

## 1. Tags in IMDS
Off by default. Enable per instance (at launch with `--metadata-options "InstanceMetadataTags=enabled"`,
after launch as below) or in a launch template:
```bash
aws ec2 modify-instance-metadata-options --instance-id i-123 --instance-metadata-tags enabled
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 300')
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/tags/instance/        # keys
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/tags/instance/Role    # value
```
Use it to configure the instance by tag (Role=web, Env=prod) without calling the
`DescribeInstances` or `DescribeTags` APIs. Tags added or removed while the instance is
running are reflected without a stop/start. Once access is enabled, tag keys may contain only
letters, digits and `+ - = . , _ : @`, and cannot contain spaces or `/`; non-compliance
fails new launches or returns an error on existing instances. To check the setting, read
`InstanceMetadataTags` from `describe-instances` (value `enabled` or `disabled`).

## 2. Dynamic data and the identity document
```bash
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/document
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/signature
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/pkcs7
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/rsa2048
```
The document is plaintext JSON with `accountId`, `architecture`, `availabilityZone`,
`billingProducts`, `imageId`, `instanceId`, `instanceType`, `kernelId`,
`marketplaceProductCodes`, `pendingTime`, `privateIp`, `ramdiskId`, `region`, `version`
(`devpayProductCodes` is deprecated). The `availabilityZone` is a zone name, which can
differ across AWS accounts.

## 3. Proving identity to a third party
Three signatures accompany the document, each at its own endpoint: base64-encoded
(`signature`, SHA256 hash, RSA key pair), `pkcs7` (SHA1 hash, DSA key pair) and `rsa2048`
(SHA256 hash, RSA-2048 key pair). Verify with the matching AWS public certificate for the
instance's Region (see "AWS public certificates for instance identity document signatures").
RSA-2048 option:
```bash
echo "-----BEGIN PKCS7-----" >> rsa2048
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/rsa2048 >> rsa2048
echo "" >> rsa2048 ; echo "-----END PKCS7-----" >> rsa2048
openssl smime -verify -in rsa2048 -inform PEM -certfile certificate -noverify | tee document
```
A valid signature prints "Verification successful" and writes the document to `document`.
After verifying, check `accountId` and `instanceId` against what you expect. Treat the
document as identity, not as a credential.

## Gotchas
- The document is regenerated when the instance is launched, stopped and started, or
  restarted, so cache it with that in mind.
- If verification fails, AWS says to contact Support.

## Verify
- [ ] Reading `.../meta-data/tags/instance/<key>` returns the tag value on an instance with tags enabled.
- [ ] `openssl smime -verify` prints "Verification successful" with the correct Region certificate.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: "View tags for your EC2 instances using instance metadata", "Instance
identity documents" (field table) and "Verify the instance identity document" (all three
options, Linux and PowerShell). The certificate list page ("Public certificates") was not
opened. Removed: `/dynamic/fws/instance-monitoring`, "SHA256 for some regions",
the claim that the document is the same for the instance's life (the page says it is
regenerated on launch/stop-start/restart), the `-content document` openssl form and the
PKCS7/RSA-2048 conflation (corrected to SHA1+DSA vs SHA256+RSA-2048), the sts:GetCallerIdentity
and Vault recommendation, and the "tampered document" and `ec2:DescribeTags` role checks.
Sample JSON output removed in favour of the documented field list.
