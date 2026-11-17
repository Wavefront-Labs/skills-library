---
id: computing-software.game-programming.godot.dedicated-server-exports
name: dedicated-server-exports
category: computing-software
field: game-programming
product: godot
tags: [godot, multiplayerapi, godot-dedicated-server, headless-server, server-feature-tag, game-programming]
level: practitioner
status: docs-checked
description: "Build and run Godot dedicated servers: dedicated server export mode, stripping visuals, --headless, the dedicated_server feature tag, startup args and containerising."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html", "https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedicated server exports

**Goal:** a headless server build of the same project, small and with no GPU dependency, that starts
straight into hosting.

## Export
- Add a preset for the server platform, Resources tab > Export Mode: **Export as dedicated server**. This
  replaces visual resources (Cubemap, CubemapArray, Material, Mesh, Texture2D, Texture2DArray, Texture3D)
  with placeholders that keep only the image size. Tick files or folders in the list to choose per
  resource: **Strip Visuals**, **Keep** or **Remove** (Remove leaves the file out of the PCK).
- This mode adds the `dedicated_server` feature tag automatically. Writing `dedicated_server` in the
  preset's Features tab gives the tag without the mode and also forces `--headless`.
- Run with `--headless` (headless display server and Dummy audio driver). Use an export template
  binary rather than the editor binary to run servers: it is smaller and more optimised.

## Code paths
```gdscript
func _ready():
    if OS.has_feature("dedicated_server") or DisplayServer.get_name() == "headless":
        _start_server(_arg_int("--port", 7777))
    else:
        get_tree().change_scene_to_file("res://ui/main_menu.tscn")

func _arg_int(name: String, def: int) -> int:
    for a in OS.get_cmdline_user_args():      # args after "--" on the command line
        if a.begins_with(name + "="): return int(a.get_slice("=", 1))
    return def

func _start_server(port: int):
    var peer := ENetMultiplayerPeer.new()
    var err := peer.create_server(port, 32)
    if err != OK: push_error("server failed: %s" % err); get_tree().quit(1); return
    multiplayer.multiplayer_peer = peer
```
Run: `./game.x86_64 --headless -- --port=7777`.

## Server hygiene
- Don't load UI scenes or audio; guard visual-only nodes (`if not multiplayer.is_server()`), or keep
  separate server scenes.
- Logs go to stdout; use `--log-file` (absolute path) or capture the container output.

## Container
Package the exported server binary and its `.pck` in the image and start it with
`./game.x86_64 --headless -- --port=7777`. ENet only uses UDP, so publish and forward only the UDP port.

## Gotchas
- Stripped visuals: code that reads texture data (e.g. image-based maps) on the server breaks; mark those
  resources Keep.

## Verify
- [ ] Server image runs on a machine without a GPU and accepts client connections.
- [ ] Server PCK smaller than the client PCK (a normal export includes all resources, such as texture data).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `--headless` equals the headless display driver plus Dummy audio; export template binaries are recommended over the editor binary for servers; the Export as dedicated server mode, the list of placeholder-replaced resource classes and the Strip Visuals, Keep and Remove options; the automatic `dedicated_server` feature tag and the Features-tab alternative that forces `--headless`; `OS.get_cmdline_user_args()` returns arguments after `--`; `DisplayServer.get_name()` returns `headless` under `--headless`; `ENetMultiplayerPeer.create_server(port, max_clients)`; ENet uses only UDP; `--log-file`. Removed the unconfirmed collision-data, tick-rate, base-image, and GDExtension claims.

Method: documentation only; no commands were run.
