---
id: computing-software.software-engineering.php.php-path-traversal-inclusion
name: php-path-traversal-inclusion
category: computing-software
field: software-engineering
product: php
tags: [php, path-traversal-inclusion, security]
level: practitioner
status: docs-checked
description: "Prevent file inclusion and path traversal in PHP: allowlists, realpath checks, open_basedir and safe downloads."
sources: ["https://www.php.net/manual/en/function.realpath.php", "https://www.php.net/manual/en/ini.core.php", "https://www.php.net/manual/en/security.filesystem.php", "https://www.php.net/manual/en/function.include.php", "https://www.php.net/manual/en/wrappers.php.php", "https://www.php.net/manual/en/filesystem.configuration.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File inclusion and path traversal

Vulnerable patterns:
```php
include $_GET['page'] . '.php';              // LFI / RFI (with allow_url_include)
readfile('/srv/files/' . $_GET['f']);        // ../../etc/passwd
```
The manual's filesystem security page shows the same flaw: user-submitted `../etc` and `passwd` produce `/home/../etc/passwd`, and it notes that even a check on the login name can be defeated if users choose a name like `../etc/`.

Safe patterns:
```php
$pages = ['home' => 'home.php', 'about' => 'about.php'];     // allowlist by key
$file = $pages[$_GET['page'] ?? ''] ?? null ?: abort(404);
include __DIR__ . '/pages/' . $file;

$base = realpath('/srv/files');
$path = realpath($base . DIRECTORY_SEPARATOR . ($_GET['f'] ?? ''));
if ($path === false || !str_starts_with($path, $base . DIRECTORY_SEPARATOR)) { http_response_code(404); exit; }
header('Content-Disposition: attachment; filename="' . rawurlencode(basename($path)) . '"');
readfile($path);
```
Settings: `allow_url_include` (INI_SYSTEM, default 0, deprecated since PHP 7.4.0) lets `include` load remote files; keep it off. `allow_url_fopen` is INI_SYSTEM and defaults to 1; turn it off if the app does not need URL fopen wrappers. `open_basedir` is defence in depth: it limits file access to the listed directory trees, resolves symlinks, matches a directory name rather than a prefix, and disables the realpath cache. A script can tighten it at runtime with `ini_set()`. It does not restrict Unix domain sockets. Keep upload directories outside the web root and store files under generated IDs rather than user names (design advice, not from the manual).

## Gotchas
- `realpath` returns false on failure, for example when the file does not exist, so it cannot validate a path you are about to create: validate the parent directory, then use `basename` for the filename.
- `realpath` expands symbolic links and resolves `/./` and `/../`, and removes trailing delimiters from the result. This is why the canonical path is compared against the canonical base, rather than blacklisting `../`. On Windows, junctions and symlinks to directories are expanded only one level.
- Keep the trailing separator in the prefix check: because `realpath` strips trailing delimiters, a bare prefix comparison would also accept a sibling directory whose name starts with the base name.
- `php://filter` is a meta-wrapper that applies filters while opening a stream; it works with all-in-one functions like `readfile()` and `file_get_contents()`. Reject user-controlled scheme prefixes (`php://`) in paths.
- A path starting with `/`, a drive letter, `.` or `..` makes `include` ignore `include_path`, so an absolute path from the user is as dangerous as `../`.

Verify: request `?f=../../etc/passwd`, an absolute path and a sibling directory with the same name prefix, and confirm each returns 404.

## Checked
2026-11-09. Confirmed on php.net manual: realpath, ini.core (open_basedir), filesystem.configuration (allow_url_*), security.filesystem, include, wrappers.php. Removed: OWASP source (not read), encoding and null-byte bypass list, phar:// and zip-slip claims, and the filename-encoding detail (not on pages read).
Method: documentation only; no commands were run.
