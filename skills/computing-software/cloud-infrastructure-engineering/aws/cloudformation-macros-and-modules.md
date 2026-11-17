---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-macros-and-modules
name: cloudformation-macros-and-modules
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, cfn-macros, cfn-modules, transform, fn-transform, language-extensions, fn-foreach, aws-include, capability-auto-expand, cloudformation-registry, template-reuse]
level: advanced
status: docs-checked
description: "Reuse and generate CloudFormation: AWS::LanguageExtensions (Fn::ForEach), AWS::Include, custom macros in Lambda, and registry modules, with CAPABILITY_AUTO_EXPAND and debugging."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros-overview.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros-author.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/transform-aws-languageextensions.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-foreach.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/modules.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/module-ref-resources.html", "https://github.com/aws-cloudformation/cloudformation-cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation macros, transforms and modules

**Goal:** stop copy-pasting the same 200 lines of YAML: loop over lists, share snippets and
package a standard component (an encrypted, logged bucket) that teams consume as one
resource — staying in plain CloudFormation.

## 1. Pick the mechanism
| Need | Use |
|---|---|
| Loops (`Fn::ForEach`), `Fn::Length`, `Fn::ToJsonString` | `AWS::LanguageExtensions` transform (a macro hosted by CloudFormation) |
| Paste a shared snippet from S3 | `AWS::Include` (hosted macro) |
| Serverless shorthand | `AWS::Serverless-2016-10-31` (SAM; hosted macro) |
| Arbitrary template rewriting | Custom **macro** (your Lambda) |
| Versioned reusable component with parameters | Registry **module** (`Org::Svc::Name::MODULE`) |

## 2. LanguageExtensions loop
```yaml
Transform: AWS::LanguageExtensions
Parameters:
  Queues: { Type: CommaDelimitedList, Default: "orders,payments,refunds" }
Resources:
  Fn::ForEach::Queue:
    - Name
    - !Ref Queues
    - "${Name}Queue":
        Type: AWS::SQS::Queue
        Properties: { QueueName: !Sub "app-${Name}", SqsManagedSseEnabled: true }
```
`${Name}` or `&{Name}` in the output key and value is replaced with each collection item; the output key (the resource's logical ID here) must come out alphanumeric, and `&{Name}` lets the collection contain non-alphanumeric characters. The loop name must be unique and must not clash with a resource logical ID. `Fn::ForEach` works only in `Resources`, `Conditions` and `Outputs`, and the transform must be declared at the top level. Short-form YAML (`!Length`) is not supported for the functions this transform adds; use `Fn::Length`. If you combine it with `AWS::Serverless`, list `AWS::LanguageExtensions` first. The AWS SAM CLI does not support `Fn::ForEach`.

## 3. Custom macro
```yaml
# macro stack
MacroFn:
  Type: AWS::Lambda::Function
  Properties:
    Runtime: python3.12
    Handler: index.handler
    Role: !GetAtt MacroRole.Arn
    Code:
      ZipFile: |
        def handler(event, _):
            frag = event["fragment"]
            owner = event["templateParameterValues"].get("Owner", "unknown")
            for res in frag.get("Resources", {}).values():
                res.setdefault("Properties", {}).setdefault("Tags", []).append({"Key": "owner", "Value": owner})
            return {"requestId": event["requestId"], "status": "success", "fragment": frag}
Macro:
  Type: AWS::CloudFormation::Macro
  Properties: { Name: AddOwnerTags, FunctionName: !GetAtt MacroFn.Arn }
```
Use: top-level `Transform: [AddOwnerTags]` (the macro sees the whole template except the `Transform` section) or
`Fn::Transform: {Name: AddOwnerTags, Parameters: {...}}` on a snippet (the macro sees the sibling nodes). The Lambda receives `region`, `accountId`, `fragment`, `transformId`, `params`, `requestId` and `templateParameterValues`, and must return `requestId` (matching the request), `status` (`success`; anything else is treated as a failure), `fragment` and optionally `errorMessage`, which CloudFormation shows in the stack events. The returned fragment must be valid JSON and the resulting template must be valid. Optional `LogGroupName` and `LogRoleArn` properties on the macro send error logs to CloudWatch Logs.
The example blindly adds `Tags`; real macros must check that the resource type supports
the property.

## 4. Modules
```bash
cfn init                         # CloudFormation CLI wizard: choose "module", name Org::Storage::SecureBucket::MODULE
# fragments/bucket.json holds Parameters + Resources (bucket, policy, logging)
cfn submit --set-default         # registers the module in this account/Region and makes the submitted version the default
```
Consume:
```yaml
Resources:
  Data:
    Type: Org::Storage::SecureBucket::MODULE
    Properties: { BucketName: app-data-prod }
```
A resource inside a module is addressed by combining the module's logical name in your template with the resource's logical name in the module, with or without a period: `Data.Bucket` or `DataBucket`, e.g. `!GetAtt Data.Bucket.Arn`. Module outputs become template outputs named from the module logical name plus the output name; module parameters are not propagated to template parameters. Stack-level tags go to the resources the module creates. The registry manages module versions and account and Regional availability; quotas apply to the processed template.

## 5. Deploying templates with transforms
```bash
aws cloudformation deploy --template-file t.yaml --stack-name s \
  --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
aws cloudformation get-template --stack-name s --template-stage Processed   # see the expanded result
```
CloudFormation recommends change sets for templates with macros, because they show what the processed template does; `CAPABILITY_AUTO_EXPAND` lets a stack be created or updated directly without that review, so use it only when you know what the macro does. A macro that adds IAM resources also needs the IAM capabilities acknowledged.

## Gotchas
- A macro can be used only in the account where its `AWS::CloudFormation::Macro` resource was created, and the name must be unique per account. To reuse one function across accounts, allow cross-account access on the Lambda function and create a macro definition in each account. Macros are supported only in Regions where Lambda is available.
- Macro failures appear as `Transform <account>::<macro> failed with: <errorMessage>`; log the incoming `fragment` and test with a saved event.
- StackSets: you can create a macro through a stack set with self-managed permissions; StackSets does not support creating or updating stack sets with service-managed permissions from templates that reference macros, and a stack set whose template uses macros must be created or updated directly (no change set review).
- Macros are not processed recursively, `Fn::ImportValue` is not supported in macros, and a macro cannot return modules in its processed content (macros are evaluated before modules).

## Verify
- [ ] `get-template --template-stage Processed` shows the expected expanded resources.
- [ ] A change set for the macro-using stack lists only the intended changes.
- [ ] `aws cloudformation describe-type --type MODULE --type-name Org::Storage::SecureBucket::MODULE` shows the default version.

## Checked
Date: 2026-10-24. Sources: CloudFormation User Guide and Template Reference pages (fetched 2026-10-24), CloudFormation CLI README (main), botocore CloudFormation model (TemplateStage Original/Processed, CAPABILITY_AUTO_EXPAND, RegistryType MODULE).
Confirmed: macro event and response fields, status handling, AWS::CloudFormation::Macro properties (Name, FunctionName, LogGroupName, LogRoleArn), Transform versus Fn::Transform scope, account scope and cross-account reuse, StackSets limits for macros, macro restrictions (no recursion, no Fn::ImportValue, modules not returned), AWS::LanguageExtensions functions (Fn::ForEach, Fn::Length, Fn::ToJsonString), ForEach syntax and substitution rules, section restrictions, short-form limitation, SAM CLI limitation, module logical-name combination rule, module output/parameter/tag behaviour, cfn init and cfn submit --set-default.
Corrected: StackSets can use macros with self-managed permissions (not 'cannot use macros directly'); AWS::Include and AWS::Serverless are hosted macros; status failure wording now matches the documented 'anything other than success'.
Removed as unconfirmed: default-deletion-policy feature of LanguageExtensions, module version roll-out advice, module sharing via StackSets.
Method: documentation only; no commands were run.
