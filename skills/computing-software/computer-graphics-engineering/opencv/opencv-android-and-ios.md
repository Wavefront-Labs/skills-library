---
id: computing-software.computer-graphics-engineering.opencv.opencv-android-and-ios
name: opencv-android-and-ios
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, opencv-android, opencv-ios, mobile, jni, xcframework]
level: practitioner
status: docs-checked
description: "Integrate OpenCV in Android and iOS apps: Maven Central or SDK module, OpenCVLoader.initLocal, building the iOS framework from source, and mobile build gotchas."
sources: ["https://docs.opencv.org/4.x/d5/df8/tutorial_dev_with_OCV_on_Android.html", "https://docs.opencv.org/4.x/d5/da3/tutorial_ios_install.html", "https://central.sonatype.com/artifact/org.opencv/opencv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV on Android and iOS

## Android
- Since OpenCV 4.9.0 the Android package is on Maven Central and installs as a Gradle dependency:
  `implementation 'org.opencv:opencv:<version>'` with `<version>` any official release (see the Maven Central page).
  The tutorial states the minimum SDK for 4.9.0 is 21; for newer releases check the release notes.
- Alternative: download the OpenCV Android SDK and import its module in Android Studio (File, New, Import module).
  The app's minimum SDK must not be lower than the one used to build the SDK (see `sdk/build.gradle`,
  `defaultConfig`). For the SDK module the tutorial also says to enable `buildConfig` in the module's `build.gradle`
  and, for Kotlin, to add the Kotlin Android plugin.
- Load the library before any OpenCV call, at app start:
  `if (OpenCVLoader.initLocal()) { ... } else { Log.e(TAG, "OpenCV initialization failed!"); }`.
  If the app has other OpenCV-dependent native libraries, load them after OpenCV initialisation.

## iOS
- The iOS installation tutorial says it "can contain obsolete information". It builds from source with
  CMake and Xcode command line tools: `python opencv/platforms/ios/build_framework.py ios`.
- Extra modules (for example aruco) are not in the iOS pack download from the OpenCV releases; build yourself with
  `--contrib opencv_contrib`. Use `--without <module_name>` to exclude a module.
- Check the current OpenCV iOS documentation and release assets for a prebuilt framework before building.

## Gotchas
- Mobile builds often omit contrib modules; check which modules are present.
- Process at reduced resolution off the UI thread.

## Verify
Check the OpenCV modules you need are present at startup and benchmark a filter on the device.

## Checked
2026-11-01. Confirmed in the OpenCV "Android Development with OpenCV" tutorial (Maven Central since 4.9.0, minimum
SDK 21 for 4.9.0, SDK import steps, initLocal), the "Installation in iOS" tutorial (build_framework.py, --contrib,
--without, obsolete warning) and the Maven Central artifact page (org.opencv:opencv exists).
Removed unconfirmed: CameraX YUV conversion, CMake find_package/NDK linking, ABI size figures, xcframework script and
CocoaPods, Objective-C++ bridging and header-order advice, CVPixelBuffer wrapping, and the getBuildInformation startup log.
Method: documentation only; no commands were run.
