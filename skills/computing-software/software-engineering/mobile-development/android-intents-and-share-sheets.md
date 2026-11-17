---
id: computing-software.software-engineering.mobile-development.android-intents-and-share-sheets
name: android-intents-and-share-sheets
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, android-intents, share-sheet, uiactivityviewcontroller, sharelink, fileprovider, package-visibility, activity-result-api]
level: practitioner
status: docs-checked
description: "Use Android intents (explicit, implicit, activity results, package visibility) and share content via the sharesheet and FileProvider, with the iOS share APIs noted."
sources: ["https://developer.android.com/develop/ui/compose/sharing/send", "https://developer.android.com/training/basics/intents/result", "https://developer.android.com/training/package-visibility"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Intents and share sheets

**Goal:** hand off to other apps and receive content from them correctly on both platforms,
without crashes when no app can handle the request.

## Android intents
- **Explicit** (`Intent(context, DetailActivity::class.java)`) for your own components.
- **Implicit** (action + data/type) to let the system choose an app:
```kotlin
val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://example.com"))
try { startActivity(intent) } catch (e: ActivityNotFoundException) { showNoAppMessage() }
```
- **Package visibility** (targetSdk 30+): the system filters what your app can see of other installed apps, including `queryIntentActivities()` results. Declare what you need in `<queries>`; `QUERY_ALL_PACKAGES` is a last resort and subject to Google Play approval.
```xml
<queries>
  <intent><action android:name="android.intent.action.SENDTO" /><data android:scheme="mailto" /></intent>
</queries>
```
- Results: use the Activity Result API, not deprecated `startActivityForResult`:
```kotlin
val pickImage = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri -> uri?.let(::upload) }
pickImage.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
```
  Register the callback unconditionally every time the activity is created (field or `onCreate`), not only inside click handlers, because the process can be destroyed while the other activity runs. `startActivityForResult()` still exists, but Google strongly recommends the Activity Result APIs.
- Pass ids or URIs in extras, not bitmaps.
- `PendingIntent` (notifications, widgets, alarms): use `FLAG_IMMUTABLE` unless the receiver must fill in fields, and set the component on the inner intent.

## Sharing out (Android sharesheet)
```kotlin
val send = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, url)
    putExtra(Intent.EXTRA_TITLE, "Share article")
}
startActivity(Intent.createChooser(send, null))
```
Files go through a `FileProvider` content URI with a temporary read grant, never `file://`:
```kotlin
val uri = FileProvider.getUriForFile(ctx, "${ctx.packageName}.fileprovider", file)
val send = Intent(Intent.ACTION_SEND).apply {
    type = "image/png"; putExtra(Intent.EXTRA_STREAM, uri)
    clipData = ClipData.newRawUri(null, uri)        // shows the preview thumbnail
    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
}
```
Declare the provider with `android:exported="false"` and `grantUriPermissions="true"` and a
`file_paths.xml` scoped to a cache subdirectory.

## Receiving shares (Android)
```xml
<activity android:name=".ShareReceiverActivity" android:exported="true">
  <intent-filter>
    <action android:name="android.intent.action.SEND" />
    <category android:name="android.intent.category.DEFAULT" />
    <data android:mimeType="image/*" />
  </intent-filter>
</activity>
```
Treat incoming data as untrusted: validate MIME type and size, copy the content from the URI via
`contentResolver.openInputStream` promptly (grants are temporary), and never read arbitrary file paths
from extras. Direct Share targets via sharing shortcuts (`ShortcutManagerCompat`).

## iOS
Use SwiftUI `ShareLink` or UIKit `UIActivityViewController`; receiving from other apps needs a Share Extension target. This skill was not checked against Apple's documentation, so read it for current details.

## Verify
- [ ] Implicit intents handle the no-app case; `<queries>` covers any `resolveActivity` calls.
- [ ] Shared files open in the target app (grant flags, FileProvider paths).
- [ ] Receiving paths validate input.

## Checked
2026-11-01. Confirmed against the Android sharing (sharesheet), activity result and package visibility pages: Activity Result API registration rule, package visibility filtering from API 30 with `<queries>` and QUERY_ALL_PACKAGES approval, createChooser, EXTRA_TITLE, ClipData preview, FileProvider sharing. Removed (not confirmed): Binder size limit, direct startActivity needing no `<queries>`, and the iOS code and iPad/extension specifics.
Method: documentation only; no commands were run.
