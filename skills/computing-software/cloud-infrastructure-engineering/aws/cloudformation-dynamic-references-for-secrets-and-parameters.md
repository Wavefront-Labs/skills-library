---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-dynamic-references-for-secrets-and-parameters
name: cloudformation-dynamic-references-for-secrets-and-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, dynamic-references, resolve-ssm, resolve-secretsmanager, ssm-secure]
level: practitioner
status: docs-checked
description: "Use CloudFormation dynamic references (ssm, ssm-secure, secretsmanager) to keep secrets and config out of templates, with the documented limits and rotation behaviour."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-ssm.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-ssm-secure-strings.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-secretsmanager.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation dynamic references

**Goal:** resolve secrets and config when CloudFormation creates or updates a stack, so sensitive values do not sit in the template.

## Syntax
```yaml
MasterUserPassword: '{{resolve:secretsmanager:MySecret:SecretString:password}}'
ImageId: '{{resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64}}'   # String/StringList, version optional
Password: '{{resolve:ssm-secure:IAMUserPassword:10}}'                                        # SecureString, supported properties only
```
- `ssm`: `{{resolve:ssm:parameter-name:version}}` for parameters of type String or StringList. The name is case-sensitive.
  Without a version CloudFormation uses the latest version whenever the stack is created or updated.
- `ssm-secure`: `{{resolve:ssm-secure:parameter-name:version}}`. Only for properties that support it; the page lists
  them (for example `AWS::RDS::DBInstance` `MasterUserPassword`, `AWS::IAM::User` `LoginProfile` `Password`,
  `AWS::ElastiCache::ReplicationGroup` `AuthToken`). CloudFormation stores only the literal reference.
- `secretsmanager`: `{{resolve:secretsmanager:secret-id:secret-string:json-key:version-stage:version-id}}`. `SecretString`
  is the only supported `secret-string` value. With no `json-key` you get the whole secret text. With neither
  `version-stage` nor `version-id` the default is `AWSCURRENT`; do not give both. Segments cannot contain a colon.
  Use the full ARN for a secret in another account.
- `{{resolve:secretsmanager:MySecret}}` (or `MySecret::::`) returns the entire `SecretString`.

## Limits and considerations (from the pages)
- Up to 60 dynamic references per stack template.
- Do not put dynamic references or sensitive data in resource properties that are part of the resource's primary identifier
  (the Return values section of the resource reference shows what `Ref` returns).
- Not supported in `AWS::CloudFormation::Init` metadata or EC2 `UserData`. Secure values (ssm-secure, secretsmanager) are not
  supported in custom resources. Do not end a reference with a backslash.
- With transforms such as `AWS::Include` or `AWS::Serverless`, the literal string is passed to the transform and resolved
  when the change set executes.
- Permissions: `GetParameters` for `ssm` references, `GetSecretValue` for `secretsmanager`.
- `ssm` references: no drift detection; in the template `Parameters` section a version number is required (or define the
  parameter as a Systems Manager parameter type instead, which fetches the latest); parameters shared from another
  account and parameter labels are not supported. `ssm-secure`: no cross-account, labels or public parameters; not supported
  by Systems Manager in `cn-north-1` and `cn-northwest-1`.
- A rollback fails if the previous secure-string version no longer exists; the page gives `CONTINUE_UPDATE_ROLLBACK` options.

## Rotation and updates
CloudFormation retrieves a secret only during creation or an update that modifies the resource holding the reference;
changing only the secret value in Secrets Manager does not update the resource. The page recommends versionless
references with Secrets Manager automatic rotation, and explicit version-stage/version-id sparingly (testing, rollback).
To check which `ssm` version a stack operation will use, create a change set and review the processed template.

## Verify
- [ ] A change set's processed template shows the `ssm` version that will be used.
- [ ] The stack operation succeeds and the resource has the expected value; the template and stack show only the literal
  `{{resolve:...}}` text for `ssm-secure`.

## Checked
Date: 2026-11-07. Read in full: dynamic-references (general considerations), dynamic-references-ssm,
dynamic-references-ssm-secure-strings, dynamic-references-secretsmanager (best practices, considerations,
permissions, reference pattern, examples). Removed because none of these pages state them: the whole CDK section
(`SecretValue.*`, `valueForStringParameter`, `valueFromLookup`), the `ManageMasterUserPassword` and
`SecretTargetAttachment` advice, the "not in Outputs" claim, the `AWS::SSM::Parameter::Value<String>` type name, and
the `get-template` verify step; "60 verify" is now stated as the page's 60-reference limit.
Method: documentation only; no commands were run.
