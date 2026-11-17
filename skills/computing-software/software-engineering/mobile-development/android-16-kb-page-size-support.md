---
id: computing-software.software-engineering.mobile-development.android-16-kb-page-size-support
name: android-16-kb-page-size-support
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, page-size-16kb, native-libraries, ndk, elf-alignment, play-requirement, agp]
level: advanced
status: docs-checked
description: "Make Android native code compatible with 16 KB memory pages: find 4 KB-aligned .so files, rebuild with NDK flags, update dependencies, and test on a 16 KB emulator."
sources: ["https://developer.android.com/guide/practices/page-sizes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Support 16 KB page sizes

Beginning with Android 15, AOSP supports devices configured with a 16 KB page size. Apps that use native code (`.so` libraries), directly or through an SDK, must be rebuilt with 16 KB ELF alignment. Google Play requires apps targeting Android 15 (API level 35) and higher to support 16 KB page sizes on 64-bit devices; per the guide, from 1 February 2027 app updates that do not support it cannot be released. Dates are Google's policy, so recheck the guide's "Google Play compatibility requirement" section.

## Do you have native code?
Native code means any C/C++ or NDK code, any third-party native library or SDK that ships `.so` files, or an app built by a third-party builder that bundles native libraries. In Android Studio use Build > Analyze APK, open the APK, and look in the `lib` folder for `.so` files; the Alignment column warns about misaligned ones. Pure Kotlin/Java apps (including all libraries) already support 16 KB devices, though testing in a 16 KB environment is still recommended.

## Check alignment
Android Studio (APK Analyzer and lint) flags unaligned libraries. By hand, with SDK Build-Tools 35.0.0 or higher and the NDK installed:
```bash
llvm-objdump -p libfoo.so | grep LOAD         # every align must be 2**14 or higher
zipalign -v -c -P 16 4 app-release.apk        # ends with "Verification successful" when .so files are 16 KB zip-aligned
```
`llvm-objdump` lives under the NDK's `toolchains/llvm/prebuilt/<host>/bin/`. Any LOAD segment aligned 2**13, 2**12 or lower must be fixed.

## Fix
- Packaging: use AGP 8.5.1 or higher with uncompressed shared libraries. If you cannot upgrade AGP, set `useLegacyPackaging` to true in `packagingOptions { jniLibs { ... } }` (compressed libraries, larger installed size).
- Compiling: NDK r28 and higher compile 16 KB-aligned by default. With AGP 8.5.1+, NDK r28+ and 16 KB-compatible prebuilt dependencies the app is compatible by default.
- NDK r27 and lower: link with `-Wl,-z,max-page-size=16384` and `-Wl,-z,common-page-size=16384`, via `LOCAL_LDFLAGS` in `Android.mk` for ndk-build or `target_link_options` in CMake. Prebuilt shared libraries must be rebuilt the same way and re-imported.
- Check each SDK vendor's site for a 16 KB-compatible version; some prebuilts are not.
- Remove code that hardcodes `PAGE_SIZE` or assumes 4096; use `getpagesize()` or `sysconf(_SC_PAGESIZE)`. `PAGE_SIZE` is undefined in 16 KB mode on NDK r27 and higher. Review `mmap()` and other page-aligned APIs.
- Custom allocators: scale release thresholds from `sysconf(_SC_PAGESIZE)` rather than fixed byte limits. Apps using the standard allocator (scudo) can skip this.

## Test
In Android Studio's SDK Manager, install an Android 15 or higher "Google APIs Experimental 16 KB Page Size" system image (ARM 64 v8a, or Intel x86_64 Atom), create a virtual device from it, and run `adb shell getconf PAGE_SIZE`, which must return `16384`. Other environments: Cuttlefish, the "Boot with 16KB page size" developer option on supported Pixel devices, Samsung Remote Test Lab. Run `zipalign -c -P 16 -v 4` on the APK too, then exercise every native code path.

## Gotchas
- A device with a 16 KB kernel can run an app with 4 KB-aligned `.so` files in 16 KB backcompat mode (it shows a warning on first launch); do not rely on it, since the guide says apps should still be 16 KB aligned for reliability.
- A `.so` built with NDK r27 or lower can have a GNU_RELRO segment whose end is not 16 KB aligned while sharing a writable LOAD segment with `.data`/`.bss`; that can crash with SIGSEGV on a 16 KB device. APK Analyzer reports RELRO status.

Verify: `adb shell getconf PAGE_SIZE` on the test device is 16384, zipalign verification succeeds, and the app launches, loads each native library and passes smoke tests.

## Checked
Date: 2026-11-08. Confirmed against the Android Developers "Support 16 KB page sizes" guide: Play requirement and 1 February 2027 date, APK Analyzer steps, llvm-objdump and zipalign commands, AGP 8.5.1 and NDK r28 thresholds, r27 linker flags, `useLegacyPackaging`, PAGE_SIZE guidance, emulator image names, getconf check, backcompat mode and RELRO notes. Removed the unsupported `APP_SUPPORT_FLEXIBLE_PAGE_SIZES` and `ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES` variables, the outdated 1 November 2025 date, and the Play Console help source (it is the target API page).
Method: documentation only; no commands were run.
