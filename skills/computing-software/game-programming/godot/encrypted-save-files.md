---
id: computing-software.game-programming.godot.encrypted-save-files
name: encrypted-save-files
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-save-game, open_encrypted, save-tampering, save-encryption, game-programming]
level: practitioner
status: verified
description: "Encrypt Godot save files with FileAccess.open_encrypted_with_pass/open_encrypted, understand what it protects against, key handling, corruption detection and migration."
sources: ["https://docs.godotengine.org/en/stable/classes/class_fileaccess.html#class-fileaccess-method-open-encrypted-with-pass", "https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted save files

**Goal:** discourage casual save editing and detect corruption, with eyes open about the limits.

## API
```gdscript
const SAVE_PATH := "user://save_01.dat"
func save_game(data: Dictionary) -> Error:
    var f := FileAccess.open_encrypted_with_pass(SAVE_PATH, FileAccess.WRITE, _key())
    if f == null: return FileAccess.get_open_error()
    f.store_string(JSON.stringify(data))
    f.close()
    return OK
func load_game() -> Variant:
    var f := FileAccess.open_encrypted_with_pass(SAVE_PATH, FileAccess.READ, _key())
    if f == null:
        push_warning("save open failed: %s" % FileAccess.get_open_error())   # wrong key / corrupt -> ERR_FILE_CORRUPT
        return null
    return JSON.parse_string(f.get_as_text())
```
`open_encrypted(path, mode, key: PackedByteArray)` takes a 32-byte key directly (any other size returns null with
`ERR_INVALID_PARAMETER`, 31). `open_encrypted_with_pass` derives a 32-byte key from the MD5 hex text of the password
(engine source `core/io/file_access_encrypted.cpp`). Encryption is AES-256 in CFB mode with an MD5 check of the content
(same source); a wrong key opens as null with `ERR_FILE_CORRUPT` (16), and so do flipped bytes inside the data. A
flipped byte in the final padding bytes was not detected (the MD5 covers the data length, not the padding).

## Threat model
- The key lives in your game binary/scripts. Anyone decompiling the PCK can recover it (script and PCK encryption need
  an encryption key supplied at export and a custom-built export template; see the export pages of the Godot docs). This stops casual
  hex-editing, not determined players.
- For competitive/online value, saves must be server-authoritative.
- Per-user keys (derive from a platform user id + secret) prevent copying saves between accounts.

## Robustness
- Write to `save_01.dat.tmp`, close, then `DirAccess.rename_absolute(tmp, final)` so a crash mid-write
  doesn't destroy the old save. Keep one backup (`.bak`).
- Include a `version` field for migrations; decrypt failures should fall back to the backup.

## Gotchas
- Changing the key in an update locks out every existing save — keep old keys for migration.
- Encrypted files are not human-readable for debugging; add a debug-build flag to write plain JSON.
- `store_var` with `full_objects = true` can deserialize arbitrary objects (code execution risk) —
  don't use it for files players can swap, encrypted or not.

## Verify
- [ ] Flip one byte in the middle of the save: load reports corruption (`ERR_FILE_CORRUPT`) and falls back to backup.
- [ ] Kill the game during save: previous save still loads.
## Checked
Ran on Godot 4.7.2 headless: `open_encrypted_with_pass` write then read of JSON text; wrong password returns null and `get_open_error()` is 16 with the engine's "MD5 sum ... does not match" message; `open_encrypted` with a 2-byte key returns null, error 31; a 32-byte key file writes and its size is 60 bytes for 7 bytes of text; byte flip in the middle fails with 16, flip of the last byte still opened. AES-256 CFB, MD5 and the password-to-key step were read in the engine source at tag 4.7.2-stable. The "store_var with full_objects" warning was run in the binary-serialization skill.
