---
id: computing-software.firmware-embedded-development.iot-protocols.aws-fleet-provisioning
name: aws-fleet-provisioning
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [aws-fleet-provisioning, iot-provisioning, aws-iot, fleet-provisioning, claim-certificate, provisioning-template, iot-protocols]
level: practitioner
status: docs-checked
description: "AWS IoT fleet provisioning: claim-based and trusted-user flows, templates, pre-provisioning hooks and the swap to a permanent certificate."
sources:
  - https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS IoT fleet provisioning

**Goal:** Give each device its own certificate on first connection.

## Steps
1. Two modes: provisioning by claim, and provisioning by trusted user.
2. Claim, before shipping: create a provisioning template (CreateProvisioningTemplate), create claim certificates and keys, register them with an IoT policy that restricts them to provisioning (Connect, plus Publish/Receive/Subscribe on $aws/certificates/create/* and $aws/provisioning-templates/<template>/provision/*), give a provisioning role the AWSIoTThingsRegistration managed policy, and embed the claim certificate in the device.
3. On first boot the device connects with the claim certificate, then gets a permanent certificate with CreateKeysAndCertificate (AWS CA) or CreateCertificateFromCsr (private key stays on the device).
4. The device calls RegisterThing. The template defines the cloud resources (thing, attributes, groups); thing groups must exist beforehand.
5. certificateOwnershipToken expires after one hour; RegisterThing must be called before then, or an unactivated, unattached certificate is deleted. The device can request a new one.
6. The device saves the permanent certificate, disconnects from the claim-certificate session, and reconnects with the permanent certificate.
7. Trusted user: an app user with an IAM role (iot:CreateProvisioningClaim on the template) gets a temporary claim certificate valid five minutes, hands it to the device with config such as Wi-Fi credentials, and the device must obtain its permanent certificate within five minutes.
8. Pre-provisioning hook: a Lambda returning allowProvisioning and parameterOverrides, wired in with --pre-provisioning-hook; AWS IoT needs lambda:InvokeFunction permission, with source-arn or source-account conditions.

## Gotcha
Claim private keys must be protected at all times, including on the device. Monitor CloudWatch metrics and logs for misuse, and turn the claim certificate off if misuse is seen.

## Verify
- [ ] Thing created with its own unique certificate
- [ ] Hook rejects an unapproved device (allowProvisioning false)
- [ ] Claim certificate policy allows only the provisioning topics

## Checked

2026-11-08. Confirmed on the AWS page: both modes, template creation, claim policy, provisioning role, API calls, token and claim expiry, reconnect step, hook output and permission. Removed as unsupported: the "serial number approval" example is generic (the page only shows allowProvisioning and parameterOverrides), mention of just-in-time provisioning/registration as alternatives (not on this page), and the advice to deactivate the claim cert after the production window (page only says to disable it on suspected misuse).
Method: documentation only; no commands were run.
