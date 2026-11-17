---
id: computing-software.software-engineering.objective-c.xctest-async
name: xctest-async
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-testing, xctest-async]
level: practitioner
status: draft
description: "Test callbacks and async code with XCTestExpectation, waitForExpectations, inverted expectations and predicate expectations."
sources:
  - https://developer.apple.com/documentation/xctest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Async tests
**Goal:** assert on completion handlers without sleeping.

```objc
- (void)testFetchCompletes {
    XCTestExpectation *done = [self expectationWithDescription:@"fetch"];
    [self.client fetchWithCompletion:^(NSData *data, NSError *error) {
        XCTAssertNil(error);
        XCTAssertGreaterThan(data.length, 0u);
        [done fulfill];
    }];
    [self waitForExpectationsWithTimeout:5 handler:nil];
}
- (void)testDoesNotCallBack {
    XCTestExpectation *never = [self expectationWithDescription:@"no call"];
    never.inverted = YES;
    [self.client onEvent:^{ [never fulfill]; }];
    [self waitForExpectations:@[never] timeout:0.5];
}
```
- Fulfill exactly once per expectation (over-fulfilling fails); use `expectedFulfillmentCount` for multiple calls.
- Assertions inside callbacks on other threads are supported by XCTest.
- `[self expectationForPredicate:... evaluatedWithObject:... handler:]` and `expectationForNotification:object:handler:` wrap common cases.
- Replace network with `NSURLProtocol` stubs or a protocol-injected fake session.
- Never `sleep` or spin the run loop manually.

## Gotchas
- A missing `fulfill` makes the test wait for the whole timeout, then fail.
- Weakly capturing the test case inside callbacks avoids retain issues only if needed (callbacks usually finish).

## Self-check
Set the timeout to 0.01 and confirm the test fails with a timeout message.
