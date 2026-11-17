---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-intrinsic-functions
name: cloudformation-intrinsic-functions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, fn-sub-getatt, intrinsic-function-reference, fn-importvalue, fn-foreach, language-extensions, intrinsic-functions]
level: practitioner
status: docs-checked
description: "Use CloudFormation intrinsics precisely: Sub vs Join, GetAtt and Ref returns, ImportValue coupling, If and conditions, and Fn::ForEach with the LanguageExtensions transform."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-sub.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-importvalue.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-foreach.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/transform-aws-languageextensions.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-findinmap-enhancements.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation intrinsic functions

## Fn::Sub (prefer over Join)
```yaml
BucketArn: !Sub "arn:${AWS::Partition}:s3:::${Bucket}/*"
Url: !Sub "https://${Api}.execute-api.${AWS::Region}.${AWS::URLSuffix}/${Stage}"
Script: !Sub |
  echo ${!HOME}        # ${!Literal} escapes to ${Literal}
  echo ${Queue.Arn}    # ${Resource.Attribute} = GetAtt
Name: !Sub
  - "${Prefix}-${AWS::StackName}"
  - Prefix: !FindInMap [Env, !Ref Env, Prefix]
```

## Ref vs GetAtt
- `!Ref` returns a resource-specific value: bucket name, queue URL (not ARN), instance id, parameter value.
- `!GetAtt Queue.Arn`, `!GetAtt Db.Endpoint.Address`: the attribute list per resource is in each resource's "Return values" section.
- Check each resource's return values: `Ref` on `AWS::SQS::Queue` returns the queue URL; on `AWS::SNS::Topic` it returns the topic ARN.

## Cross-stack: Fn::ImportValue
```yaml
Outputs:
  VpcId: {Value: !Ref Vpc, Export: {Name: !Sub "${AWS::StackName}-VpcId"}}
# consumer
VpcId: !ImportValue network-prod-VpcId
```
- You can't modify or remove an output value that another stack references, which freezes the
  producer. Prefer SSM parameters (`{{resolve:ssm:/net/vpc-id}}` or `AWS::SSM::Parameter::Value<String>`) for values that may change.
- Cross-stack references work only within the same Region (`Fn::ImportValue` imports only values exported in the same Region).

## Conditions
```yaml
Conditions:
  IsProd: !Equals [!Ref Env, prod]
Resources:
  Db:
    Properties:
      MultiAZ: !If [IsProd, true, false]
      BackupRetentionPeriod: !If [IsProd, 14, !Ref AWS::NoValue]   # NoValue removes the property
```

## Fn::ForEach (needs the transform)
```yaml
Transform: AWS::LanguageExtensions
Resources:
  Fn::ForEach::Queues:
    - Name
    - [orders, payments, refunds]
    - "Queue${Name}":
        Type: AWS::SQS::Queue
        Properties: {QueueName: !Sub "${Name}-${Env}"}
```
- The same transform adds `Fn::Length` and `Fn::ToJsonString` (long form only; the short `!Length` form is not supported) and
  lets `Fn::FindInMap` use intrinsic functions in its fields plus an optional `DefaultValue`.
- The transform must be declared at the top level with the literal string `AWS::LanguageExtensions`; with `AWS::Serverless`,
  list it first. Its functions work in `Resources`, `Conditions` and `Outputs` only.
- Macros and transforms are processed through a change set (`CAPABILITY_AUTO_EXPAND` lets you execute directly).
- With `&{Name}` in the output key, collection values may contain non-alphanumeric characters; `${Name}` is for plain values.

## Other useful ones
`Fn::Select` + `Fn::GetAZs` (`!Select [0, !GetAZs ""]`; `GetAZs` returns Availability Zones alphabetically), `Fn::Split`, `Fn::Cidr`
(`!Cidr [!GetAtt Vpc.CidrBlock, 6, 8]`), `Fn::Base64` for UserData, dynamic references `{{resolve:secretsmanager:...}}`
(at most 60 dynamic references per template).

## Verify
- [ ] `aws cloudformation validate-template` passes.
- [ ] The change set shows the expected values; review the processed template when transforms or macros are used.

## Checked
Date: 2026-10-24. Documentation release: AWS CloudFormation User Guide (awsdocs source, December 2023 snapshot) and the current CloudFormation Template Reference pages for `AWS::LanguageExtensions`, `Fn::ForEach` and the quotas page.
Confirmed: `${!Literal}` escape in `Fn::Sub`; `Ref` return values for SQS (URL) and SNS (ARN); ImportValue same-Region rule and no change to referenced outputs; `ssm` dynamic reference pattern with optional version; `Fn::ForEach` structure, `${Identifier}` and `&{Identifier}`; `Fn::Length`, `Fn::ToJsonString`, FindInMap enhancements and the short-form restriction; 60 dynamic references per template; `AWS::NoValue`.
Removed as unconfirmed: intrinsic functions in `DeletionPolicy` and `UpdateReplacePolicy`, `get-template --template-stage Processed`, and the claim that `cfn-lint` is part of the checks.

Method: documentation only; no commands were run.
