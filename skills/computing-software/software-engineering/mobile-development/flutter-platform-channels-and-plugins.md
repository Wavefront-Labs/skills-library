---
id: computing-software.software-engineering.mobile-development.flutter-platform-channels-and-plugins
name: flutter-platform-channels-and-plugins
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, flutter, platform-channels, flutter-plugins, methodchannel, pigeon, ffigen, federated-plugins, dart]
level: advanced
status: docs-checked
description: "Call native Android/iOS code from Flutter: MethodChannel, type-safe Pigeon, FFI with ffigen, threading rules, background task queues, and writing federated plugins."
sources: ["https://docs.flutter.dev/platform-integration/platform-channels", "https://pub.dev/packages/pigeon", "https://docs.flutter.dev/packages-and-plugins/developing-packages", "https://dart.dev/interop/c-interop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flutter platform channels and plugins

**Goal:** reach platform APIs Flutter does not wrap (sensors, SDKs, OS services) with type-safe,
well-threaded bridges, packaged as reusable plugins.

## First check pub.dev
Many integrations already exist as maintained plugins (camera, maps, payments). Write your own only when needed.

## MethodChannel (request/response)
Dart:
```dart
const _channel = MethodChannel('com.example.app/battery');
Future<int> batteryLevel() async {
  try {
    return await _channel.invokeMethod<int>('getBatteryLevel') ?? -1;
  } on PlatformException catch (e) {
    throw BatteryException(e.message);
  }
}
```
Android (Kotlin, in MainActivity or a plugin):
```kotlin
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example.app/battery")
    .setMethodCallHandler { call, result ->
        when (call.method) {
            "getBatteryLevel" -> result.success(readBattery())
            else -> result.notImplemented()
        }
    }
```
iOS (Swift): `FlutterMethodChannel(name:binaryMessenger:)` with `setMethodCallHandler`.
- Values use the StandardMessageCodec (null, bool, num, String, Uint8List, List, Map); custom
  classes must be encoded manually - error-prone, hence Pigeon.
- Unhandled methods return `result.notImplemented()`.

## Pigeon: generated, type-safe channels (recommended)
```dart
// pigeons/messages.dart
@ConfigurePigeon(PigeonOptions(dartOut: 'lib/src/messages.g.dart',
    kotlinOut: 'android/app/src/main/kotlin/com/example/Messages.g.kt', swiftOut: 'ios/Runner/Messages.g.swift'))
class Book { String? title; int? pages; }
@HostApi()
abstract class BookApi {
  @async Book fetch(String id);
  List<Book> search(String query);
}
@FlutterApi()
abstract class BookEvents { void onBookAdded(Book b); }
```
Pigeon generates Dart, Kotlin (and Java) and Swift (and Objective-C) code; implement the
generated host interface natively (see the pigeon package page for the exact command and annotations). Compile-time types on both sides, no stringly method names.

## Threading rules
- Channel methods must be invoked on the platform's main thread (the UI thread on Android); long work
  there causes jank. To do work elsewhere, use a background task queue
  (`BinaryMessenger.makeBackgroundTaskQueue()`) for the channel, or jump back to the UI thread before
  calling a channel (post a Runnable to the UI Looper on Android, the main dispatch queue on iOS).
- Channels can be used from a background Isolate only if it is registered with
  `BackgroundIsolateBinaryMessenger.ensureInitialized(rootIsolateToken)`.

## FFI for C/C++ and direct native calls
- `dart:ffi` + **ffigen** generates bindings from C headers: synchronous, no message encoding -
  best for compute libraries (SQLite, image codecs, Rust via a C ABI).
- Dart also documents Java/Kotlin and Objective-C/Swift interop (jnigen, ffigen) as direct bindings
  without channels. Dart build hooks (formerly native assets) bundle compiled native code.

## Writing a plugin
```bash
flutter create --template=plugin --platforms=android,ios my_plugin
```
- **Federated plugins** split the API into a platform interface, independent per-platform
  implementations, and an app-facing interface that uses the implementation registered for the running platform.

## Verify
- [ ] No heavy work on the platform main thread in handlers (profile for jank).
- [ ] Channel contracts generated with Pigeon (or documented and tested).
- [ ] Plugin tested on Android and iOS devices.

## Checked
2026-11-01. Confirmed against the Flutter platform-channels page (main-thread rule, makeBackgroundTaskQueue, background Isolate registration, notImplemented), the developing-packages page (plugin template, federated plugins), the pigeon package page (generated languages, @async) and the Dart C interop page (ffigen, build hooks). Removed: EventChannel section, Pigeon CLI command, PlatformInterface verifyToken and default_package details, ActivityAware and lifecycle callbacks, Swift Package Manager note, Flutter Favorite advice.
Method: documentation only; no commands were run.
