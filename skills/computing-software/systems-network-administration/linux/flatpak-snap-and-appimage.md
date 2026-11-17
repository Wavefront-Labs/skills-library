---
id: computing-software.systems-network-administration.linux.flatpak-snap-and-appimage
name: flatpak-snap-and-appimage
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, flatpak, snap, appimage, snapd, flathub, universal-packages, sandboxed-apps, flatpak-override, flatseal, snap-refresh, snap-channels, snap-confinement, appimagelauncher, fuse, desktop-apps, lpic-1, sysadmin, snap-connect, snap-revert, flatpak-runtimes]
level: intro
status: gated
description: "Manage distro-independent apps: Flatpak (Flathub, overrides, runtimes), Snap (channels, refresh control, confinement), AppImage (FUSE), and when each is the wrong choice."
sources:
  - https://docs.flatpak.org/en/latest/using-flatpak.html
  - https://snapcraft.io/docs/managing-updates
  - https://docs.appimage.org/user-guide/run-appimages.html
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Flatpak, Snap and AppImage — apps outside the distro package manager

**Goal:** install a current desktop or CLI app on any distro without touching system
libraries, keep it updated (or deliberately not), and know what it is allowed to see.

| | Flatpak | Snap | AppImage |
|---|---|---|---|
| Daemon | none (needs `flatpak` + a remote) | `snapd` (system service, auto-refresh) | none |
| Sandbox | bubblewrap, portal-based, permissions per app | AppArmor + seccomp, interfaces | none (plain binary) |
| Store | Flathub (any), distro remotes | Snap Store only (Canonical-run) | per-project download |
| Typical for | desktop apps on any distro | Ubuntu default; also server CLIs (lxd, certbot, juju) | portable one-off tools |
| Updates | `flatpak update`, or GNOME Software | automatic, 4×/day, hard to disable | manual (or AppImageUpdate) |

Rule: distro package first (`apt`/`dnf`) for anything a server depends on. These (gated: unconfirmed, source is paywalled or blocked)
formats are for desktop apps the distro ships old or not at all, or when the vendor
only publishes a snap (certbot, LXD, microk8s on Ubuntu).

## 1. Flatpak
```bash
# Debian/Ubuntu: apt install flatpak gnome-software-plugin-flatpak ; Fedora has it built in
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.mozilla.firefox        # app IDs are reverse-DNS; search: flatpak search firefox
flatpak run org.mozilla.firefox                     # also appears in the desktop menu after re-login
flatpak list --app; flatpak update; flatpak uninstall --unused   # remove orphan runtimes
```
- `--user` installs under `~/.local/share/flatpak` without root; default is system-wide
  (`/var/lib/flatpak`). Mixed installs are confusing: pick one per machine.
- Runtimes (`org.freedesktop.Platform//23.08`, `org.gnome.Platform`) are shared
  per-version and large (hundreds of MB); apps pin a runtime branch and a runtime EOL
  warning on `flatpak update` means the app itself is unmaintained.
- Permissions: `flatpak info --show-permissions org.app`,
  override per app: `flatpak override --user org.app --filesystem=home` (or
  `--filesystem=/srv/data:ro`, `--socket=pulseaudio`, `--nofilesystem=home` to tighten);
  `flatpak override --user --reset org.app` undoes. **Flatseal** (`com.github.tchx84.Flatseal`)
  is the GUI for the same files (`~/.local/share/flatpak/overrides/`).
- File dialogs work through portals (`xdg-desktop-portal` + the GTK/KDE backend must be
  installed, or dialogs are blank). Themes/fonts: apps see `~/.themes` only if granted.
- A flatpak's data lives in `~/.var/app/<id>/`; `flatpak uninstall --delete-data` removes it.
- Enterprise: host your own remote (`flatpak build-export` into an OSTree repo) and
  `flatpak remote-modify --disable flathub` to switch the public remote off.

## 2. Snap
```bash
# Ubuntu: preinstalled. Others: apt/dnf install snapd ; systemctl enable --now snapd.socket ; ln -s /var/lib/snapd/snap /snap
snap find certbot
snap install certbot --classic      # --classic = no confinement (vendor must be allowed to publish classic)
snap install lxd --channel=5.21/stable
snap list; snap info lxd            # channels: <track>/<risk>  e.g. latest/stable, 5.21/candidate
snap refresh lxd --channel=5.21/stable
snap revert lxd                     # back to the previous revision (kept on disk)
snap remove --purge firefox
```
- Auto-refresh: `snap refresh --time` shows the schedule. Control it:
  `snap set system refresh.timer=sat,03:00-05:00` (window), `snap set system refresh.hold=forever`
  (snapd ≥ 2.58; older: `refresh.hold=<RFC3339 ≤ 90 days>`), `snap refresh --hold lxd`
  per snap; `snap refresh --unhold`. A refresh restarts the app's services — plan the
  window on servers. `snap set system refresh.retain=2` limits kept revisions (disk).
- Confinement: `strict` snaps need interfaces; `snap connections firefox`,
  `snap connect firefox:removable-media`. Home directory outside `/home` (e.g. LDAP
  `/export/home`) breaks strict snaps — `snap set system homedirs=/export/home`.
- Each snap is a loop-mounted squashfs: `df -h` and `lsblk` fill with `/dev/loopN`
  entries; that is normal. Logs: `journalctl -u snapd`, `snap changes`, `snap tasks <id>`.
- Proxy: `snap set system proxy.http=http://proxy:3128 proxy.https=...`. Offline:
  `snap download lxd` then `snap ack lxd_*.assert && snap install lxd_*.snap`.
- Ubuntu's `apt install firefox`/`chromium` is a transitional deb that installs the snap;
  for a real deb add Mozilla's apt repo with a pin, or use Flatpak.

## 3. AppImage
```bash
chmod +x App-1.2.3-x86_64.AppImage
./App-1.2.3-x86_64.AppImage                 # that's it
./App.AppImage --appimage-extract           # unpack to squashfs-root/ (no FUSE needed)
./App.AppImage --appimage-extract-and-run   # run without FUSE
```
- Needs FUSE: older AppImages (type 2 with libfuse2) fail on Ubuntu ≥ 22.04 with
  `dlopen(): error loading libfuse.so.2` — `apt install libfuse2` (24.04: `libfuse2t64`),
  or use the extract-and-run flag. Newer AppImages (static runtime) do not need it.
- No sandbox, no updates, no menu entry by default. For menu integration install
  **AppImageLauncher** or put a `.desktop` file in `~/.local/share/applications` that
  points at the file; keep AppImages in one dir (`~/Applications`). `AppImageUpdate`
  works only if the publisher embedded update information (most do not); otherwise
  updating means downloading the next release by hand.
- Verify what you downloaded against the project's checksum or signature. Treat an AppImage exactly like a random
  binary from the internet, because that is what it is.
- An AppImage on a `noexec` `/home` or `/tmp` will not run because the mount options block
  execution; extract or move it to an exec-permitted location.

## 4. Choosing and cleaning up
- Disk: `flatpak uninstall --unused`, `snap set system refresh.retain=2` +
  `snap remove --revision=<old>`, delete old AppImages by hand.
- Theming/scaling bugs in Flatpak and Snap apps are usually a missing portal backend or
  a permission (`--filesystem=xdg-config/gtk-3.0:ro` as a flatpak override).
- CLI tools from these formats are not on `PATH` as expected: flatpak → `flatpak run`
  or an alias; snap → `/snap/bin` (must be in `PATH`, including for `sudo` via
  `secure_path`); AppImage → symlink into `~/.local/bin`.
- Remove snapd entirely on a Debian-based desktop that prefers Flatpak:
  `snap list`, `snap remove` each, `apt purge snapd`, `apt-mark hold snapd`.

## Verify
- [ ] `flatpak run <id>` launches, `flatpak info --show-permissions <id>` shows the
      overrides you set, and the app can open a file from the directory you granted.
- [ ] `snap refresh --time` shows your maintenance window and `snap list` shows the
      intended channel; `snap revert` after a test refresh restores the previous revision.
- [ ] An AppImage runs both directly and with `--appimage-extract-and-run`.

## Checked

2026-11-02

- Confirmed: Flatpak using-flatpak page, AppImage run guide and the Flathub repo file were fetched.
- Removed or gated: The snapcraft managing-updates page is a stub; snap flags (--classic, --channel, --purge) and flatpak override/info syntax are gated, confirm in the current snap and flatpak references.

Method: documentation only; no commands were run.
