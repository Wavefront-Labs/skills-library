---
id: computing-software.software-engineering.objective-c.xctest-basics
name: xctest-basics
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-testing, xctest-basics]
level: intro
status: draft
description: "Write XCTestCase classes in Objective-C with setUp/tearDown, XCTAssert macros, exception assertions and performance measurement."
sources:
  - https://developer.apple.com/documentation/xctest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# XCTest basics
**Goal:** unit tests that run in Xcode and xcodebuild.

```objc
#import <XCTest/XCTest.h>
#import "ABCCart.h"
@interface ABCCartTests : XCTestCase
@property (nonatomic, strong) ABCCart *cart;
@end
@implementation ABCCartTests
- (void)setUp { [super setUp]; self.cart = [ABCCart new]; }
- (void)tearDown { self.cart = nil; [super tearDown]; }
- (void)testAddingItemIncreasesCount {
    [self.cart addItem:@"apple"];
    XCTAssertEqual(self.cart.count, 1u);
    XCTAssertEqualObjects(self.cart.items.firstObject, @"apple");
    XCTAssertNil([self.cart itemNamed:@"pear"]);
}
- (void)testRejectsNil {
    XCTAssertThrowsSpecificNamed([self.cart addItem:nil], NSException, NSInvalidArgumentException);
}
- (void)testSpeed { [self measureBlock:^{ [self.cart recalculate]; }]; }
@end
```
- Methods named `test...` returning void are discovered automatically.
- Common macros: `XCTAssertTrue/False`, `XCTAssertEqual`, `XCTAssertEqualObjects`, `XCTAssertEqualWithAccuracy`, `XCTAssertNil/NotNil`, `XCTAssertThrows`, `XCTAssertNoThrow`, `XCTFail`.
- Run: `xcodebuild test -scheme App -destination '...'`; filter with `-only-testing:AppTests/ABCCartTests/testAddingItemIncreasesCount`.
- Use `XCTSkip`-style skipping via `XCTSkipIf`/`XCTSkipUnless` (macros available in modern Xcode; they require `throws` in Swift but work with `XCTSkipIf` macro in Objective-C; verify in your SDK).

## Gotchas
- `XCTAssertEqual` is for C scalars; use `XCTAssertEqualObjects` for objects.
- Tests share process state; reset singletons in `setUp`.

## Self-check
Run the suite; break an assertion deliberately and confirm it fails with a message.
