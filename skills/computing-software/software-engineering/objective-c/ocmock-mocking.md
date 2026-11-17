---
id: computing-software.software-engineering.objective-c.ocmock-mocking
name: ocmock-mocking
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-testing, ocmock-mocking]
level: advanced
status: draft
description: "Create mocks, stubs and verifications with OCMock, and prefer protocol-based fakes where possible."
sources:
  - https://developer.apple.com/documentation/xctest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mocking
**Goal:** isolate the unit under test.

```objc
#import <OCMock/OCMock.h>
id session = OCMProtocolMock(@protocol(ABCSession));
OCMStub([session fetchURL:[OCMArg any] completion:[OCMArg any]]).andDo(^(NSInvocation *inv) {
    void (^cb)(NSData *, NSError *); [inv getArgument:&cb atIndex:3]; cb(data, nil);
});
ABCClient *c = [[ABCClient alloc] initWithSession:session];
[c refresh];
OCMVerify([session fetchURL:url completion:[OCMArg any]]);

id partial = OCMPartialMock(realObject);
OCMStub([partial currentDate]).andReturn(fixedDate);
```
- OCMock (third-party; install through SwiftPM or CocoaPods) offers `OCMClassMock`, `OCMProtocolMock`, `OCMPartialMock`, `OCMStub`, `OCMVerify`, `OCMReject`, `OCMArg`.
- OCMock relies on the runtime (isa-swizzling/forwarding); it cannot mock direct methods (`objc_direct`) or final C functions.
- Hand-written fakes conforming to a protocol are simpler and more robust: inject them through initializers.
- Stub class methods and singletons with `OCMStub([classMock sharedInstance])`; stop mocking with `[mock stopMocking]` in tearDown.
- Argument indices in invocations start at 2 (0 is self, 1 is _cmd).

## Gotchas
- Forgetting `stopMocking` on class mocks leaks the swizzle into other tests.
- Strict mocks fail on unexpected calls; use `OCMStrictClassMock` deliberately.

## Self-check
Run the whole suite in random order (Xcode test plan option) to detect leaked mocks.
