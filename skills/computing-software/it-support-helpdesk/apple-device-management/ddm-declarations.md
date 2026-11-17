---
id: computing-software.it-support-helpdesk.apple-device-management.ddm-declarations
name: ddm-declarations
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, ddm, ddm-declarations, declarations, activations]
level: practitioner
status: docs-checked
description: "Use DDM configurations, assets, activations and management declarations, and the DeclarativeManagement sync endpoints, to let devices apply settings autonomously."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/checkin/declarativemanagement.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/declarativemanagement.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/declarations/activations/simple.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/protocol/declarationitemsresponse.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ddm-declarations

Goal: understand the four declaration types before authoring or reading DDM payloads.
- Types: configurations, assets, activations and management declarations. The manifest (`DeclarationItemsResponse`) lists them under `Activations`, `Configurations`, `Assets` and `Management`, each item with an `Identifier` and a `ServerToken`.
- A declaration is JSON with `Type` (for example `com.apple.configuration.softwareupdate.enforcement.specific`), `Identifier`, `ServerToken` and `Payload`.
- The server computes `ServerToken` over the entire declaration content so the value changes whenever the content changes; the device uses it to see whether its copy differs.
- `com.apple.activation.simple` activates a set of configurations. It takes `StandardConfigurations` (identifiers of configurations to install; one failing does not stop the others) and an optional `Predicate` (a predicate format string); the activation installs only when the predicate is true or absent.
- Turn it on with the MDM `DeclarativeManagement` command (iOS 15, macOS 13, tvOS 16, visionOS 1.1, watchOS 10 and later). The first one enables the engine on the device; later ones trigger a sync. `Data` is a base64 `TokensResponse`.
- The device then calls the server's check-in endpoint (`MessageType` `DeclarativeManagement`) with `Endpoint` set to `tokens`, `declaration-items`, `status`, or `declaration/<type>/<identifier>` where type is `activation`, `asset`, `configuration` or `management`.
- If the server returns `404 Not Found` for a declaration the device asks for, the device removes the matching declaration it holds.
Gotcha: the legacy and declarative paths overlap (software update, passcode); a deprecated profile key points to the declaration that replaces it, so use one path per setting.
Verify: the `management.declarations` status item lists each processed declaration with `identifier`, `server-token`, `active` and `valid` (`unknown`, `invalid` or `valid`), plus `reasons` when invalid.

## Checked

Date: 2026-11-07. Read in full: apple/device-management raw YAML for the `DeclarativeManagement` check-in (endpoint values and 404 rule), the `DeclarativeManagement` MDM command (introduced versions, `Data`), `activation.simple` (StandardConfigurations, Predicate), `DeclarationItemsResponse` (the four arrays, Identifier/ServerToken, ServerToken computation) and `status/management.declarations` (identifier, server-token, active, valid, reasons). The `Type`/`Identifier`/`ServerToken`/`Payload` shape was read in the repository's example JSON for `softwareupdate.enforcement.specific`. Removed: Jamf Pro Blueprints claim, the unverified "predicate-gated supervised device" example and the invented Verify about a group. The Apple Platform Deployment DDM page URL previously cited redirected to the guide's welcome page, so it was dropped.
Method: documentation only; no commands were run.
