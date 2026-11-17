---
id: computing-software.web-development.hugo.file-caches-config
name: file-caches-config
category: computing-software
field: web-development
product: hugo
tags: [caches, file-cache, maxage, garbage-collection, cachedir]
level: advanced
status: docs-checked
description: "Hugo file caches: the seven cache names, dir and maxAge keys, the :cacheDir, :project and :resourceDir tokens, and clearing old entries with hugo build --gc."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/caches.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo stores data on disk in file caches, to avoid repeated work in one build and to carry data from one build to the next.

Cache names:

- `assets`: processed CSS and Sass.
- `getresource`: files fetched with `resources.GetRemote`.
- `images`: processed images.
- `misc`: miscellaneous data, such as `transform.ToMath` results.
- `modulegitinfo`: Git information for modules.
- `modulequeries`: module resolution query results.
- `modules`: downloaded modules.

Keys per cache:

- `dir`: absolute path where cached files are stored. It can begin with `:cacheDir` or `:resourceDir`.
- `maxAge`: duration before an entry is evicted. `0` disables the cache for that key; `-1` means entries never expire (the default).

Tokens:

- `:cacheDir`: the designated cache directory.
- `:project`: the base directory name of the current project, which isolates each project's caches so `hugo build --gc` does not affect other projects.
- `:resourceDir`: the directory for asset pipeline output.

```toml
[caches.images]
dir = ':cacheDir/images'
```

Cached files from earlier builds or configurations can waste space. `hugo build --gc` removes expired or unused entries.

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure file caches: the seven cache names and what each stores, the `dir` and `maxAge` keys with 0 and -1 meanings and the -1 default, the three tokens, and garbage collection with `hugo build --gc`. Nothing removed.

Method: documentation only; no commands were run.
