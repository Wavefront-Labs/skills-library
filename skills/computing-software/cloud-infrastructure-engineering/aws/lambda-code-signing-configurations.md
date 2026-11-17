---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-code-signing-configurations
name: lambda-code-signing-configurations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, code-signing, aws-signer, supply-chain-security]
level: advanced
status: docs-checked
description: "Enforce that only signed, unaltered code deploys to Lambda with AWS Signer profiles, code signing configurations and an IAM condition requiring them."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning-create.html", "https://docs.aws.amazon.com/lambda/latest/dg/config-codesigning-policies.html", "https://docs.aws.amazon.com/signer/latest/developerguide/signing-profiles.html", "https://docs.aws.amazon.com/signer/latest/developerguide/signing-jobs-lambda.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda code signing

## 1. Signing profile
```bash
aws signer put-signing-profile --profile-name lambda_prod --platform-id AWSLambda-SHA384-ECDSA \
  --signature-validity-period value=135,type=MONTHS
```
135 months is the default and the maximum. The profile name allows A-Z, a-z, 0-9 and underscore.

## 2. Sign a package
Start a signing job with `aws signer start-signing-job`, giving the Lambda zip in an S3 source bucket, the
signing profile and an S3 destination bucket (see the CLI reference for the `--source` and `--destination`
syntax). Check the result with `describe-signing-job`. Signing fails for a zip that is empty, already signed or
malformed. Deploy the signed zip from the destination bucket.

## 3. Code signing config and attach
```bash
CSC=$(aws lambda create-code-signing-config \
  --allowed-publishers SigningProfileVersionArns=<PROFILE_VERSION_ARN> \
  --code-signing-policies UntrustedArtifactOnDeployment=Enforce --query CodeSigningConfig.CodeSigningConfigArn --output text)
aws lambda put-function-code-signing-config --function-name orders --code-signing-config-arn $CSC
aws lambda update-function-code --function-name orders --s3-bucket <DEST_BUCKET> --s3-key <SIGNED_OBJECT_KEY>
```
A configuration lists up to 20 signing profile versions. At deploy time Lambda checks integrity, expiry,
mismatch (allowed profile) and revocation. For the last three, `UntrustedArtifactOnDeployment` decides:
`Warn` (the default) allows the deploy and emits the `SignatureValidationErrors` metric and a CloudTrail entry;
`Enforce` also blocks the deploy. A failed integrity check blocks the deploy even under `Warn`.
Adding a configuration to a function with unsigned code does not stop that code running until the next deploy.
Layers added to a function with code signing must also be signed by an allowed profile.

## 4. Require it everywhere
Lambda blocks `CreateFunction` when the request lacks, or mismatches, the configuration named in an allowing
statement that carries this condition (from the AWS example policy):
```json
{"Effect":"Allow","Action":["lambda:CreateFunction"],"Resource":"*",
 "Condition":{"StringEquals":{"lambda:CodeSigningConfigArn":"<CSC_ARN>"}}}
```

## Limits
There is no extra charge, and signing does not change runtime behaviour. The Lambda page that explains
how to create configurations states that functions defined as container images do not support code signing.

## Verify
- [ ] Deploying an unsigned zip to an `Enforce` function fails with `CodeVerificationFailedException`.

## Checked
Date 2026-10-23. Lambda Developer Guide code signing pages and AWS Signer Developer Guide (profile and Lambda signing
job pages). Confirmed: platform id `AWSLambda-SHA384-ECDSA`, 135-month default and maximum validity, up to 20
profiles per configuration, Warn default and Enforce behaviour, the four validation checks,
`CodeVerificationFailedException`, `lambda:CodeSigningConfigArn` condition semantics, layers must be signed,
container images not supported. Replaced the old Deny/StringNotEquals policy with the documented Allow form,
and removed unconfirmed S3 CLI syntax and the versioned-bucket requirement.
Method: documentation only; no commands were run.
