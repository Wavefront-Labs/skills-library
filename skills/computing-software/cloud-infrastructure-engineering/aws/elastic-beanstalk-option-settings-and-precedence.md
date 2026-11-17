---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-beanstalk-option-settings-and-precedence
name: elastic-beanstalk-option-settings-and-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-beanstalk, option-settings, configuration-precedence, ebextensions-options, saved-configurations, environment-properties]
level: practitioner
status: docs-checked
description: "Set Elastic Beanstalk configuration options without surprises: namespaces, the precedence of API/console vs saved config vs .ebextensions vs defaults, and removing overrides."
sources: ["https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-general.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-configuration-methods-after.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Beanstalk option settings and precedence

## 1. Namespaces
Settings are `Namespace / OptionName = Value`. Common ones:
| Namespace | Examples |
|---|---|
| `aws:autoscaling:asg` | `MinSize`, `MaxSize` |
| `aws:autoscaling:launchconfiguration` | `InstanceType` (legacy), `IamInstanceProfile`, `SecurityGroups`, `RootVolumeType` |
| `aws:ec2:instances` | `InstanceTypes` (list), `EnableSpot`, `SpotFleetOnDemandBase` |
| `aws:elasticbeanstalk:environment` | `EnvironmentType` (`LoadBalanced`/`SingleInstance`), `LoadBalancerType`, `ServiceRole` |
| `aws:elasticbeanstalk:application:environment` | environment properties (env vars) |
| `aws:elasticbeanstalk:command` | `DeploymentPolicy`, `BatchSize`, `Timeout` |
| `aws:elasticbeanstalk:healthreporting:system` | `SystemType=enhanced` |
| `aws:elbv2:listener:443` | `Protocol`, `SSLCertificateArns` |
| `aws:elasticbeanstalk:environment:process:default` | `HealthCheckPath`, `Port` |
| `aws:ec2:vpc` | `VPCId`, `Subnets`, `ELBSubnets`, `AssociatePublicIpAddress` |

## 2. Precedence (highest first)
1. **Settings applied directly to the environment**: console changes, `eb setenv`,
   `aws elasticbeanstalk update-environment --option-settings`, `eb create` options.
2. **Saved configurations** (when creating from one).
3. **Configuration files** in the source bundle: `.ebextensions/*.config` `option_settings`.
4. **Default values** of the platform.
The trap: once a value is set at level 1 (e.g. someone changed instance type in the
console), changing `.ebextensions` has **no effect**. The console shows the effective
value but not where it came from.

## 3. Inspect effective values and their source
```bash
aws elasticbeanstalk describe-configuration-settings --application-name app \
  --environment-name app-prod \
  --query 'ConfigurationSettings[0].OptionSettings[?Namespace==`aws:autoscaling:asg`]'
eb config   # EB CLI: edit the environment configuration directly
```

## 4. Removing a level-1 override so .ebextensions applies
```bash
aws elasticbeanstalk update-environment --environment-name app-prod \
  --options-to-remove Namespace=aws:autoscaling:asg,OptionName=MaxSize
```

## 5. Recommended practice
- Pick one source of truth. For teams using IaC, set everything via CloudFormation/
  Terraform/CDK option settings (they go through the environment API, so they are
  level-1 direct settings) and keep
  `.ebextensions` for things that are code-adjacent (packages, files, commands, hooks).
- Prefer Elastic Beanstalk environment secrets (an option whose value is the ARN of a
  Secrets Manager secret or Systems Manager Parameter Store parameter) over plain
  environment properties.
- Saved configurations (`eb config save prod --cfg prod-baseline`) give a portable snapshot
  for creating identical environments; store the YAML in Git.

## Gotchas
- Console and EB CLI changes also write directly to the environment, so they win over
  `.ebextensions`; the docs say to remove such recommended-value settings if you want
  configuration files to set the same options.
- Check `/var/log/eb-engine.log` on an instance for deployment errors.

## Verify
- [ ] `describe-configuration-settings` matches IaC for key namespaces.
- [ ] A change in `.ebextensions` takes effect on deploy (proving no level-1 override hides it).
- [ ] No secrets in `aws:elasticbeanstalk:application:environment`.

## Checked
2026-10-28: Confirmed against the Beanstalk Developer Guide pages command-options, command-options-general and environment-configuration-methods-after: the four-level precedence (settings applied directly to the environment, saved configuration, .ebextensions configuration files, defaults), the namespaces and option names in the table (MinSize/MaxSize, IamInstanceProfile, EnableSpot, SpotFleetOnDemandBase, EnvironmentType, LoadBalancerType, ServiceRole, DeploymentPolicy, SystemType, HealthCheckPath, SSLCertificateArns, VPCId, ELBSubnets, AssociatePublicIpAddress, RootVolumeType), environment secrets from Secrets Manager or Parameter Store, eb-engine.log, and the eb config / eb setenv methods. Read end to end. Removed: the 4 KB property size limit, the claim about tabs silently skipping files, the claim that some options are creation-only, and the .platform/hooks secrets advice.

Method: documentation only; no commands were run.
