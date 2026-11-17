---
id: computing-software.software-engineering.mobile-development.android-scoped-storage-and-mediastore
name: android-scoped-storage-and-mediastore
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, scoped-storage, mediastore, storage-access-framework, manage-external-storage, photo-picker]
level: practitioner
status: docs-checked
description: "Handle files under Android scoped storage: app-specific dirs, MediaStore inserts, Storage Access Framework, photo picker, and the MANAGE_EXTERNAL_STORAGE limits."
sources: ["https://developer.android.com/training/data-storage", "https://developer.android.com/training/data-storage/shared/media", "https://developer.android.com/training/data-storage/shared/documents-files", "https://developer.android.com/training/data-storage/manage-all-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scoped storage and MediaStore

Apps that target Android 10 (API 29) or higher get scoped storage by default: access only to their app-specific directory on external storage plus the media types they created. On Android 11+ (target API 30), `WRITE_EXTERNAL_STORAGE` has no effect on storage access. Choose storage by the purpose of the file, not its location.

## Pick the right place
| Need | API |
|---|---|
| private files | `getFilesDir()`, `getCacheDir()`; external `getExternalFilesDir()` / `getExternalCacheDir()` (no permission on API 19+) |
| save a photo/video/audio to the shared library | `MediaStore` insert (no storage permission on Android 10+ for files your app owns) |
| user picks or saves a document | Storage Access Framework (`ACTION_OPEN_DOCUMENT`, `ACTION_CREATE_DOCUMENT`, `ACTION_OPEN_DOCUMENT_TREE`) |
| user picks images/video | Android photo picker: no need to grant access to the whole media library (supported devices only) |
| file manager, backup, antivirus | `MANAGE_EXTERNAL_STORAGE` (all-files access), restricted by Google Play policy |

## Save an image
```kotlin
val values = ContentValues().apply {
    put(MediaStore.Images.Media.DISPLAY_NAME, "photo.jpg")
    put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
    put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/MyApp")
    put(MediaStore.Images.Media.IS_PENDING, 1)
}
val uri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)!!
resolver.openOutputStream(uri)!!.use { bitmap.compress(Bitmap.CompressFormat.JPEG, 90, it) }
values.clear(); values.put(MediaStore.Images.Media.IS_PENDING, 0)
resolver.update(uri, values, null, null)
```

## Gotchas
- Reading other apps' media requires `READ_MEDIA_IMAGES` / `READ_MEDIA_VIDEO` / `READ_MEDIA_AUDIO`, and the files must be in `MediaStore.Images`, `Video` or `Audio`. Requesting both images and video shows one runtime dialog. The images and video permissions are restricted to specific use cases by Google Play policy; the guide recommends the photo picker instead. On Android 9 or lower (or when opted out of scoped storage) use `READ_EXTERNAL_STORAGE`, plus `WRITE_EXTERNAL_STORAGE` (`maxSdkVersion="29"` in the guide's snippet) to modify.
- Another app's files in `MediaStore.Downloads` must be opened through the Storage Access Framework.
- Unredacted photo EXIF location needs `ACCESS_MEDIA_LOCATION` (declared and requested at runtime; user consent is not guaranteed).
- `IS_PENDING = 1` gives your app exclusive access while writing (Android 10+); set it back to 0 when finished. Use `DISPLAY_NAME` and `RELATIVE_PATH` to create or move files, not the `DATA` column. Run `query()` on a worker thread.
- Targeting Android 11+ and not the default gallery app: modifying or deleting media shows a user confirmation dialog each time.
- Persist access to a picked document with `takePersistableUriPermission`; access is lost if the document is moved or deleted. Do not use `CATEGORY_OPENABLE` if virtual files must be listed.
- `MANAGE_EXTERNAL_STORAGE` is granted by sending the user to the "Allow access to manage all files" settings page via `ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION`; check with `Environment.isExternalStorageManager()`. It does not reach other apps' `Android/data` directories. For apps targeting Android 11+, Google Play evaluates its use: request it only when SAF or MediaStore cannot do the job and it is core functionality (file managers, backup, antivirus, document management, on-device search, disk encryption, data migration).

Verify: save an image through `MediaStore`, confirm it appears in the gallery with no storage permission in the merged manifest, and exercise the picker and Storage Access Framework paths on Android 10 and on a newer version.

## Checked
Date: 2026-11-08. Confirmed against the Android Developers pages Data and file storage overview, Access media files from shared storage, Access documents and other files from shared storage and Manage all files on a storage device. Removed unconfirmed claims: API 33 permission versioning, Android 14 partial photo access (`READ_MEDIA_VISUAL_USER_SELECTED`), the `PickVisualMedia` API name (photo picker guide not in sources), "raw File paths fail" and the Play Console declaration step.
Method: documentation only; no commands were run.
