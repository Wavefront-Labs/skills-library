---
id: computing-software.cloud-infrastructure-engineering.aws.ssm-distributor-packages
name: ssm-distributor-packages
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, systems-manager, ssm, distributor, aws-configureawspackage, software-packages, package-manifest]
level: practitioner
status: docs-checked
description: "Package software with SSM Distributor: platform zips and manifest, package versions, installing with AWS-ConfigureAWSPackage and keeping it installed via State Manager."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/distributor.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/distributor-working-with-packages-create.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/distributor-working-with-packages-deploy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSM Distributor packages

**Goal:** ship an agent or internal tool to mixed Linux/Windows fleets as a versioned package,
installed and upgraded by Systems Manager instead of bespoke scripts.

## AWS-published packages
Packages published by Amazon appear in the Distributor Packages list (for example `AmazonCloudWatchAgent`
and `AWSPVDriver`), alongside third-party packages.
```bash
aws ssm send-command --document-name AWS-ConfigureAWSPackage \
  --targets Key=tag:Env,Values=prod \
  --parameters '{"action":["Install"],"name":["AmazonCloudWatchAgent"],"installationType":["Uninstall and reinstall"]}'
```
- `installationType`: `Uninstall and reinstall` (default) or `In-place update` (adds new or updated files to an
  existing installation without taking the application offline; you supply your own update script).
- If you give no version, Run Command installs the default version selected in Distributor.

## Create your own package
One zip per platform (and architecture where needed) with install and uninstall scripts and the payload, plus a JSON manifest:
```json
{"schemaVersion":"2.0","version":"1.4.0","publisher":"platform-team",
 "packages":{"amazon":{"_any":{"x86_64":{"file":"tool-linux-amd64.zip"},"arm64":{"file":"tool-linux-arm64.zip"}}},
             "windows":{"_any":{"_any":{"file":"tool-windows.zip"}}}},
 "files":{"tool-linux-amd64.zip":{"checksums":{"sha256":"..."}},
          "tool-linux-arm64.zip":{"checksums":{"sha256":"..."}},
          "tool-windows.zip":{"checksums":{"sha256":"..."}}}}
```
```bash
aws s3 cp dist/ s3://ssm-packages/tool/1.4.0/ --recursive
aws ssm create-document --name OurTool --document-type Package --content file://manifest.json \
  --attachments Key=SourceUrl,Values=s3://ssm-packages/tool/1.4.0/ --version-name 1.4.0
aws ssm update-document --name OurTool --content file://manifest.json \
  --attachments Key=SourceUrl,Values=s3://ssm-packages/tool/1.5.0/ --version-name 1.5.0 --document-version '$LATEST'
aws ssm update-document-default-version --name OurTool --document-version 2
```
Manifest structure is platform, then platform version, then architecture. `_any` matches all versions of the
parent element, and a major release plus wildcard such as `7.*` is allowed for versions. Simple mode in the console
accepts `.rpm`, `.msi` or `.deb` files (no spaces in file names), generates the manifest and the install and uninstall
scripts for you; in-place update packages need your own update script.

## Keep it installed
Create a State Manager association that installs or updates the package on a schedule so the installation
always includes the default version. Tag new managed nodes and target the tag in the association: State Manager
installs the package on nodes with matching tags.

## Gotchas
- A package shared from another account is referenced by its package ARN in the `name` parameter.

## Verify
- [ ] `describe-document --name OurTool` shows versions; install succeeds on each platform.

## Checked
2026-10-28: Confirmed against the Systems Manager User Guide pages distributor, distributor-working-with-packages-create and distributor-working-with-packages-deploy: Amazon-published packages (AmazonCloudWatchAgent, AWSPVDriver), AWS-ConfigureAWSPackage with action Install and installationType (default Uninstall and reinstall, In-place update), manifest schema 2.0 structure with version, publisher, packages, files, sha256 checksums, _any and 7.* wildcards, Simple mode file types, create-document --document-type Package with --attachments SourceUrl and --version-name, --document-version, State Manager scheduling with tag targets, ARN reference for shared packages. The SSM commands passed check_commands.py. Read end to end. Removed as unconfirmed: the other AWS package names, the complete platform key list, idempotent/exit-code advice, private-subnet endpoint note, modify-document-permission sharing, and the AWS:Application inventory check.

Method: documentation only; no commands were run.
