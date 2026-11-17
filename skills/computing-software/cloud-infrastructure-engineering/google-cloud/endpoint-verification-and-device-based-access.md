---
id: computing-software.cloud-infrastructure-engineering.google-cloud.endpoint-verification-and-device-based-access
name: endpoint-verification-and-device-based-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, endpoint-verification, device-trust, access-levels, context-aware-access, beyondcorp, chrome-enterprise-premium, identity-aware-proxy]
level: advanced
status: docs-checked
description: "Collect device posture with Endpoint Verification, express it as Access Context Manager device policies, and require trusted devices for IAP apps."
sources: ["https://docs.cloud.google.com/endpoint-verification/docs/overview", "https://docs.cloud.google.com/access-context-manager/docs/create-basic-access-level", "https://docs.cloud.google.com/iap/docs/cloud-iap-context-aware-access-howto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Endpoint Verification and device trust

## 1. Deploy Endpoint Verification
Endpoint Verification is part of Chrome Enterprise Premium and is available to Google Cloud, Cloud
Identity and Google Workspace customers. It is a Chrome extension that collects and reports
device inventory by syncing with Google Cloud, building an inventory of devices with Chrome that
access your organisation's data (including encryption status and OS). Third-party clients such as
CrowdStrike and Microsoft Intune can supply real-time device information to Access Context
Manager through it. Roll the extension out to managed browsers with your normal Chrome policy
tooling; follow the overview page for the current admin steps.

## 2. Turn posture into an access level
A basic level's `devicePolicy` accepts (Access Context Manager API `DevicePolicy`):
`requireScreenlock`, `osConstraints` (each with a required `osType` and optional
`minimumVersion`), `allowedDeviceManagementLevels`, `allowedEncryptionStatuses`
(`ENCRYPTED`, `UNENCRYPTED`, ...), `requireCorpOwned` and `requireAdminApproval`.
`osType` values include `DESKTOP_MAC`, `DESKTOP_WINDOWS`, `DESKTOP_LINUX`, `DESKTOP_CHROME_OS`,
`ANDROID`, `IOS`.
```yaml
# corp_device.yaml  (basic level spec)
- devicePolicy:
    requireScreenlock: true
    allowedEncryptionStatuses: [ENCRYPTED]
    requireCorpOwned: true
    osConstraints:
    - osType: DESKTOP_MAC
      minimumVersion: <MIN_MAC_VERSION>
    - osType: DESKTOP_WINDOWS
      minimumVersion: <MIN_WINDOWS_VERSION>
    - osType: DESKTOP_CHROME_OS
```
```bash
POLICY=$(gcloud access-context-manager policies list --organization=<ORG_ID> --format='value(name)')
gcloud access-context-manager levels create corp_device --policy=$POLICY \
  --title="Corp managed device" --basic-level-spec=corp_device.yaml
```

## 3. Enforce on IAP
IAP access levels work with IAM conditional bindings: bind the IAP-secured Web App User role and
add the access level as the condition (console), or edit the project's `policy.yaml` from
`gcloud iap web get-iam-policy` (gcloud supports only project-level conditional bindings). See the
IAP context-aware access guide for the exact steps.

## Gotchas
- Device attributes in access levels need a Chrome Enterprise Premium licence; licence validation happens when you configure the access level, not at runtime.
- Test with a small group first and keep a break-glass admin who is not subject to the device level, so a bad level cannot lock admins out.

## Verify
- [ ] The device list shows encryption and OS version for a test laptop.
- [ ] A device failing the level is denied on the IAP app; one passing it is allowed.

## Checked
2026-10-31. Confirmed against the Endpoint Verification overview (Chrome extension, inventory, CrowdStrike and Intune, Chrome Enterprise Premium), the Access Context Manager v1 discovery document (`DevicePolicy` and `OsConstraint` fields and enums), the basic access level page (`devicePolicy`, `osType`, `minimumVersion` format) and the IAP context-aware access guide (access levels with IAM conditions, Chrome Enterprise Premium licence for device attributes, validation at configuration time, project-level gcloud conditional bindings). Removed: Admin console menu paths, helper app details, example version numbers, CEL device attributes, the console and APIs app assignment, sync timing and the IAP `--condition` command and the service-account device-context claim (not confirmed in fetched pages).
Method: documentation only; no commands were run.
