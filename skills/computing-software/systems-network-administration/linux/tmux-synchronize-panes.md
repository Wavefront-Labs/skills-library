---
id: computing-software.systems-network-administration.linux.tmux-synchronize-panes
name: tmux-synchronize-panes
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tmux, synchronize-panes, multi-host-ssh, xpanes, panes, cluster-ssh]
level: intro
status: docs-checked
description: "Type into many panes at once with tmux synchronize-panes for multi-host SSH work, a script to open one pane per host, toggling safely, and alternatives like xpanes/clusterssh."
sources:
  - https://github.com/tmux/tmux/blob/master/tmux.1
  - https://github.com/greymd/tmux-xpanes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tmux synchronize-panes

**Use:** quick parallel commands on a handful of hosts where you want to watch each output live
(tail logs on 4 web nodes, compare `ss -s` across a cluster). For anything repeatable, use Ansible.

## Open one pane per host
```bash
hosts=(web1 web2 web3 web4)
tmux new-session -d -s multi "ssh ${hosts[0]}"
for h in "${hosts[@]:1}"; do tmux split-window -t multi "ssh $h"; tmux select-layout -t multi tiled; done
tmux set-window-option -t multi synchronize-panes on
tmux attach -t multi
```
Or with xpanes: `xpanes -c 'ssh {}' web1 web2 web3 web4` (synchronize-panes is on by default; `-d` starts desynchronised).

## Toggle
`prefix :setw synchronize-panes` toggles the option (`on` or `off` can be given explicitly). Bind it and show the state in the pane border using the `pane_synchronized` format variable:
```
bind S setw synchronize-panes \; display "sync #{?pane_synchronized,ON,OFF}"
set -g pane-border-format "#{?pane_synchronized,#[bg=red] SYNC ,}#P #{pane_current_command}"
set -g pane-border-status top
```

## Safety
- Hosts differ (paths, prompts asking for passwords, one host already at a different directory) — typed
  input goes everywhere regardless. Check each pane before pressing Enter on destructive commands.
- Turn sync OFF before editing files in an interactive editor, since the panes' states diverge quickly.
- Password prompts: use keys or an agent so all panes behave the same.

## Verify
- [ ] Border/status shows SYNC state; `hostname` typed once prints a different name in each pane.

## Checked
Checked 2026-10-25 against the tmux manual page source and CHANGES file (tmux/tmux master, latest release 3.8 of 2026-09-09). Confirmed: `synchronize-panes [on|off]`, `select-layout tiled`, `split-window`, `pane-border-format`, `pane-border-status`, the `pane_synchronized` format variable, and from the tmux-xpanes README (greymd/tmux-xpanes, pushed 2026-05-05) the `-c` command with `{}` placeholder and `-d/--desync`. Removed unconfirmed claims: vim keystroke-desync detail was reworded as general advice.

Method: documentation only; no commands were run.
