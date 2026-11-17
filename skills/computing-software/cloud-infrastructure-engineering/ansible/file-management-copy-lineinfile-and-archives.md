---
id: computing-software.cloud-infrastructure-engineering.ansible.file-management-copy-lineinfile-and-archives
name: file-management-copy-lineinfile-and-archives
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, file-management, copy, fetch, file-module, lineinfile, blockinfile, replace, unarchive, archive, archives, get-url, stat, find, synchronize, rsync, slurp, tempfile, permissions, selinux-context, checksum, remote-src, ini-file, xml-module, files-vs-templates]
level: practitioner
status: docs-checked
description: "Pick the right Ansible file module: copy/template vs lineinfile/blockinfile/replace, unarchive/get_url with checksums, synchronize for trees, stat/find/slurp for reads, permission rules."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/lineinfile_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/lineinfile.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/blockinfile.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/copy.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/unarchive.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/get_url.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/find.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/file.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/fetch.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/files.py", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/synchronize.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/archive.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File management: copy, lineinfile and archives

**Goal:** files on hosts match the repo byte-for-byte where Ansible owns them, are
edited surgically where it does not, and transfers are checksummed and idempotent.

## 1. Decide: own the file or edit a line?
| Situation | Module |
|---|---|
| Ansible owns the whole file, static | `copy` (src from `files/`, or `content:`) |
| Owns it, varies per host | `template` |
| Someone else owns it, one setting | `lineinfile` (regexp + line) |
| A contiguous managed section | `blockinfile` (marker comments) |
| Many occurrences / regex rewrite | `replace` |
| INI / key=value | `community.general.ini_file` |
| XML / JSON | `community.general.xml`, or render JSON via `template` + `to_nice_json` |
| Whole directory tree | `ansible.posix.synchronize` (rsync) or `copy` with `src: dir/` (the docs say recursive copy does not scale past hundreds of files) |
Prefer owning the file: `lineinfile` replaces only the last match of `regexp` and needs a separate
`state: absent` task to remove a line.

## 2. Edits that stay idempotent
```yaml
- ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?PasswordAuthentication\s'
    line: PasswordAuthentication no
    validate: /usr/sbin/sshd -t -f %s
  notify: restart sshd
- ansible.builtin.blockinfile:
    path: /etc/hosts
    marker: "# {mark} ANSIBLE MANAGED cluster"
    block: |
      {% for h in groups['cluster'] %}{{ hostvars[h].ansible_host }} {{ h }}
      {% endfor %}
- ansible.builtin.replace: {path: /etc/default/grub, regexp: 'quiet splash', replace: 'quiet'}
```
The `regexp` must match the line **after** the edit too, or every run inserts another copy.
`insertafter: EOF` is the default (also used when the `insertafter` regexp has no match); `insertbefore`
and `firstmatch: true` control placement. `state: absent` + `regexp` removes lines. `backrefs: true` lets `line`
reuse capture groups, ignores `insertbefore`/`insertafter`, and leaves the file unchanged when the regexp does not match.

## 3. Transfers
```yaml
- ansible.builtin.copy: {src: app.conf, dest: /etc/app/app.conf, owner: root, group: app, mode: "0640", backup: true}
- ansible.builtin.copy: {src: /tmp/on-remote.conf, dest: /etc/x.conf, remote_src: true}   # source already on the target
- ansible.builtin.get_url:
    url: https://dl.example/app-1.2.tgz
    dest: /opt/dist/app-1.2.tgz
    checksum: sha256:<HEX>           # or sha256:https://dl.example/app-1.2.tgz.sha256
    mode: "0644"
- ansible.builtin.unarchive:
    src: /opt/dist/app-1.2.tgz      # remote_src: true when the file is already on the host
    remote_src: true
    dest: /opt/app/releases/1.2
    creates: /opt/app/releases/1.2/bin/app     # idempotence marker
    extra_opts: [--strip-components=1]
    owner: app
- ansible.posix.synchronize: {src: site/, dest: /var/www/site/, delete: true, rsync_opts: ["--exclude=.git"]}
- ansible.builtin.fetch: {src: /var/log/app.log, dest: "logs/{{ inventory_hostname }}/", flat: false}
- community.general.archive: {path: /var/lib/app, dest: /backup/app.tgz, format: gz}
```
- `copy` has `force: true` by default (replace when contents differ); `src: dir/` (trailing slash) copies the directory contents, without the slash it copies the directory itself.
- `unarchive` uses gtar `--diff` to decide whether anything changed and, if that is not supported, always unpacks; `creates` skips the step when the given path (below `dest`) exists, and `list_files: true` returns the archive contents.
- `synchronize` modes are `push` (default) and `pull`; `delete: true` requires `recursive: true`; `rsync_opts` takes a list and `rsync_path` sets the remote rsync command.
- `get_url` verifies the downloaded file against `checksum` (`<algorithm>:<digest or URL>`); `force: false` (default) downloads only when `dest` does not exist.

## 4. Reads and existence
```yaml
- ansible.builtin.stat: {path: /etc/app/app.conf, checksum_algorithm: sha256}
  register: st
- ansible.builtin.slurp: {src: /etc/app/token}
  register: tok           # tok.content | b64decode
- ansible.builtin.find: {paths: /var/log/app, patterns: "*.log", age: 30d, recurse: true}
  register: old
- ansible.builtin.file: {path: "{{ item.path }}", state: absent}
  loop: "{{ old.files }}"
```
`stat` for `when: st.stat.exists`, `st.stat.islnk`, `st.stat.mode`; `find` + `file` for cleanup (`age: 30d` selects files at least 30 days old by `mtime`, the default `age_stamp`); `tempfile` for scratch files.

## 5. Permissions and metadata
Quote octal `mode` values (`"0644"`) or use symbolic modes (`u=rw,g=r,o=r`); `file: state: directory` with
`recurse: true` applies attributes to directory contents; `state: link` creates symlinks (`force: true` also replaces
an existing destination file); `state: touch` with `modification_time: preserve` avoids changing the modification time;
`attributes`, `seuser`, `setype` and `selevel` are common file options; `community.general.sefcontext` manages SELinux file contexts.

## Gotchas
- `lineinfile` with `regexp` matching several lines replaces only the **last** match.
- `blockinfile` default marker is `# {mark} ANSIBLE MANAGED BLOCK`; give each task editing one file a unique `marker`.
- Be explicit about trailing newlines in `content:` (YAML `|` keeps one, `|-` strips it).
- Unquoted numbers without a documented octal form are read as decimal: quote `mode` values; a leading zero "works sometimes, but can fail in loops and some other circumstances" (module docs).
- `unarchive` requires `zipinfo` and `gtar`/`unzip` on the target, and `zstd` for `.tar.zst`.
- `fetch` appends `<hostname>/<path>` to `dest` unless `flat: true`; with `flat: true` and several hosts the files overwrite each other.

## Verify
- [ ] Second run: every file task `changed=0`, including `lineinfile`/`blockinfile`/`unarchive`.
- [ ] `--check --diff` on a `lineinfile` task shows a single-line diff, not an appended duplicate.

## Checked
Checked 2026-10-26 against ansible-core devel module sources and the `files` doc fragment (repository last commit 2026-10-23),
ansible.posix `synchronize.py` and community.general `archive.py`. Confirmed: lineinfile last-match, `insertafter` EOF default
and `backrefs` behaviour, blockinfile default marker, `unarchive` requirements and gtar `--diff` change detection, `creates`,
`get_url` checksum format and `force` default, `find` `age`/`age_stamp`, `file` `recurse`/`force`/`modification_time`,
`fetch` `flat`, `synchronize` options, mode quoting guidance, existence of `community.general` ini_file, xml, sefcontext, archive.
Removed or corrected: the claim that unarchive without `creates` re-extracts and reports changed every run (docs say it uses
gtar `--diff`), the "decimal 644 shows -w----r-T" example, synchronize SSH-quirk advice, the Jinja trailing-newline claim,
and the checksum/ls verification command.
Method: documentation only; no commands were run.
