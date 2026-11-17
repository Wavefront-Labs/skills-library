---
id: computing-software.web-development.vapor.vapor-content-custom-coders-hooks
name: vapor-content-custom-coders-hooks
category: computing-software
field: web-development
product: vapor
tags: [vapor, content, contentconfiguration, afterdecode, beforeencode, responseencodable, custom-coders]
level: advanced
status: docs-checked
description: "Customize Vapor Content: afterDecode/beforeEncode hooks, ContentConfiguration global and one-off coders, custom coders, and ResponseEncodable types."
sources:
  - https://docs.vapor.codes/basics/content/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: hook into, reconfigure or extend Vapor's Content encoding.

## Hooks
Vapor calls `afterDecode` after decoding and `beforeEncode` before encoding a `Content` type (defaults do nothing). `mutating` is needed only for structs.
```swift
mutating func afterDecode() throws {
    self.name = self.name?.trimmingCharacters(in: .whitespacesAndNewlines)
    if let name = self.name, name.isEmpty {
        throw Abort(.badRequest, reason: "Name must not be empty.")
    }
}
mutating func beforeEncode() throws {
    guard let name = self.name?.trimmingCharacters(in: .whitespacesAndNewlines),
          !name.isEmpty else {
        throw Abort(.badRequest, reason: "Name must not be empty.")
    }
    self.name = name
}
```
## Override defaults
Global (usually in configure.swift):
```swift
let encoder = JSONEncoder()
encoder.dateEncodingStrategy = .secondsSince1970
ContentConfiguration.global.use(encoder: encoder, for: .json)
```
One-off:
```swift
let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .secondsSince1970
let hello = try req.content.decode(Hello.self, using: decoder)
```
## Custom coders
Conform to `ContentEncoder` (`encode(_:to: inout ByteBuffer, headers: inout HTTPHeaders)`) / `ContentDecoder` (`decode(_:from: ByteBuffer, headers:)`) and register them with ContentConfiguration. For query strings conform to `URLQueryEncoder` (`encode(_:to: inout URI)`) / `URLQueryDecoder` (`decode(_:from: URI)`) and register with `use(urlEncoder:)` / `use(urlDecoder:)`.

## Custom ResponseEncodable
```swift
struct HTML { let value: String }
extension HTML: AsyncResponseEncodable {
  public func encodeResponse(for request: Request) async throws -> Response {
    var headers = HTTPHeaders()
    headers.add(name: .contentType, value: "text/html")
    return .init(status: .ok, headers: headers, body: .init(string: value))
  }
}
app.get { _ in HTML(value: "<html><body><h1>Hello, World!</h1></body></html>") }
```
Without async/await, implement `ResponseEncodable` returning `request.eventLoop.makeSucceededFuture(...)` of the same `Response`. This lets you control the `Content-Type` header.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/content, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
