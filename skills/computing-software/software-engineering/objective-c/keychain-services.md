---
id: computing-software.software-engineering.objective-c.keychain-services
name: keychain-services
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-security, keychain-services]
level: practitioner
status: draft
description: "Store secrets in the Keychain with SecItemAdd, SecItemCopyMatching, SecItemUpdate and accessibility attributes, checking OSStatus."
sources:
  - https://developer.apple.com/documentation/security
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keychain Services
**Goal:** persist credentials securely.

```objc
NSDictionary *base = @{ (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
                        (__bridge id)kSecAttrService: @"com.example.app",
                        (__bridge id)kSecAttrAccount: @"user" };
NSMutableDictionary *add = [base mutableCopy];
add[(__bridge id)kSecValueData] = [token dataUsingEncoding:NSUTF8StringEncoding];
add[(__bridge id)kSecAttrAccessible] = (__bridge id)kSecAttrAccessibleWhenUnlockedThisDeviceOnly;
OSStatus st = SecItemAdd((__bridge CFDictionaryRef)add, NULL);
if (st == errSecDuplicateItem) {
    st = SecItemUpdate((__bridge CFDictionaryRef)base, (__bridge CFDictionaryRef)@{ (__bridge id)kSecValueData: add[(__bridge id)kSecValueData] });
}
NSMutableDictionary *q = [base mutableCopy];
q[(__bridge id)kSecReturnData] = @YES; q[(__bridge id)kSecMatchLimit] = (__bridge id)kSecMatchLimitOne;
CFTypeRef out = NULL; st = SecItemCopyMatching((__bridge CFDictionaryRef)q, &out);
NSData *data = CFBridgingRelease(out);
```
- Check every `OSStatus`: `errSecSuccess`, `errSecItemNotFound`, `errSecDuplicateItem`.
- Accessibility: pick `...WhenUnlocked`, `...AfterFirstUnlock` (background access), and `...ThisDeviceOnly` variants to prevent backup/migration.
- Access groups (`kSecAttrAccessGroup`) share items among your apps.
- Never store secrets in NSUserDefaults, plists or source code.
- Biometric protection through `SecAccessControlCreateWithFlags`.

## Gotchas
- Keychain items persist across app reinstalls on iOS (older behaviour); clear on first launch if needed.
- The macOS keychain APIs and flags differ from iOS (data protection keychain needs `kSecUseDataProtectionKeychain`).

## Self-check
Add, read, update and delete an item in a unit test and assert each OSStatus.
