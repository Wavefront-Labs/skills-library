---
id: computing-software.software-engineering.perl.ffi-platypus-native-libs
name: ffi-platypus-native-libs
category: computing-software
field: software-engineering
product: perl
tags: [perl, ffi-platypus, native-library, attach-function, ffi-checklib, shared-library, ffi-platypus-native-libs, perl-interop-ffi]
level: advanced
status: draft
description: "Call functions in shared libraries from Perl without XS using FFI::Platypus and FFI::CheckLib."
sources: ["https://metacpan.org/pod/FFI::Platypus", "https://metacpan.org/pod/FFI::Platypus::Type", "https://metacpan.org/pod/FFI::CheckLib"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling C libraries with FFI::Platypus

**Goal:** reuse a C library with a few lines of Perl.

```perl
use FFI::Platypus 2.00;                       # API level 2 (recommended in current docs)
use FFI::CheckLib qw(find_lib_or_die);
my $ffi = FFI::Platypus->new(api => 2, lib => [undef]);       # undef: libc and the executable's symbols
$ffi->attach(puts => ['string'] => 'int');
puts("hello from C");

my $ffi2 = FFI::Platypus->new(api => 2, lib => find_lib_or_die(lib => 'z'));   # libz
$ffi2->attach(zlibVersion => [] => 'string');
$ffi2->attach(crc32 => ['unsigned long', 'opaque', 'unsigned int'] => 'unsigned long');

# strings and buffers
my ($ptr, $size) = scalar_to_buffer($data);               # FFI::Platypus::Buffer
# callbacks
my $closure = $ffi->closure(sub { return $_[0] + 1 });
$ffi->attach(apply => ['(int)->int', 'int'] => 'int');
# structs: FFI::C or FFI::Platypus::Record
```
Type names: `sint8..sint64`, `uint8..uint64`, `float`, `double`, `string`, `opaque` (pointer), `int` `long` `size_t`, arrays `int[10]`, pointers `int*`.

## Rules
- Match the C prototype exactly; a wrong type is a crash, not an error. Check header files.
- Strings: `string` arguments are NUL-terminated copies owned by Perl for the call; returned `string` is copied; use `opaque` plus `cast` for ownership-sensitive pointers.
- Manage lifetimes and free what C allocates (`attach` the library's free function).
- Platform-specific library names are found by `find_lib` (`libz.so`, `z.dll`, dylib); do not hard-code paths.
- Declare the dependency on FFI::Platypus and the library in `cpanfile`; provide `Alien::*` modules (Alien::Build) to build/find the native library on user systems.
- For wrapping C++ or generating bindings, XS or `FFI::Platypus::Lang::CPP` and bindings generators exist (check docs).
- Thread safety, callbacks across threads: read the docs; not generally safe.

## Self-check
- [ ] The attached function returns the expected value (for example `zlibVersion()` prints a version string).
