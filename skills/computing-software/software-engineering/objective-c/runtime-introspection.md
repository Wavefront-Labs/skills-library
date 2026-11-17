---
id: computing-software.software-engineering.objective-c.runtime-introspection
name: runtime-introspection
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runtime, runtime-introspection]
level: advanced
status: docs-checked
description: "Inspect classes, methods, ivars, properties and protocols at runtime with objc/runtime.h and free the returned arrays."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Introduction/Introduction.html
  - https://raw.githubusercontent.com/apple-oss-distributions/objc4/main/runtime/runtime.h
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOImplementation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime introspection
**Goal:** enumerate a class's structure with the C runtime API.

```objc
#import <objc/runtime.h>
unsigned int n = 0;
Method *methods = class_copyMethodList([NSString class], &n);
for (unsigned i = 0; i < n; i++) NSLog(@"%s", sel_getName(method_getName(methods[i])));
free(methods);                      // the returned array must be freed with free()

Class cls = object_getClass(obj);
const char *name = class_getName(cls);
Class sup = class_getSuperclass(cls);
objc_property_t *props = class_copyPropertyList(cls, &n); free(props);
Ivar *ivars = class_copyIvarList(cls, &n); free(ivars);
Protocol * __unsafe_unretained *protos = class_copyProtocolList(cls, &n); free(protos);
```
- The `class_copy*List` functions return a NULL-terminated array of `*outCount` entries that you must free with `free()`.
- `class_copyMethodList` does not search superclasses (unlike `class_getInstanceMethod`); walk `class_getSuperclass` to cover them.
- Class methods: `class_copyMethodList(object_getClass(cls), &count)`, because class methods live on the metaclass.
- Queries without iteration: `class_respondsToSelector`, `class_getInstanceMethod`, `class_conformsToProtocol`, `class_getInstanceVariable`; `object_getIvar` reads an ivar of an object.
- Creating a class at runtime: `objc_allocateClassPair`, add methods and ivars with `class_addMethod` and `class_addIvar`, then `objc_registerClassPair`.

## Gotchas
- With key-value observing the observed object's isa pointer is changed to an intermediate class, so `object_getClass` (which returns the isa class) may not be the true class; Apple says to use the `class` method to find the class of an instance.
- The runtime API is C: you manage the memory of the returned arrays yourself.

## Self-check
List the methods of a small class with `class_copyMethodList` and compare them with its declared and implemented methods.

## Checked
2026-11-08. Confirmed against the objc4 `runtime.h` header (function names, the free() requirement for class_copy* arrays, superclass note for class_copyMethodList, metaclass note, class creation sequence, class_copyProtocolList signature) and the Apple archive KVO Implementation Details page (isa-swizzling, use `class`). Read the Objective-C Runtime Programming Guide introduction only (its chapter list; the chapters themselves were not read). Removed the `NSKVONotifying_Foo` class name, the claim that `[obj class]` misreports KVO-observed objects (Apple's page says the opposite) and the ARC bridging remark.
Method: documentation only; no commands were run.
