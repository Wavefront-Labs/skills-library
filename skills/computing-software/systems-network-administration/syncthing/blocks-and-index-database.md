---
id: computing-software.systems-network-administration.syncthing.blocks-and-index-database
name: blocks-and-index-database
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, blocks, block-list, index-database]
level: practitioner
status: docs-checked
description: "Understand how Syncthing splits files into hashed blocks, compares block lists and tracks local versus global versions."
sources: ["https://docs.syncthing.net/users/syncing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocks, block lists and the index

## Blocks
Syncthing splits each file into equal-size blocks (the last may be smaller). Block size depends on file size and ranges from 128 KiB to 16 MiB. It computes the SHA-256 of every block, producing a block list of offset, size and hash.

## Updating a file
To move from the current version to the wanted one, Syncthing compares the two block lists and looks for a source for each differing block:
- locally, if another file already holds a block with the same hash, in which case it is copied on disk
- from another device, in which case it is requested over the network

Each copied or received block is hashed again. A mismatch discards it and another source is tried. Good blocks go into a temporary copy of the file.

## Versions and the index
For each file Syncthing tracks the local version on disk, the versions announced by connected devices, and the best (usually newest) one, called the global version. A device tries to converge on the global version. This data lives in the index database, in files named `index-*` with a version number, in the configuration or data directory.

When new index data arrives, the global version is recalculated and compared with the local one. If they differ, the file is queued and only the needed blocks are fetched.

## Consequence
Syncthing requests only blocks whose hashes differ. Finding which parts of a file changed needs the file to be read and each block hashed again, because the docs say this cannot be known otherwise.

## Checked
2026-11-04. Read Understanding Synchronization: block size range 128 KiB to 16 MiB, SHA256 per block, block list of offset/size/hash, local copy versus network request, hash check with discard and retry, temporary copy, local/global version, `index-*` files in the configuration or data directory. Reworded the closing consequence to what the page states.
Method: documentation only; no commands were run.
