---
id: computing-software.software-engineering.java.jpackage-native-installers
name: jpackage-native-installers
category: computing-software
field: software-engineering
product: java
tags: [java, java-modules-packaging, jpackage, native-installer, msi, deb, dmg, app-image, bundled-runtime]
level: practitioner
status: docs-checked
description: "Package a Java app with jpackage: modular and non-modular inputs, app images, jlink runtime options, package types, launchers, resource-dir overrides (JDK 21 man page)."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/jpackage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jpackage

jpackage takes a Java application and a Java run-time image and produces an application image with its dependencies. It can produce a native package such as exe on Windows or dmg on macOS. Each format must be built on the platform it runs on; there is no cross-platform support.

## Commands (from the man page examples)
```bash
# modular application
jpackage -n name -p modulePath -m moduleName/className
# non-modular application
jpackage -i inputDir -n name --main-class className --main-jar myJar.jar
# from a pre-built application image
jpackage -n name --app-image appImageDir
# application image only
jpackage --type app-image -n name -p modulePath -m moduleName/className
# own jlink options: run jlink separately, then pass the runtime image
jlink --output appRuntimeImage -p modulePath --add-modules moduleName --no-header-files
jpackage --type app-image -n name -m moduleName/className --runtime-image appRuntimeImage
# Java runtime package
jpackage -n name --runtime-image <runtime-image>
```

## Key options
- `--type`/`-t`: one of app-image, exe, msi, rpm, deb, pkg, dmg. If omitted a platform-dependent default type is created.
- `--module`/`-m` or `--main-jar` (with optional `--main-class`): use one, not both. `--main-class` only works with `--main-jar`. `--main-jar` is a path relative to `--input`.
- `--input`/`-i`: every file in the directory is packaged into the application image.
- `--module-path`/`-p`, `--add-modules`: the module list plus the main module is passed to jlink as `--add-module`. Without `--add-modules`, either just the main module (with `--module`) or the default module set (with `--main-jar`) is used.
- `--jlink-options`: if not given, defaults to `--strip-native-commands --strip-debug --no-man-pages --no-header-files`. `--runtime-image` skips the jlink step and copies the prepared image.
- `--java-options` (options for the Java runtime), `--arguments` (used if the launcher gets none), `--icon`, `--app-version`, `--vendor`, `--copyright`, `--description`, `--dest` (default current directory), `--verbose`.
- `--temp dir`: if given, the directory is not removed afterwards and must be removed manually; otherwise a temp directory is created and removed.
- `@filename` reads options from a file.
- `--add-launcher name=path`: properties file whose keys (module, main-jar, main-class, description, arguments, java-options, app-version, icon, launcher-as-service, win-console, win-shortcut, win-menu, linux-app-category, linux-shortcut) add to or override the command-line options to build an extra launcher.
- `--file-associations path` (keys extension, mime-type, icon, description), `--license-file`, `--install-dir`, `--app-content`, `--launcher-as-service` (registers the main launcher as a background service).

## Platform options
- Windows: `--win-console`, `--win-dir-chooser`, `--win-menu`, `--win-menu-group`, `--win-shortcut`, `--win-shortcut-prompt`, `--win-per-user-install`, `--win-upgrade-uuid` (UUID associated with upgrades for this package), `--win-help-url`, `--win-update-url`.
- Linux: `--linux-package-name` (default the app name), `--linux-deb-maintainer`, `--linux-package-deps`, `--linux-rpm-license-type`, `--linux-app-release`, `--linux-app-category`, `--linux-menu-group`, `--linux-shortcut`.
- macOS: `--mac-package-identifier` (alphanumeric, hyphen, period), `--mac-package-name` (under 16 characters), `--mac-sign`, `--mac-signing-keychain`, `--mac-signing-key-user-name`, `--mac-entitlements`, `--mac-app-store`, `--mac-dmg-content`.
- Sign an existing image on macOS: `jpackage --type app-image --app-image <app-image> --mac-sign ...`; in that mode only the mac signing options and `--verbose` are permitted.

## Resource directory
`--resource-dir` overrides jpackage resources by file name. Examples from the page: `<launcher-name>.png`/`.desktop` on Linux, `<launcher-name>.ico` on Windows, `<launcher-name>.icns` and `Info.plist` on macOS; for Linux DEB `control`, `copyright`, `preinstall`, `postinstall`, `prerm`, `postrm`; for RPM `<package-name>.spec`; for Windows MSI/EXE `main.wxs` and `overrides.wxi`, and `<application-name>-post-image.wsf`.

## Verify
Build `--type app-image` first and run its launcher; then build the installer type on the matching OS and test install and uninstall.

## Checked
Confirmed against the JDK 21 `jpackage` man page (options, examples, resource directory). Removed: WiX version requirements, MSI version limits, upgrade-UUID side-by-side behaviour, notarization, SmartScreen/antivirus remarks, JVM patching advice, a jdeps recipe and the overview page as a source, none of which the man page states.
Method: docs-only read of cited pages, 2026-11-08
