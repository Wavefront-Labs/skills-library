---
id: computing-software.software-engineering.objective-c.gnustep-make
name: gnustep-make
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ops, gnustep-make]
level: advanced
status: draft
description: "Build Objective-C on Linux with GNUstep: install toolchain, write a GNUmakefile, and source GNUstep.sh."
sources:
  - https://www.gnustep.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GNUstep on Linux
**Goal:** compile Foundation-based Objective-C on non-Apple platforms.

```make
# GNUmakefile
include $(GNUSTEP_MAKEFILES)/common.make
TOOL_NAME = hello
hello_OBJC_FILES = main.m
hello_OBJCFLAGS += -fobjc-arc
include $(GNUSTEP_MAKEFILES)/tool.make
```
```bash
# Debian/Ubuntu package names vary by release (unconfirmed): gobjc, gnustep, gnustep-devel, libgnustep-base-dev
. "$(gnustep-config --variable=GNUSTEP_MAKEFILES)/GNUstep.sh"    # sets GNUSTEP_MAKEFILES etc.
make
./obj/hello
```
- GNUstep provides gnustep-base (Foundation), gnustep-gui (AppKit-like), gnustep-make, and libobjc2 as the runtime.
- Makefile templates: `tool.make`, `application.make`, `library.make`, `framework.make`, `bundle.make`.
- Use clang with libobjc2 for ARC, blocks and modern features; GCC's runtime lacks them.
- Docker: build from a Debian/Ubuntu image, `apt-get install` the packages, then `make`; mount sources and build in CI to verify portability.
- Foundation coverage is large but not identical to Apple's; check for missing classes or behaviours.

## Gotchas
- Without sourcing `GNUstep.sh`, `GNUSTEP_MAKEFILES` is unset and make fails on include.
- Link flags for blocks and ARC require libobjc2 and libdispatch.

## Self-check
Build and run hello world in a clean container.
