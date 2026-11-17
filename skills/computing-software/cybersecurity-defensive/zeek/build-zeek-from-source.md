---
id: computing-software.cybersecurity-defensive.zeek.build-zeek-from-source
name: build-zeek-from-source
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, build-from-source, configure, cross-compile]
level: practitioner
status: docs-checked
description: "Build Zeek from source: required dependencies, configure --prefix, auxil options, cross compiling with a CMake toolchain, and setting PATH afterwards."
sources: ["https://docs.zeek.org/en/current/building-from-source.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# build zeek from source

Required: Bash, Bison 3.3+, a C++20 compiler (GCC 12+ or Clang 10+), CMake 3.15+, Flex 2.6+, libpcap, Make, OpenSSL, Python 3.9+, SWIG, ZeroMQ 4.3.0+, zlib, and the BIND8 resolver library if libresolv lacks it.

Debian family:

```
sudo apt-get install bison cmake cppzmq-dev gcc g++ flex libfl-dev libpcap-dev libssl-dev make python3 python3-dev swig zlib1g-dev
```

If cppzmq-dev is missing, try libzmq3-dev. On RHEL/CentOS 9 a gcc-toolset gives a recent GCC. Windows support is experimental.

Then `./configure`, `make`, `make install`. The default prefix is `/usr/local/zeek`; use `--prefix` to change it, and avoid `/usr`, `/opt/bro` and `/opt/zeek`, which belong to binary packages. If configure fails it usually lacks a dependency, so use `--with-*` options (see `./configure --help`). `--disable-*` options skip auxil projects; `make install-aux` installs more of zeek-aux.

Cross compiling: build native tools first (`./configure --builddir=../zeek-buildtools`, then `make binpac bifcl`), then configure with `--toolchain=/path/to/toolchain.cmake --with-binpac=... --with-bifcl=...`.

Add the install `bin` directory to PATH, for example `export PATH=/usr/local/zeek/bin:$PATH`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
