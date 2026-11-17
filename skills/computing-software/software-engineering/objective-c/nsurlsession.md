---
id: computing-software.software-engineering.objective-c.nsurlsession
name: nsurlsession
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-io, nsurlsession]
level: practitioner
status: draft
description: "Issue HTTP requests with NSURLSession data, download and upload tasks, configure timeouts and cache, and handle responses and errors."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSURLSession
**Goal:** reliable HTTP calls with proper result handling.

```objc
NSURLSessionConfiguration *cfg = [NSURLSessionConfiguration defaultSessionConfiguration];
cfg.timeoutIntervalForRequest = 30;
NSURLSession *session = [NSURLSession sessionWithConfiguration:cfg];
NSMutableURLRequest *req = [NSMutableURLRequest requestWithURL:url];
req.HTTPMethod = @"POST";
[req setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
req.HTTPBody = body;
NSURLSessionDataTask *task = [session dataTaskWithRequest:req completionHandler:^(NSData *data, NSURLResponse *resp, NSError *error) {
    if (error) { return; }
    NSInteger code = [(NSHTTPURLResponse *)resp statusCode];
    if (code < 200 || code >= 300) { return; }
    dispatch_async(dispatch_get_main_queue(), ^{ /* update UI */ });
}];
[task resume];                    // tasks start suspended
```
- Completion handlers run on the session's delegate queue (a background serial queue by default), not on the main thread.
- HTTP error statuses are not `NSError`s; check the status code.
- Use `downloadTaskWithURL:` for large files, background configurations (`backgroundSessionConfigurationWithIdentifier:`) for transfers surviving app suspension.
- Cancel with `[task cancel]`; invalidate sessions (`finishTasksAndInvalidate`) because sessions retain their delegate.
- Certificate pinning goes in the delegate `URLSession:didReceiveChallenge:completionHandler:`.

## Gotchas
- Creating a session per request is wasteful; share one.
- A session with a delegate retains it until invalidated.

## Self-check
Request a 404 URL and confirm your code treats it as failure.
