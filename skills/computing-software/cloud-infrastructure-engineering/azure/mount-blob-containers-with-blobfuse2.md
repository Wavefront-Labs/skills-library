---
id: computing-software.cloud-infrastructure-engineering.azure.mount-blob-containers-with-blobfuse2
name: mount-blob-containers-with-blobfuse2
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, blobfuse2, blobfuse, fuse-mount, linux, managed-identity]
level: practitioner
status: docs-checked
description: "Mount Blob containers on Linux with BlobFuse2: caching (file cache) vs streaming (block cache) mode, mount commands, config file and POSIX caveats."
sources: ["https://learn.microsoft.com/azure/storage/blobs/blobfuse2-what-is", "https://learn.microsoft.com/azure/storage/blobs/blobfuse2-how-to-deploy", "https://github.com/Azure/azure-storage-fuse"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount Blob containers with BlobFuse2

**Goal:** give file-based Linux apps access to Blob Storage, knowing where the filesystem illusion breaks.

## What it is
BlobFuse is an open-source (MIT) virtual file system driver. It uses libfuse (fuse3) and translates file operations into Azure Storage REST API calls, turning blob names into a directory-like structure with `/` delimiters. It mounts a container or a Data Lake Storage file system, on flat or hierarchical-namespace accounts. BlobFuse v1 support ends in September 2026; use v2.

## Two modes
- **Caching (file cache)**: downloads the whole file to a local cache directory before the app sees it; later reads and writes use the local copy until evicted or invalidated; closing a created or modified file uploads it. Good for files accessed repeatedly or datasets that fit the local disk.
- **Streaming (block cache)**: streams data in blocks as it downloads. Designed for large files (AI/ML training sets, genomics, HPC).

## Mount
```bash
sudo blobfuse2 mount <mount-path> --tmp-path=<local-cache-path>
sudo blobfuse2 mount <mount-path> --streaming
sudo blobfuse2 mount <mount-path> --config-file=<configuration-file>
```
- The first two take account name, container name and auth type and details from environment variables (see the BlobFuse environment variables page); other parameters such as memory, disk limits and parallelism are set automatically from the system.
- The config file is YAML holding settings and storage credentials. Microsoft and the GitHub repo ship sample files: file cache, block cache, distributed cache, and file cache with SAS. See the "All config options" page for keys.
- By default BlobFuse logs warnings to the system log.

## Supported operations and caveats
- Supported: mkdir, opendir, readdir, rmdir, open, read, create, write, close, unlink, truncate, stat, rename; chmod on hierarchical-namespace (HNS) accounts only.
- BlobFuse does not guarantee full POSIX compliance. Example: rename is atomic in POSIX but not in BlobFuse. Read "BlobFuse and Linux file systems compared" and the limitations page before relying on locking, links or permissions.
- Other features named on the overview: health monitor, blob filter (restrict which blobs a mount sees), and preloading a container or subdirectory into the cache at mount.
- On Kubernetes, the CSI driver provides BlobFuse as persistent storage (read-write or read-only).

## Verify
- [ ] Create a directory and a file under the mount (`mkdir test; echo "hello world" > test/blob.txt`) and see the blob in the container.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages blobfuse2-what-is and blobfuse2-how-to-deploy (read in full) and the GitHub repo page for Azure/azure-storage-fuse. Removed unconfirmed claims: apt install line, the config.yaml example and its numbers, managed identity auth key names, role requirements, fstab/systemd line, and locking, hard link and directory-rename specifics.
