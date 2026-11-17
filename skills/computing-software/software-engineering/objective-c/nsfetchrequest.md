---
id: computing-software.software-engineering.objective-c.nsfetchrequest
name: nsfetchrequest
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-persistence, nsfetchrequest]
level: practitioner
status: draft
description: "Fetch entities with NSFetchRequest, NSPredicate, sort descriptors, batch size and fetch limits, and count efficiently."
sources:
  - https://developer.apple.com/documentation/coredata
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSFetchRequest
**Goal:** efficient queries.

```objc
NSFetchRequest *req = [Person fetchRequest];
req.predicate = [NSPredicate predicateWithFormat:@"age >= %d AND name BEGINSWITH[cd] %@", 18, @"a"];
req.sortDescriptors = @[[NSSortDescriptor sortDescriptorWithKey:@"name" ascending:YES]];
req.fetchBatchSize = 50;
req.fetchLimit = 200;
NSError *err = nil;
NSArray<Person *> *rows = [ctx executeFetchRequest:req error:&err];
NSUInteger n = [ctx countForFetchRequest:req error:&err];
```
- Use `%@`/`%d` argument substitution in `predicateWithFormat:` rather than string concatenation (prevents injection and escaping bugs).
- String modifiers: `[c]` case-insensitive, `[d]` diacritic-insensitive; `CONTAINS`, `BEGINSWITH`, `IN`, `MATCHES`.
- `fetchBatchSize` makes results a lazily faulting array; `relationshipKeyPathsForPrefetching` reduces faults.
- Index frequently queried attributes in the model editor.
- Use `NSFetchedResultsController` for table-backed UI.
- `NSPredicate` is also useful on plain collections: `filteredArrayUsingPredicate:`.

## Gotchas
- Mismatched types in the predicate (string vs number) raise at runtime.
- A fetch returning faults still touches the store when properties are read.

## Self-check
Turn on SQL debug with launch argument `-com.apple.CoreData.SQLDebug 1` and inspect the generated SQL.
