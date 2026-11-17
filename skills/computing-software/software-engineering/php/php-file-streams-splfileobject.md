---
id: computing-software.software-engineering.php.php-file-streams-splfileobject
name: php-file-streams-splfileobject
category: computing-software
field: software-engineering
product: php
tags: [php, file-streams-splfileobject, files]
level: practitioner
status: docs-checked
description: "Read and write files in PHP with fopen, SplFileObject, locks, temp-file writes and php:// stream wrappers; stream large files."
sources: ["https://www.php.net/manual/en/book.filesystem.php", "https://www.php.net/manual/en/class.splfileobject.php", "https://www.php.net/manual/en/wrappers.php.php", "https://www.php.net/manual/en/function.flock.php", "https://www.php.net/manual/en/function.fopen.php", "https://www.php.net/manual/en/function.tempnam.php", "https://www.php.net/manual/en/function.file-put-contents.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File streams and SplFileObject

```php
// Stream a large CSV one row at a time
$f = new SplFileObject($path, 'r');
$f->setFlags(SplFileObject::READ_CSV | SplFileObject::SKIP_EMPTY | SplFileObject::READ_AHEAD | SplFileObject::DROP_NEW_LINE);
foreach ($f as $row) { /* array of fields */ }

// Locked append
$h = fopen($log, 'ab');
if (flock($h, LOCK_EX)) { fwrite($h, $line . PHP_EOL); fflush($h); flock($h, LOCK_UN); }
fclose($h);

// Replace a file via a temp file in the same directory, then rename
$tmp = tempnam(dirname($target), '.tmp');   // string|false; may fall back to the system temp dir
file_put_contents($tmp, $data, LOCK_EX);
rename($tmp, $target);

// Copy a stream without loading it
stream_copy_to_stream(fopen($src, 'rb'), fopen($dst, 'wb'));
file_get_contents('php://input');           // raw request body
$t = fopen('php://temp/maxmemory:1048576', 'r+');   // spill to a temp file after 1 MiB
```

## What the manual states
- `SplFileObject` flags: `READ_CSV`, `READ_AHEAD`, `SKIP_EMPTY` (skips empty lines and "requires the READ_AHEAD flag be enabled, to work as expected") and `DROP_NEW_LINE` (drops the newline at the end of a line).
- `flock()` is advisory: all accessing programs must lock the same way. It blocks by default (`LOCK_NB` avoids that). The lock is also released by `fclose()` or when the stream is garbage collected. It is not supported on FAT and derivatives (always returns false there). On Windows it uses mandatory locking.
- `file_put_contents()` with `LOCK_EX` takes an exclusive lock between the open and the write; it does not stop readers unless they also take a lock.
- `tempnam(string $directory, string $prefix): string|false` creates the file with permission 0600. If the directory does not exist or is not writable it may create the file in the system temp directory instead (since 7.1.0 with a notice), so the later `rename()` may then cross filesystems; check the returned path.
- `fopen()` modes: the default translation mode is `b`; on Windows `t` translates `\n` to `\r\n`. The manual recommends `b` except for plain-text files you need to read in old Notepad versions.
- `php://input` is a read-only raw request-body stream and can be read repeatedly; it is not available for `multipart/form-data` POSTs when `enable_post_data_reading` is enabled.
- `php://memory` always stays in memory; `php://temp` switches to a temporary file once the data reaches a limit (default 2 MB), settable with `/maxmemory:NN` in bytes.
- `php://filter` applies filters when opening a stream, useful with `file_get_contents()`, `file()` and `readfile()`.

## Gotchas
- `file()` and `file_get_contents()` read the whole file into memory; iterate with `SplFileObject` or `fgets` for big files.
- Handle `false` returns: PHP warns rather than throws unless you convert warnings to exceptions with an error handler.
- User-controlled paths passed to file functions can reach wrappers such as `php://filter` and URL wrappers; validate paths and reject any scheme you did not expect (see the path traversal skill).
- Close handles in `finally`.

Verify: process a file larger than `memory_limit` with the SplFileObject loop and watch `memory_get_peak_usage()` stay flat.

## Checked
Confirmed 2026-11-08 against the PHP manual pages for SplFileObject, flock, fopen, tempnam, file_put_contents, php:// wrappers and the filesystem book. Removed: any claim that `rename()` is atomic (the manual page text does not state it), that flock is unreliable on network filesystems, the return values of `fwrite` and `file_put_contents`, and the `allow_url_fopen` setting's behaviour.
Method: docs-only read of cited pages, 2026-11-08
