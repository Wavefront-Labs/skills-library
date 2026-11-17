---
id: computing-software.software-engineering.objective-c.core-data-stack
name: core-data-stack
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-persistence, core-data-stack]
level: advanced
status: draft
description: "Set up NSPersistentContainer, use viewContext on main and performBackgroundTask for background work with correct merge policies."
sources:
  - https://developer.apple.com/documentation/coredata
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Core Data stack
**Goal:** a thread-correct persistence layer.

```objc
NSPersistentContainer *c = [[NSPersistentContainer alloc] initWithName:@"Model"];
[c loadPersistentStoresWithCompletionHandler:^(NSPersistentStoreDescription *d, NSError *e) {
    if (e) { NSLog(@"store failed: %@", e); }
}];
c.viewContext.automaticallyMergesChangesFromParent = YES;
c.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy;

[c performBackgroundTask:^(NSManagedObjectContext *ctx) {
    Person *p = [NSEntityDescription insertNewObjectForEntityForName:@"Person" inManagedObjectContext:ctx];
    p.name = @"Ada";
    NSError *err = nil;
    if (![ctx save:&err]) { NSLog(@"%@", err); }
}];
```
- A managed object context is bound to its queue: use `[ctx performBlock:]` / `performBlockAndWait:` for every access, and never pass `NSManagedObject` instances across contexts; pass `objectID` and re-fetch with `objectWithID:`.
- `viewContext` is main-queue; use it for UI (e.g. `NSFetchedResultsController`).
- Handle the store-load error properly in production (migration failures).
- Lightweight migration is automatic with `shouldMigrateStoreAutomatically` and `shouldInferMappingModelAutomatically` (both default YES on NSPersistentContainer descriptions).
- Batch operations: `NSBatchDeleteRequest`, `NSBatchInsertRequest` bypass contexts; merge changes manually.

## Gotchas
- Accessing a managed object from the wrong queue crashes intermittently; enable `-com.apple.CoreData.ConcurrencyDebug 1` launch argument.
- Saving a context with unresolved validation errors fails; read `NSDetailedErrorsKey`.

## Self-check
Run with the concurrency debug launch argument and exercise background saves.
