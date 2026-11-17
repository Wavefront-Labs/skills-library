---
id: computing-software.software-engineering.objective-c.nscoding-archiving
name: nscoding-archiving
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-data, nscoding-archiving]
level: advanced
status: draft
description: "Archive objects with NSSecureCoding, NSKeyedArchiver and NSKeyedUnarchiver using requiresSecureCoding and allowed classes."
sources:
  - https://developer.apple.com/documentation/foundation
  - https://developer.apple.com/documentation/security
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSSecureCoding and archiving
**Goal:** persist object graphs without class-substitution attacks.

```objc
@interface ABCProfile : NSObject <NSSecureCoding>
@property (nonatomic, copy) NSString *name;
@end
@implementation ABCProfile
+ (BOOL)supportsSecureCoding { return YES; }
- (void)encodeWithCoder:(NSCoder *)c { [c encodeObject:self.name forKey:@"name"]; }
- (instancetype)initWithCoder:(NSCoder *)c {
    if ((self = [super init])) { _name = [c decodeObjectOfClass:[NSString class] forKey:@"name"]; }
    return self;
}
@end
NSError *e = nil;
NSData *d = [NSKeyedArchiver archivedDataWithRootObject:p requiringSecureCoding:YES error:&e];
ABCProfile *back = [NSKeyedUnarchiver unarchivedObjectOfClass:[ABCProfile class] fromData:d error:&e];
```
- Use `decodeObjectOfClass:forKey:` / `decodeObjectOfClasses:forKey:` (collections need the element classes in the set).
- `archivedDataWithRootObject:requiringSecureCoding:error:` and `unarchivedObjectOfClass:fromData:error:` are the modern API; older `archivedDataWithRootObject:` / `unarchiveObjectWithData:` are deprecated.
- Keys must be stable; add new keys with backward-compatible defaults; version via `decodeIntegerForKey:`.
- `NSCoding` classes must call `[super initWithCoder:]` if the superclass conforms.

## Gotchas
- Insecure unarchiving of untrusted data can instantiate arbitrary classes.
- Renaming a class breaks old archives unless `setClassName:forClass:` is used.

## Self-check
Round-trip an object and assert equality of every field.
