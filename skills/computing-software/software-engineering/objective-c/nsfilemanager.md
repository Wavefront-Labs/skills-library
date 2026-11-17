---
id: computing-software.software-engineering.objective-c.nsfilemanager
name: nsfilemanager
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-io, nsfilemanager]
level: practitioner
status: draft
description: "Read, write, copy, move and enumerate files with NSFileManager using URLs, application directories and error out-parameters."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSFileManager
**Goal:** file operations with proper locations and errors.

```objc
NSFileManager *fm = [NSFileManager defaultManager];
NSURL *docs = [fm URLsForDirectory:NSDocumentDirectory inDomains:NSUserDomainMask].firstObject;
NSURL *file = [docs URLByAppendingPathComponent:@"data.json"];
NSError *err = nil;
if (![fm createDirectoryAtURL:docs withIntermediateDirectories:YES attributes:nil error:&err]) { ... }
if (![data writeToURL:file options:NSDataWritingAtomic error:&err]) { ... }
if ([fm fileExistsAtPath:file.path]) { [fm removeItemAtURL:file error:&err]; }
for (NSURL *u in [fm contentsOfDirectoryAtURL:docs includingPropertiesForKeys:nil options:0 error:&err]) { ... }
```
- Use URL-based APIs; path-string APIs remain but URLs carry security-scope and resource keys.
- Standard locations: Documents (user data), Library/Caches (purgeable), Application Support (app data), temporary directory (`NSTemporaryDirectory()`).
- Atomic writes (`NSDataWritingAtomic`) avoid partial files.
- Exclude from backup with the `NSURLIsExcludedFromBackupKey` resource value.
- Do slow file work off the main thread; use `NSFileCoordinator` for shared (iCloud, extension) files.

## Gotchas
- Checking existence then acting is racy; act and handle the error.
- Container paths change between installs; store relative paths, not absolute.

## Self-check
Write, read back and delete a file in a test using the temporary directory.
