---
id: computing-software.web-development.vapor.vapor-apns-push-notifications
name: vapor-apns-push-notifications
category: computing-software
field: web-development
product: vapor
tags: [vapor, apns, push-notifications, jwt, swift, ios, apnswift, vaporapns]
level: practitioner
status: docs-checked
description: "Send Apple push notifications from Vapor with the apns package: dependency, JWT or TLS config, APNSAlertNotification, custom payload."
sources:
  - https://docs.vapor.codes/advanced/apns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: authenticate to APNS and send an alert push from a Vapor app (built on APNSwift).

## Add the package
```swift
.package(url: "https://github.com/vapor/apns.git", from: "4.0.0"),
// target dependency:
.product(name: "VaporAPNS", package: "apns")
```
Run `swift package resolve` if not editing in Xcode.

## Configure
```swift
import APNS
import VaporAPNS
import APNSCore

let apnsConfig = APNSClientConfiguration(
    authenticationMethod: .jwt(
        privateKey: try .loadFrom(string: "<key.p8 content>"),
        keyIdentifier: "<key identifier>",
        teamIdentifier: "<team identifier>"
    ),
    environment: .development
)
app.apns.containers.use(
    apnsConfig,
    eventLoopGroupProvider: .shared(app.eventLoopGroup),
    responseDecoder: JSONDecoder(),
    requestEncoder: JSONEncoder(),
    as: .default
)
```
The `.p8` key comes from Apple's developer portal. For certificate (TLS) auth use:

```swift
authenticationMethod: .tls(
    privateKeyPath: <path to private key>,
    pemPath: <path to pem file>,
    pemPassword: <optional pem password>
)
```

## Send
```swift
struct Payload: Codable {
    let acme1: String
    let acme2: Int
}
let alert = APNSAlertNotification(
    alert: .init(title: .raw("Hello"), subtitle: .raw("This is a test from vapor/apns")),
    expiration: .immediately,
    priority: .immediately,
    topic: "<my topic>",
    payload: Payload(acme1: "hey", acme2: 2)
)
try await req.apns.client.sendAlertNotification(alert, deviceToken: "<device token>", deadline: .distantFuture)
```
Use `req.apns` inside route handlers (also available on `Application`). Alert property names map one-to-one to Apple's payload key reference. Any `Codable` can be the custom `payload`. For other methods see APNSwift's README.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) advanced/apns, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
