---
id: computing-software.software-engineering.perl.file-locking-binary-io
name: file-locking-binary-io
category: computing-software
field: software-engineering
product: perl
tags: [perl, flock, binmode, sysopen, autoflush, seek-tell, fcntl, file-locking-binary-io]
level: advanced
status: docs-checked
description: "Use flock safely, read and write binary data with binmode and sysread, seek/tell, truncate, and control buffering."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlopentut", "https://perldoc.perl.org/Fcntl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File locking, binary I/O and buffering

**Goal:** correct low-level I/O.

```perl
use Fcntl qw(:flock :seek O_RDWR O_CREAT O_EXCL);
open(my $fh, '>>', $log) or die; flock($fh, LOCK_EX) or die "flock: $!";
print {$fh} $entry; $fh->flush; flock($fh, LOCK_UN);    # close also releases
flock($fh, LOCK_EX | LOCK_NB) or warn "busy";            # non-blocking attempt
sysopen(my $lock, $lockfile, O_RDWR|O_CREAT|O_EXCL, 0600) or die "exists: $!";   #
binmode($in, ':raw'); read($in, my $hdr, 4) == 4 or die;  my ($magic, $len) = unpack('A2 n', $hdr);
seek($fh, 0, SEEK_SET); my $pos = tell($fh); truncate($fh, 0);
sysread($fh, my $buf, 8192);  syswrite($out, $buf);      # unbuffered
$| = 1;  STDOUT->autoflush(1);                            # unbuffered STDOUT
```

## Rules
- `flock` is advisory: locks are merely advisory (perlfunc flock), so only cooperating processes honour it.
- On DOSish platforms text mode applies the `:crlf` layer (perlport), so use `binmode` for binary data.
- `read` returns 0 at EOF and undef on error; check both.

## Failure modes

## Self-check
- [ ] Two parallel runs of an appender with `flock` never interleave a line.

## Checked
2026-11-03: confirmed against perlfunc (flock is advisory and waits indefinitely; read returns 0 at EOF and undef on error; binmode, seek, tell, truncate, sysread, syswrite), Fcntl (flock constants, SEEK_*, O_RDWR O_CREAT O_EXCL), perlport (:crlf text mode) and perlvar (autoflush). Removed: NFS claim, lock-file and rename advice, mixing buffered and sys I/O claim, character-position seek claim, File::Temp advice and the two failure-mode claims.
Method: documentation only; no commands were run.
