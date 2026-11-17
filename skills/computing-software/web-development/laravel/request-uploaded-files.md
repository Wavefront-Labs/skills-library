---
id: computing-software.web-development.laravel.request-uploaded-files
name: request-uploaded-files
category: computing-software
field: web-development
product: laravel
tags: [laravel, requests, file-uploads, uploadedfile, storage]
level: intro
status: docs-checked
description: "Read uploaded files in Laravel with file, hasFile, isValid, extension, then save them with store and storeAs to a filesystem disk."
sources:
  - https://laravel.com/docs/requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Retrieve an `Illuminate\Http\UploadedFile` (extends `SplFileInfo`):

```php
$file = $request->file('photo');
$file = $request->photo;
if ($request->hasFile('photo')) { }
if ($request->file('photo')->isValid()) { }
$path = $request->photo->path();
$extension = $request->photo->extension();
```

`extension` guesses the extension from the file's contents, which may differ from the extension the client supplied.

For an image you need to manipulate, `$request->image('photo')` returns an `Illuminate\Image\Image` instance, or `null` if the file is not present.

Store on a configured filesystem disk. `store` takes a directory path (no filename, since a unique ID is generated as the filename) and an optional disk; it returns the path relative to the disk root:

```php
$path = $request->photo->store('images');
$path = $request->photo->store('images', 's3');
```

`storeAs` takes the path, filename and optional disk:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');
$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

## Checked

2026-11-07

Method: read the whole requests page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed file(), dynamic access, hasFile, isValid, path, extension, image(), store (generated name, optional disk, relative path returned) and storeAs. The linked Symfony UploadedFile API page was not opened.
