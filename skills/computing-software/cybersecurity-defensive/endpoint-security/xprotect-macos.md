---
id: computing-software.cybersecurity-defensive.endpoint-security.xprotect-macos
name: xprotect-macos
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [xprotect, macos-antimalware, gatekeeper, notarization, macos-security, antimalware]
level: practitioner
status: docs-checked
description: "Understand macOS built-in anti-malware as Apple documents it: Gatekeeper, notarisation, XProtect signatures and remediation, updates, user overrides and managed-Mac limits."
sources: ["https://support.apple.com/guide/security/protecting-against-malware-sec469d47bd8/web", "https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web", "https://support.apple.com/en-us/102445"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XProtect and macOS anti-malware

Apple describes three layers: prevent launch of malware, block malware on customer systems, and remediate malware that ran. Gatekeeper with notarisation covers the first two; XProtect spans the second and third.

## Layers
| Layer | What Apple documents |
|---|---|
| Gatekeeper | Verifies software from outside the App Store is from an identified developer, notarised and unaltered; asks approval before downloaded software first opens. Checks notarisation tickets including revocation tickets |
| Notarisation | Apple scans submitted apps for known malware and issues a ticket if none is found; developers usually staple it so Gatekeeper can verify offline. Apple can revoke tickets, even for previously notarised apps; macOS checks revocations in the background, more often than XProtect signature updates |
| XProtect | Built-in signature-based antivirus using YARA rules, updated automatically and separately from macOS updates. On macOS 10.15+ it checks at first launch, when an app changes on disk, and when signatures update; blocks, moves to Trash and alerts the user. Rules are more generic than hashes so can catch variants |
| XProtect behavioural engine | Looks for unknown malware; its data improves signatures |
| XProtect remediation | Removes malware based on Apple updates and periodically rechecks for infection; it does not restart the Mac automatically |

## Updates
- XProtect updates are delivered automatically; macOS checks daily by default. Notarisation updates arrive via CloudKit sync and are more frequent.
- On new malware Apple may revoke Developer ID certificates, issue revocation tickets and release XProtect signatures, applied retroactively to previously notarised software.

## Gatekeeper policy and overrides
- Default: software must be signed by the App Store or a registered developer and notarised. Settings under Privacy & Security allow "App Store" or "App Store and identified developers"; these may be unavailable on managed Macs.
- A user can override once: try to open the app, then System Settings > Privacy & Security > Open Anyway > Open. The app is saved as an exception.
- Users and organisations can restrict to the App Store, allow any software (unless device management restricts it), or turn Gatekeeper off; Apple warns unsigned, unnotarised software exposes the Mac to malware.

## Visibility
- On macOS 15+, third-party developers (for example EDR vendors) receive Endpoint Security API events when a user bypasses Gatekeeper; they can be viewed with `eslogger`. The Endpoint Security API also exposes files XProtect detected and the matching signature.
- Apple's pages describe no central console for built-in protection; use an EDR if you need enterprise detection and response (this is an inference, not an Apple statement).

## Gotchas
- Notarisation targets known files or hashes, and signatures cover known malware and variants; Apple does not claim they stop targeted attacks.
- Not in the sources, so verify yourself before relying on them: exact CLI commands to read XProtect version, MDM keys that enforce Gatekeeper or security updates, and which install paths skip quarantine checks.

## Verify
- [ ] Managed Macs are set to App Store and identified developers (per Apple's Privacy & Security setting) and the override policy matches your intent.
- [ ] Automatic security-content updates are not disabled on the fleet.

## Checked
Method: 2026-11-08 read the three Apple pages; removed the CLI commands, plist path, MDM payload keys, ES event constant, unified-log predicate, named malware families and quarantine-bypass claims as unsupported, and the macOS 15 Control-click claim as absent from the pages. Layer, update and override descriptions now follow the pages.
