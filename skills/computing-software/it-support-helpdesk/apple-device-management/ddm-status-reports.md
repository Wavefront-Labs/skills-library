---
id: computing-software.it-support-helpdesk.apple-device-management.ddm-status-reports
name: ddm-status-reports
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, ddm, ddm-status-reports, ddm-status, status-subscriptions]
level: practitioner
status: docs-checked
description: "Subscribe to DDM status items with a status-subscriptions configuration so devices report changes to the MDM instead of being polled."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/declarations/configurations/management.status-subscriptions.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/protocol/statusreport.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/status/management.client-capabilities.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/status/management.declarations.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ddm-status-reports

Goal: replace polling with device-pushed state.
- Subscribe with a configuration of type `com.apple.configuration.management.status-subscriptions` (iOS 15, macOS 13 and later). Its `StatusItems` array holds dictionaries with a `Name`, for example `device.identifier.serial-number`, `device.operating-system.version`, `passcode.is-compliant`, `security.certificate.list`.
- The device sends a `StatusReport` with `StatusItems` and `Errors` through the `status` endpoint (Base64 JSON in `Data`; a success is `200 OK` with an empty body). An error entry has `StatusItem` and `Reasons`, each with `Code`, optional `Description` and `Details`.
- `FullReport` true means a full replacement, not an incremental update; the system sends one as a "safety sync", typically about every 24 hours.
- `management.declarations` reports every processed declaration: `identifier`, `server-token`, `active`, `valid` (`unknown`, `invalid`, `valid`) and `reasons` for failures.
- `management.client-capabilities` is always implicitly subscribed. It reports `supported-versions`, `supported-features` and `supported-payloads` (the declarations and status items the client supports), so read it before subscribing to items an OS may not have.
- Software update state: `softwareupdate.install-state` is one of `none`, `downloading`, `prepared`, `installing`, `failed`. `passcode.is-compliant` is true when the passcode meets all policies on the device, and also true when none are set; it is not available on macOS.
Practice: start with a small set (OS version, passcode compliance, software update state) and add items only when a report needs them.
Gotcha: items are introduced in different OS versions and enrolment types (for example `softwareupdate.install-state` starts at iOS 17 and macOS 14), so gate subscriptions on the capabilities report.
Verify: after an OS update the `device.operating-system.version` value in the next status report matches the new version (for example `15.0`).

## Checked

Date: 2026-11-07. Read in full from apple/device-management raw YAML: `status-subscriptions` configuration, `StatusReport` protocol (StatusItems, Errors, FullReport and the 24-hour safety sync), `management.client-capabilities` (read to the start of supported-payloads configurations; the rest of the file, status-item lists, was not read), `management.declarations`, and the `softwareupdate.install-state`, `passcode.is-compliant` and `device.operating-system.version` status items; the `status` endpoint behaviour is from the DeclarativeManagement check-in YAML. Removed: the "PUT /status" HTTP verb, "within minutes" timing, the claim about reducing server traffic per subscription, and the Verify step about a deliberately invalid declaration. Replaced the unreadable developer.apple.com and guessed Apple deployment guide sources.
Method: documentation only; no commands were run.
