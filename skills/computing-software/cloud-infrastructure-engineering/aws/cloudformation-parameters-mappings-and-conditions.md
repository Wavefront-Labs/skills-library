---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-parameters-mappings-and-conditions
name: cloudformation-parameters-mappings-and-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, ssm-parameter-types, cfn-mappings, cfn-conditions, template-parameters, aws-specific-parameter-types]
level: practitioner
status: docs-checked
description: "Write reusable CloudFormation templates with typed parameters (AWS-specific and SSM parameter types), constraints, Mappings with FindInMap, Conditions, and the Rules section."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/rules-section-structure.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation parameters, mappings and conditions

## 1. Typed parameters
```yaml
Parameters:
  Env:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev
  VpcId:
    Type: AWS::EC2::VPC::Id                 # validated against the account at deploy
  AppSubnets:
    Type: List<AWS::EC2::Subnet::Id>
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
  LatestAmi:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/<public-parameter-path-from-the-AMI-provider>
  DbPasswordParam:
    Type: AWS::SSM::Parameter::Value<String>
    NoEcho: true
  InstanceType:
    Type: String
    AllowedPattern: '^(t3|m7i|c7i)\.(medium|large|xlarge)$'
    ConstraintDescription: must be an approved instance type
```
- AWS-specific types (`AWS::EC2::SecurityGroup::Id`, `AWS::Route53::HostedZone::Id`, ...)
  give console dropdowns and early validation.
- SSM parameter types take the value from Parameter Store when you create or update the stack; a later SSM change is
  picked up on the next stack update.
- CloudFormation does not support template parameters of the `SecureString` SSM type; use dynamic
  references (`{{resolve:ssm-secure:...}}` for supported resource properties, or `{{resolve:secretsmanager:...}}`).
- `NoEcho` masks the value (asterisks) in describe calls and events, but not in places such as `Metadata` or `Outputs`;
  never output secrets.

## 2. Mappings
```yaml
Mappings:
  EnvConfig:
    dev:     {InstanceType: t3.medium, MinSize: 1, MultiAZ: "false"}
    prod:    {InstanceType: m7i.large, MinSize: 3, MultiAZ: "true"}
Resources:
  Asg:
    Properties:
      MinSize: !FindInMap [EnvConfig, !Ref Env, MinSize]
```
Mappings are static: you can't include parameters, pseudo parameters or intrinsic functions in the `Mappings` section
(`Fn::FindInMap` keys can use `Ref`; the `AWS::LanguageExtensions` transform adds more functions in `FindInMap` fields and a `DefaultValue`).
Region maps (`!FindInMap [RegionMap, !Ref 'AWS::Region', Ami]`) are the classic use, largely replaced
by SSM public parameters.

## 3. Conditions
```yaml
Conditions:
  IsProd: !Equals [!Ref Env, prod]
  CreateReplica: !And [!Condition IsProd, !Not [!Equals [!Ref 'AWS::Region', us-east-1]]]
Resources:
  ReadReplica:
    Type: AWS::RDS::DBInstance
    Condition: CreateReplica
  Db:
    Properties:
      MultiAZ: !If [IsProd, true, false]
      BackupRetentionPeriod: !If [IsProd, 35, !Ref AWS::NoValue]
Outputs:
  ReplicaEndpoint:
    Condition: CreateReplica
    Value: !GetAtt ReadReplica.Endpoint.Address
```
`AWS::NoValue` removes the property (the resource behaves as if it were not specified). Resources with a false condition are not
created, so anything that references them must be under the same condition or use `!If`.

## 4. Rules (validate combinations before deploy)
```yaml
Rules:
  ProdNeedsLargeInstances:
    RuleCondition: !Equals [!Ref Env, prod]
    Assertions:
      - Assert: !Contains [[m7i.large, m7i.xlarge], !Ref InstanceType]
        AssertDescription: prod requires m7i.large or larger
```
Rules validate parameter values before resources are created, using rule-specific functions such as `Fn::Contains`.

## Gotchas
- Per-template quotas: 200 parameters, 200 mappings (200 attributes each), 200 outputs, 500 resources; a parameter value is
  at most 4,096 bytes. Split into nested stacks when you hit them.
- Changing a parameter's type or removing a parameter used by existing stacks breaks
  updates; add new parameters with defaults.

## Verify
- [ ] `aws cloudformation validate-template` succeeds.
- [ ] Change sets for dev and prod parameter files produce the expected resource differences.
- [ ] Rules reject an invalid prod parameter combination before resources are created.

## Checked
Date: 2026-10-24. Documentation release: AWS CloudFormation User Guide (awsdocs source, December 2023 snapshot) and the current quotas page.
Confirmed: AWS-specific parameter types (`AWS::EC2::VPC::Id`, `List<AWS::EC2::Subnet::Id>`, `AWS::EC2::KeyPair::KeyName`); SSM parameter types; no `SecureString` parameter type; `NoEcho` behaviour; Mappings cannot include parameters or intrinsic functions; `Rules` with `RuleCondition`, `Assertions` and `Fn::Contains`; `AWS::NoValue`; quotas of 200 parameters, 200 mappings, 200 attributes, 200 outputs, 500 resources and 4,096-byte parameter values.
Removed as unconfirmed: the example AMI parameter path (now a placeholder), the CLI escaping of list parameter values and the claim that Rules fail change set creation.

Method: documentation only; no commands were run.
