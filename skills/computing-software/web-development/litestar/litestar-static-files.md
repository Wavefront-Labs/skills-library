---
id: computing-software.web-development.litestar.litestar-static-files
name: litestar-static-files
category: computing-software
field: web-development
product: litestar
tags: [litestar, static-files, fsspec, file-system, create-static-files-router, html-mode, symlinks, filesystemregistry]
level: practitioner
status: docs-checked
description: "Serve static files in Litestar with create_static_files_router, HTML mode and attachments, plus local, fsspec and registry-based file systems and symlink safety."
sources: [https://docs.litestar.dev/latest/usage/static-files.html, https://docs.litestar.dev/latest/usage/file_systems.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar static files and file systems

Goal: serve a directory (local or remote) safely.

## Method

1. Serve a directory: `create_static_files_router(path="/static", directories=["assets"])` (from `litestar.static_files`) and pass it in `route_handlers`. `assets/hello.txt` is then at `/static/hello.txt`. Directories are relative to the working directory the app is started from.
2. Files are sent inline (`Content-Disposition: inline`). Set `send_as_attachment=True` for `attachment`.
3. HTML mode: `create_static_files_router(path="/", directories=["html"], html_mode=True)` serves `/index.html` for `/` and tries `/404.html` for missing files.
4. Router options (those of `Router`) can be passed straight to the function; `router_class` swaps the router class.
5. Reverse a file URL: `app.route_reverse(name="static", file_path="/some_file.txt")` gives `/static/some_file.txt`; `url_for` works too. `name` must match the `name` given to the function (default `static`).
6. File systems: pass `file_system=` an implementation of `BaseFileSystem` or any fsspec file system (for example `FTPFileSystem(host="127.0.0.1")`). Litestar ships `BaseLocalFileSystem`. fsspec systems are wrapped in `FsspecSyncWrapper` or `FsspecAsyncWrapper`. S3, GCS and Azure work through S3FS, GCSFS and adlfs.
7. Wrap once rather than on every use: `FsspecAsyncWrapper(fsspec.filesystem("s3", asynchronous=True))`, or register it. Async fsspec systems must be built with `asynchronous=True` and without passing a `loop`.
8. Registry: `Litestar([handler], plugins=[FileSystemRegistry({"assets": assets_fs})])` then `File(file_name, file_system="assets")`. The registry plugin is set up automatically unless you pass one. Default for sending files: `FileSystemRegistry(default=fsspec.filesystem("s3", asynchronous=True))`; otherwise the default is `BaseLocalFileSystem`.
9. Symlinks: `allow_symlinks_outside_directory` is disabled by default so links cannot point outside the base directories. Keep it off unless every symlink is known and permissions are right. On a file system that is not a `LinkableFileSystem`, setting it to anything but `None` raises `TypeError`. Register existing symlink-capable file systems with `LinkableFileSystem.register_as_linkable`; fsspec `LocalFileSystem` is already registered.

## Verify

The page's full example expects `GET /static/hello.txt` to return the file; in HTML mode, `/`, `/index.html` and a missing path (served from `404.html`) are the documented requests.

## Checked

2026-11-07. Read the full cited page(s) (usage/static-files.html, usage/file_systems.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
