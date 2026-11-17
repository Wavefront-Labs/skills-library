---
id: computing-software.systems-network-administration.linux.scp-sftp-and-rsync-over-ssh
name: scp-sftp-and-rsync-over-ssh
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, openssh, scp, sftp-client, rsync, file-transfer, sftp-batch, resume-transfer, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Move files over SSH with the right tool: scp (now SFTP-based) quirks, interactive and batch sftp, rsync -e ssh for resumable/incremental copies, bandwidth limits and permissions."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/scp.1
  - https://github.com/openssh/openssh-portable/blob/master/sftp.1
  - https://github.com/RsyncProject/rsync/blob/master/rsync.1.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scp, sftp and rsync over SSH

**Goal:** copy files between hosts correctly (permissions, symlinks, big trees, flaky links)
using the tool that fits.

## 1. scp — quick one-offs
```bash
scp file.tgz alice@web01:/tmp/
scp -r -p conf/ web01:/etc/app/          # -p keeps times/modes; -r recursive
scp -3 web01:/data/x.sql db01:/tmp/      # remote→remote through the local host (the default mode)
scp -J bastion file db1:/tmp/            # through a jump host
scp -l 8000 big.iso host:                # limit to 8000 Kbit/s
```
Current OpenSSH scp uses the SFTP protocol for data transfer; `-O` forces the legacy SCP protocol, which may be needed
for servers without SFTP or for particular wildcard patterns.

## 2. sftp — interactive or scripted
```bash
sftp alice@files01
sftp> cd /upload; lcd ~/out; put -r report/; get -a big.iso   # -a resumes a partial download
sftp> ls -l; chmod 640 file; df -h; bye
sftp -b batch.txt alice@files01         # non-interactive; aborts if a command fails (a leading "-" on a command ignores its error)
sftp -P 2222 -i ~/.ssh/key host
```
Works against SFTP-only accounts (`ForceCommand internal-sftp`, chroot) where scp/rsync don't.

## 3. rsync over SSH — anything big, repeated, or fragile
```bash
rsync -aHAXv --progress /srv/data/ backup01:/backup/data/         # a=archive; H hardlinks, A ACLs, X xattrs
rsync -a --partial --append-verify bigfile host:/dst/              # resume interrupted large files
rsync -a --delete --dry-run src/ host:/dst/                         # preview deletions — then drop --dry-run
rsync -az -e 'ssh -p 2222 -i ~/.ssh/backup' src/ host:/dst/
rsync -a --bwlimit=20m src/ host:/dst/
rsync -a --info=progress2 --no-inc-recursive src/ host:/dst/      # overall progress
```
Trailing slash matters: `src/` copies contents, `src` copies the directory itself.
Needs rsync installed on both ends. Ownership is preserved only when the receiver runs as root.

## 4. Choosing
| Need | Tool |
|---|---|
| One file, now | scp |
| SFTP-only server, partner upload | sftp (batch) |
| Large trees, repeat syncs, resume, deletes | rsync |
| Very fast LAN bulk copy | rsync with `-W` (whole file), or tar over ssh: `tar cf - dir | ssh h 'tar xf - -C /dst'` |

## Gotchas
- `rsync --delete` with the wrong trailing slash or destination wipes data — always dry-run first.
- rsync needs `-A` and `-X` to preserve ACLs and extended attributes.
- Host key prompts break scripted transfers — manage known_hosts (BatchMode yes to fail fast).

## Verify
- [ ] Checksums match after transfer (`sha256sum` both ends or `rsync -c --dry-run` shows nothing to do).
- [ ] Permissions/ownership on the destination are as required.

## Checked
Checked 2026-10-25 against OpenSSH portable scp.1 and sftp.1 and the rsync man page source (RsyncProject/rsync master).
Confirmed: scp `-3`, `-J`, `-l` (Kbit/s), `-O`, `-p`, SFTP being scp's default transfer protocol; sftp `-b`, `-P`, `-i`, `get -a`, `df`, `chmod`; rsync `-a`, `-H`, `-A`, `-X`, `--partial`, `--append-verify`, `--dry-run`, `-z`, `--bwlimit`, `--info=progress2`, `--no-inc-recursive`, `-W`, `--rsh`, trailing-slash semantics, and ownership preserved only for the super-user.
Removed as unconfirmed: the OpenSSH 9.0 version gate and the statements about scp resume and symlink handling. The sftp batch-error prefix wording reflects the manual's description of batch mode.

Method: documentation only; no commands were run.
