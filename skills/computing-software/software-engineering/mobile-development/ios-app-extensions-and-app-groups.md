---
id: computing-software.software-engineering.mobile-development.ios-app-extensions-and-app-groups
name: ios-app-extensions-and-app-groups
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, app-extensions, app-groups, share-extension, notification-service-extension, shared-container, entitlements]
level: practitioner
status: draft
description: "Add iOS app extensions (share, notification service, widgets) and share data with the host app via App Groups, with the memory, lifecycle and signing gotchas."
sources: ["https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/", "https://developer.apple.com/documentation/xcode/configuring-app-groups", "https://developer.apple.com/documentation/usernotifications/modifying-content-in-newly-delivered-notifications"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iOS app extensions and App Groups

An extension is a separate process with its own bundle id, entitlements and provisioning profile, embedded in the host app.

## Add one
Xcode > File > New > Target > pick the extension type (Share, Notification Service, Widget, Action, Intents...). Its bundle id must be prefixed with the app's (`com.example.app.share`). Each needs a provisioning profile; automatic signing creates them.

## Share data with App Groups
1. Enable the App Groups capability on the app and every extension target, using the same group id such as `group.com.example.app`.
2. Read and write through the shared container:
```swift
let defaults = UserDefaults(suiteName: "group.com.example.app")
defaults?.set(token, forKey: "lastSync")
let dir = FileManager.default
    .containerURL(forSecurityApplicationGroupIdentifier: "group.com.example.app")
```
Use the shared Keychain access group for secrets rather than group UserDefaults.

## Example: notification service extension
```swift
override func didReceive(_ request: UNNotificationRequest,
                         withContentHandler handler: @escaping (UNNotificationContent) -> Void) {
    let content = request.content.mutableCopy() as! UNMutableNotificationContent
    // download image, decrypt body, then
    handler(content)
}
```
The push payload must include `"mutable-content": 1`.

## Gotchas
- Strict memory ceilings (tens of MB for many types; Apple does not publish exact numbers) and short runtime; the system kills overruns. Notification service extensions get roughly 30 seconds, then `serviceExtensionTimeWillExpire` is called.
- Extensions cannot use `UIApplication.shared`; mark shared frameworks with "App Extension API Only".
- Not every capability is allowed in all extensions.

Verify: run the extension scheme in Xcode, attach to the extension process, trigger it from the system UI, and confirm the app reads data the extension wrote to the group container.
