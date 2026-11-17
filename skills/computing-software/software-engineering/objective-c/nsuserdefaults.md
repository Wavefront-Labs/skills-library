---
id: computing-software.software-engineering.objective-c.nsuserdefaults
name: nsuserdefaults
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-data, nsuserdefaults]
level: intro
status: draft
description: "Store small user preferences with NSUserDefaults, register defaults, observe changes and avoid storing secrets."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSUserDefaults
**Goal:** persist small preference values.

```objc
NSUserDefaults *ud = [NSUserDefaults standardUserDefaults];
[ud registerDefaults:@{ @"theme": @"light", @"launchCount": @0 }];
[ud setInteger:[ud integerForKey:@"launchCount"] + 1 forKey:@"launchCount"];
[ud setObject:@"dark" forKey:@"theme"];
NSString *t = [ud stringForKey:@"theme"];
[ud removeObjectForKey:@"theme"];
NSUserDefaults *group = [[NSUserDefaults alloc] initWithSuiteName:@"group.com.example.shared"];
```
- Property list types only: NSString, NSNumber, NSDate, NSData, NSArray, NSDictionary.
- `registerDefaults:` values are not persisted and are used when the key is unset; call it every launch.
- Writes are synchronised automatically; calling `synchronize` is generally unnecessary on current systems.
- App groups share defaults between app and extensions via `initWithSuiteName:`.
- Not for secrets: use Keychain. Not for large blobs: use files.
- Observable via KVO on keys or `NSUserDefaultsDidChangeNotification`.

## Gotchas
- `integerForKey:` returns 0 for missing; use `objectForKey:` nil test to distinguish.
- Defaults are unencrypted and included in backups.

## Self-check
Remove a key and confirm `registerDefaults` supplies the fallback.
