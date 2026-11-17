---
id: computing-software.game-programming.godot.godot-pck-encryption-keys
name: godot-pck-encryption-keys
category: computing-software
field: game-programming
product: godot
tags: [pck-encryption, godot, export, aes-key, encrypt-pck]
level: practitioner
status: docs-checked
description: "Encrypt exported Godot PCK files: generate the AES key, build export templates with it, set the export preset key and filters, and read the error."
sources:
  - https://raw.githubusercontent.com/godotengine/godot-docs/master/engine_details/development/compiling/compiling_with_script_encryption_key.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Godot PCK encryption

**Goal:** make casual extraction of game assets and scripts harder in a release build.

## Steps (Godot 4.x)
1. Generate a 256-bit AES key in hexadecimal: `openssl rand -hex 32 > godot.gdkey`. Do not reuse an example key from any docs page. Redirecting to a file lowers the risk of exposing the key compared with printing it.
2. Official precompiled export templates do not work with PCK encryption. Build your own export templates from source with the same key.
3. Set the environment variable `SCRIPT_AES256_ENCRYPTION_KEY` to the key in the console you compile Godot with (`export` on Linux/macOS, `set` in Windows cmd, `$env:` in PowerShell). These commands do not persist across terminal sessions.
4. Compile the export templates and set them as custom export templates in the export preset. If the variable is set correctly, compilation prints "Compiling Godot with custom `SCRIPT_AES256_ENCRYPTION_KEY` set as environment variable" at the start.
5. Set the same key in the **Encryption** tab of the export preset. For a command-line export, set the `GODOT_SCRIPT_ENCRYPTION_KEY` environment variable to the same value before exporting.
6. Add include filters for the files and folders to encrypt. By default the include filters are empty and nothing is encrypted.
7. Export the project.

## Limits
- The key must be stored in the binary. The docs say a compiled, optimised build without symbols takes some effort to search, so treat this as obfuscation. Never ship credentials in the PCK.
- A key missing from the build gives an error: `open_and_parse: Condition "String::md5(md5.digest) != String::md5(md5d)" is true. Returning: ERR_FILE_CORRUPT` at `core/io/file_access_encrypted.cpp`. Godot encrypted the PCK on export but cannot read it at runtime.

## Verify
- [ ] The compile output shows the custom-key message.
- [ ] The preset has include filters, not the empty default.
- [ ] The exported project starts and loads its encrypted resources without the ERR_FILE_CORRUPT error.

## Checked

2026-11-08. Read in full: compiling_with_script_encryption_key.rst (godot-docs, master; the old contributing/development/compiling path has moved to engine_details/development/compiling). Confirmed the key generation, both environment variables, the preset Encryption tab, the empty-filter default and the error text. Removed the unsourced preset checkbox labels, the DLC and patch advice, the load overhead claim and the hex-viewer check, none of which that page covers.

Method: documentation only; no commands were run.
