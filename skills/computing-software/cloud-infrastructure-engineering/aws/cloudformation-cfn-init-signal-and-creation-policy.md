---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-cfn-init-signal-and-creation-policy
name: cloudformation-cfn-init-signal-and-creation-policy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, cfn-init, cfn-signal, creation-policy, cfn-hup, wait-condition, bootstrap]
level: practitioner
status: docs-checked
description: "Bootstrap EC2 from CloudFormation with cfn-init metadata, report success with cfn-signal and CreationPolicy/UpdatePolicy, keep config current with cfn-hup, and debug timeouts."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-creationpolicy.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-init.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-hup.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cfn-init, cfn-signal and CreationPolicy

**Goal:** the stack only reports `CREATE_COMPLETE` when instances are actually configured and
healthy, and fails (and rolls back) when bootstrap breaks.

## 1. Template skeleton
```yaml
WebInstance:
  Type: AWS::EC2::Instance
  CreationPolicy:
    ResourceSignal: {Count: 1, Timeout: PT15M}
  Metadata:
    AWS::CloudFormation::Init:
      configSets: {default: [install, configure]}
      install:
        packages: {yum: {nginx: []}}     # cfn-init package formats: apt, msi, python, rpm, rubygems, yum, zypper
      configure:
        files:
          /etc/nginx/conf.d/app.conf:
            content: !Sub |
              server { listen 80; location / { proxy_pass http://127.0.0.1:8080; } }
            mode: "000644"
        services:
          systemd:
            nginx: {enabled: true, ensureRunning: true, files: [/etc/nginx/conf.d/app.conf]}
  Properties:
    ImageId: !Ref LatestAmiId
    InstanceType: t3.small
    IamInstanceProfile: !Ref InstanceProfile
    UserData:
      Fn::Base64: !Sub |
        #!/bin/bash
        # install aws-cfn-bootstrap here if your AMI does not already include it
        /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource WebInstance --region ${AWS::Region}
        /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebInstance --region ${AWS::Region}
```
- Init keys run in fixed order within a config: packages → groups → users → sources → files →
  commands → services. Use configSets to order multiple configs.
- `cfn-signal -e $?` sends success (0) or failure; if the required signals do not arrive before `Timeout`, creation fails.

## 2. Auto Scaling groups
```yaml
WebAsg:
  Type: AWS::AutoScaling::AutoScalingGroup
  CreationPolicy:
    ResourceSignal: {Count: 2, Timeout: PT20M}
    AutoScalingCreationPolicy: {MinSuccessfulInstancesPercent: 100}
  UpdatePolicy:
    AutoScalingRollingUpdate: {MinInstancesInService: 2, MaxBatchSize: 1, PauseTime: PT15M, WaitOnResourceSignals: true}
```
Signal with `--resource WebAsg` from each instance.

## 3. cfn-hup
Daemon that checks resource metadata for changes (`interval` in minutes, default 15) and runs your action:
`/etc/cfn/cfn-hup.conf` (stack, region, interval) and a hook file in `/etc/cfn/hooks.d/` such as `cfn-auto-reloader.conf`
(`triggers=post.update` — valid triggers are `post.add`, `post.update`, `post.remove`;
`path=Resources.WebInstance.Metadata.AWS::CloudFormation::Init`, `action=cfn-init ...`).

## 4. Debug
On the instance: `/var/log/cfn-init.log` and `/var/log/cloud-init.log` (the CloudFormation troubleshooting guide names both).
A missing signal produces a `Failed to receive N resource signal(s)` stack event.
Turn rollback off in dev (`--disable-rollback` or `--on-failure DO_NOTHING`) to keep the instance for inspection.

## Gotchas
- The instance must be able to reach the CloudFormation endpoint for cfn-init metadata and signals.
- `cfn-signal` needs permission for the CloudFormation `SignalResource` API; the other helper scripts need the describe permission named in the helper scripts reference.

## Verify
- [ ] Stack reaches CREATE_COMPLETE only after the signal; a deliberately broken package makes it roll back.
- [ ] `cfn-init.log` shows each config step succeeding.
- [ ] Metadata change + stack update triggers cfn-hup (or rolling update) as designed.

## Checked
Date: 2026-10-24. Documentation release: AWS CloudFormation User Guide (awsdocs source, December 2023 snapshot).
Confirmed: `cfn-init` section order and supported package formats; `services` support for sysvinit and systemd; `CreationPolicy` `ResourceSignal` `Count` and `Timeout`; `AutoScalingCreationPolicy.MinSuccessfulInstancesPercent`; `UpdatePolicy` `WaitOnResourceSignals` and `PauseTime`; `cfn-hup` interval default and valid triggers; log file names; `SignalResource` permission for `cfn-signal`.
Fixed: `dnf` is not a documented `cfn-init` package format (changed to `yum`). Removed as unconfirmed: the `cfn-init-cmd.log` and `cloud-init-output.log` names, the private-subnet endpoint advice and the AMI-baking advice.

Method: documentation only; no commands were run.
