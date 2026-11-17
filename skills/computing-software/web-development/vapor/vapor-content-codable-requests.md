---
id: computing-software.web-development.vapor.vapor-content-codable-requests
name: vapor-content-codable-requests
category: computing-software
field: web-development
product: vapor
tags: [vapor, content, codable, req-content, query, json, url-encoded, multipart]
level: practitioner
status: docs-checked
description: "Decode Vapor request bodies and query strings into Content structs, with supported media types, 415 behaviour, file uploads and single query values."
sources:
  - https://docs.vapor.codes/basics/content/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn HTTP bodies and query strings into Codable structs.

```swift
struct Greeting: Content { var hello: String }
app.post("greeting") { req in
    let greeting = try req.content.decode(Greeting.self)
    return HTTPStatus.ok
}
```
`Content` adds `Codable` plus helpers. `decode` picks a decoder from the request's content-type; if none is found or the header is absent, a `415` is thrown. So the same route accepts JSON and `application/x-www-form-urlencoded` (`hello=world`). JSON is the default encoding.

Supported by default: JSON `application/json` (`.json`), Multipart `multipart/form-data` (`.formData`), URL-encoded form `application/x-www-form-urlencoded` (`.urlEncodedForm`), Plaintext `text/plain` (`.plainText`), HTML `text/html` (`.html`). Not every media type supports every Codable feature (JSON: no top-level fragments; plaintext: no nested data).

File uploads: declare the property as `Data`.
```swift
struct Profile: Content { var name: String; var email: String; var image: Data }
```

## Query strings
Make query fields optional; to require a value use a route parameter instead.
```swift
struct Hello: Content { var name: String? }
app.get("hello") { req -> String in
    let hello = try req.query.decode(Hello.self)
    return "Hello, \(hello.name ?? "Anonymous")"
}
```
`GET /hello?name=Vapor` gives `Hello, Vapor`; with no query string it gives `Hello, Anonymous`. Single value: `let name: String? = req.query["name"]`.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/content, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
