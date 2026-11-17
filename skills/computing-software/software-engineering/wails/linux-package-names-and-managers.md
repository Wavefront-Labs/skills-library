---
id: computing-software.software-engineering.wails.linux-package-names-and-managers
name: linux-package-names-and-managers
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, linux, package-manager, contributing, distro-support]
level: practitioner
status: docs-checked
description: "Add a distro-specific package name or a whole new package manager to the Wails CLI dependency detection."
sources: [https://wails.io/docs/guides/linux-distro-support]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make Wails detect and suggest the right development packages on a Linux distribution.

## Supported package managers
apt, dnf, emerge, eopkg, nixpkgs, pacman, xbps, zypper. Wails checks whether the packages you need are available through the system package manager by iterating a list of candidate package names.

## Add an alternative package name
Package lists live in `v2/internal/system/packagemanager/<pm>.go` (for apt, `apt.go`), in the `Packages()` method:

```go
"libgtk-3": []*Package{
	{Name: "libgtk-3-dev", SystemPackage: true, Library: true},
	{Name: "lib-gtk3-dev", SystemPackage: true, Library: true},
},
```

The second line is the added distro-specific name. Other entries seen: `libwebkit` (`libwebkit2gtk-4.0-dev`), `gcc` (`build-essential`), `pkg-config`, `npm`, and `docker` (`docker.io`, `Optional: true`).

## Add a new package manager
1. Create `v2/internal/system/packagemanager/<pm>.go`.
2. Implement the interface from `pm.go`:

```go
type PackageManager interface {
	Name() string
	Packages() packagemap
	PackageInstalled(*Package) (bool, error)
	PackageAvailable(*Package) (bool, error)
	InstallCommand(*Package) string
}
```

- `Name()` returns the manager name; `Packages()` returns candidate names per dependency; `PackageInstalled()` is true if installed; `PackageAvailable()` is true if not installed but installable; `InstallCommand()` returns the exact install command.
3. Look at the existing managers for guidance, and update the Linux distro support docs page.

Related: `computing-software.software-engineering.wails.linux-runtime-deps-and-nfpm`.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Linux Distro Support" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
