---
id: computing-software.software-engineering.mobile-development.android-manifest-merging
name: android-manifest-merging
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, manifest-merging, androidmanifest, tools-node, tools-remove, merge-conflicts, permissions]
level: practitioner
status: docs-checked
description: "Resolve Android manifest merge conflicts: merge priority, tools:replace/remove/node markers, reading the merged manifest and removing unwanted library permissions."
sources: ["https://developer.android.com/build/manage-manifests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android manifest merging

Gradle merges all manifests into the single one packaged in the APK or bundle, lowest priority into highest. Priority, highest first: build-variant manifests (variant, then build type, then product flavor; flavor dimensions in `flavorDimensions` order, first highest), the main manifest of the app module, then library manifests (in the order of the Gradle dependencies block). If the same attribute has different values in two matching elements, the merge reports a conflict error until you add a marker in the higher-priority manifest. Values set in `build.gradle` (such as `minSdk`) override the manifest, so leave `<uses-sdk>` out.

## Resolve with `tools:` markers
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
          xmlns:tools="http://schemas.android.com/tools">

    <!-- drop a permission a library added -->
    <uses-permission android:name="android.permission.READ_PHONE_STATE" tools:node="remove" />

    <application
        android:allowBackup="false"
        tools:replace="android:allowBackup,android:label">
        <!-- turn off an exported component from a library -->
        <activity android:name="com.lib.DebugActivity" tools:node="remove" />
    </application>
</manifest>
```
Markers go in the higher-priority manifest, which must declare the `tools` namespace. Element markers: `tools:node="merge"` (default), `mergeOnlyAttributes`, `remove`, `removeAll` (all elements of that type in the same parent), `replace`, `strict`. Attribute markers: `tools:remove="attr, ..."`, `tools:replace="attr, ..."`, `tools:strict="attr, ..."` (the default behaviour). `tools:selector="com.example.lib1"` limits a marker to one library's manifest.

## See what happened
- Android Studio: open `AndroidManifest.xml` and click the Merged Manifest tab. It shows the merged result, which file each element came from (Merging Log) and conflicts with suggested markers (Merging Errors).
- Full decision log: `build/outputs/logs/manifest-merger-<buildVariant>-report.txt` in the module.

## Gotchas
- `<intent-filter>` elements are never matched between manifests; each is added as unique.
- `android:required` on `<uses-feature>` and `<uses-library>` merges with OR: "true" wins.
- Do not depend on default attribute values: a lower-priority manifest that sets an attribute you left unset overrides the default, so declare attributes explicitly.
- In app modules the tools markers are removed after the merge; in library modules they are not, and can affect downstream merges.
- Build variables: `manifestPlaceholders` (for example `manifestPlaceholders["hostName"] = "www.example.com"` in `defaultConfig`, used as `${hostName}`) and `${applicationId}`, which always matches the final application ID of the variant.
- A library `minSdk` higher than the app's fails the merge. `tools:overrideLibrary="com.example.lib1"` on `<uses-sdk>` in the main manifest imports it anyway; only use it after verifying the library is safe on the lower API levels.
- A library with a lower `targetSdkVersion` can make the merger add system permissions for you (for example `WRITE_EXTERNAL_STORAGE` and `READ_PHONE_STATE` when the library targets 3 or lower), so check the merged result.

Verify: open the Merged Manifest view (or the merger report) for the release variant and compare the `uses-permission` entries and components against what you intend to ship.

## Checked
Date: 2026-11-08. Confirmed against the Android Developers "Manage manifest files" page: merge priorities, conflict heuristics, all node and attribute markers, selector, overrideLibrary, implicit permissions, Merged Manifest view, report file path, placeholders and applicationId. Removed the unsupported intermediates path, the "Manifest merger failed" message text, the Android 12 exported rule and the Play data-safety and queries claims.
Method: documentation only; no commands were run.
