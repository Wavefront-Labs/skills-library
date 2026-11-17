---
id: computing-software.cloud-infrastructure-engineering.aws.sam-nested-applications-and-serverless-application-repository
name: sam-nested-applications-and-serverless-application-repository
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sam, nested-applications, serverless-application-repository, sar, serverless-application, sam-publish]
level: practitioner
status: docs-checked
description: "Compose SAM apps from nested applications (local or from the Serverless Application Repository), pass parameters and outputs, and publish your own apps to SAR with sharing."
sources: ["https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-template-nested-applications.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-template-publishing-applications.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-template-publishing-applications-metadata-properties.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-publish.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAM nested applications and the Serverless Application Repository

## Nested application
```yaml
Resources:
  Auth:
    Type: AWS::Serverless::Application
    Properties:
      Location: ./auth/template.yaml           # local path, packaged by sam build/deploy
      Parameters: {Env: !Ref Env}
  Notifier:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: arn:aws:serverlessrepo:us-east-1:123456789012:applications/slack-notifier
        SemanticVersion: 1.4.2               # the application version to deploy
      Parameters: {SlackChannel: alerts}
Outputs:
  UserPoolId: {Value: !GetAtt Auth.Outputs.UserPoolId}
```
- Becomes a nested CloudFormation stack; outputs are read with `!GetAtt App.Outputs.<Name>`.
- Deploying nested applications requires acknowledging them with `CAPABILITY_AUTO_EXPAND`; the Serverless Application Repository
  also asks you to acknowledge IAM roles and resource policies (`CAPABILITY_IAM`, `CAPABILITY_RESOURCE_POLICY`).

## Publish your own application to SAR
```yaml
Metadata:
  AWS::ServerlessRepo::Application:
    Name: slack-notifier
    Description: Posts SNS messages to Slack
    Author: platform-team                # Name, Description and Author are required
    SpdxLicenseId: MIT
    LicenseUrl: LICENSE
    ReadmeUrl: README.md
    SemanticVersion: 1.4.2
    SourceCodeUrl: https://github.com/example/slack-notifier
```
```bash
sam package --output-template-file packaged.yaml --s3-bucket my-sar-artifacts
sam publish --template packaged.yaml --region us-east-1
aws serverlessrepo put-application-policy --application-id "$APP" \
  --statements Principals=444455556666,Actions=Deploy      # or PrincipalOrgIDs for the org
```
- The S3 bucket needs a bucket policy that grants the Serverless Application Repository read access to the packaged artifacts.
- Applications are private by default; share with specific AWS accounts (`Principals`) or an organization (`PrincipalOrgIDs`), or make them public.
- A semantic version and a license file are required only to share an application publicly.

## When to use what
- Local nested apps: split a large template, reuse a component across your stacks.
- SAR: distribute a component to many accounts/teams with versioning.

## Gotchas
- A nested application becomes a nested CloudFormation stack, updated with its parent.
- Review the IAM roles and resource policies of a third-party application before acknowledging them.

## Verify
- [ ] Parent stack shows nested stacks `CREATE_COMPLETE`; outputs resolve.
- [ ] A consumer account can deploy the shared SAR app version.

## Checked
Date: 2026-10-24. Documentation release: AWS SAM Developer Guide (awsdocs source, June 2023 snapshot) plus the botocore `serverlessrepo` model.
Confirmed: `AWS::Serverless::Application` with `Location` as a local path or `ApplicationId` plus `SemanticVersion`; `CAPABILITY_AUTO_EXPAND` for nested applications; `AWS::ServerlessRepo::Application` metadata fields (`Name`, `Description`, `Author`, `SpdxLicenseId`, `LicenseUrl`, `ReadmeUrl`, `SemanticVersion`, `SourceCodeUrl`); bucket policy requirement; private by default; policy statement members `Actions`, `Principals`, `PrincipalOrgIDs`; `sam publish` of a private version.
Removed as unconfirmed: the `serverlessrepo.amazonaws.com` principal wording, version immutability and the parent rollback claim.

Method: documentation only; no commands were run.
