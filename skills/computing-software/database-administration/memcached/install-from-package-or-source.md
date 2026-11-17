---
id: computing-software.database-administration.memcached.install-from-package-or-source
name: install-from-package-or-source
category: computing-software
field: database-administration
product: memcached
tags: [install, package, build-from-source, libevent, configure]
level: intro
status: docs-checked
description: "Install memcached from an OS package or build from source with libevent, and know why packaged versions can be stale."
sources:
  - https://docs.memcached.org/serverguide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memcached works on most Linux and BSD like systems; there is no official support for windows builds.

Install from your OS package (the OS solves dependencies and takes care of security updates):
- Debian or Ubuntu: `apt-get install memcached`
- Redhat/Fedora: `yum install memcached`
- Mac: `brew install memcached`

Potential issue: the packaged version may be out of date, significantly so on an OS that can be several years old (such as Ubuntu LTS), so you may miss features or bug fixes. Your package manager may offer a newer version, you can use Docker, or you can build from source.

From source (depends on libevent and a C compiler):
```
apt-get install build-essential libevent-dev
yum install libevent-devel
```
(or whatever your OS needs), then
```
tar -zxf memcached-x.x.x.tar.gz
cd memcached-x.x.x
./configure --prefix=/usr/local/memcached
make && make test && sudo make install
```
See `./configure --help` for full options.

Memcached on its own is just a key/value storage daemon. Installing it does not automatically cache any of your data: applications need to be programmed to use it, with a client library for your language.

## Checked

2026-11-04. Confirmed against the Server Guide installation section. Removed: the unstated `--enable-tls` / `--enable-proxy` configure options and the `nc` version check.

Method: documentation only; no commands were run.
