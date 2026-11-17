---
id: computing-software.systems-network-administration.bash.ps1-prompt-customisation
name: ps1-prompt-customisation
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, ps1, prompt, prompt-command, prompt-escapes, colour-prompt, git-prompt, exit-status-prompt, root-prompt, terminal-title, ps2, shell-environment, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Build a bash PS1 that does not corrupt line editing: escapes, non-printing brackets around colours, PROMPT_COMMAND for exit status and git branch, and terminal titles."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Controlling-the-Prompt
  - https://github.com/git/git/blob/master/contrib/completion/git-prompt.sh
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PS1 — a prompt that tells you where you are and warns when you are root

**Goal:** show user@host:path, exit status and (optionally) git branch, in colour, without
the wrapped-line corruption that badly escaped prompts cause.

## 1. Escapes
`\u` user, `\h` host (short), `\H` FQDN, `\w` cwd (`~` abbreviated), `\W` basename,
`\$` `#` for root else `$`, `\t` time HH:MM:SS, `\d` date, `\j` jobs, `\!` history number,
`\n` newline, `\e` escape (ESC), `\[` `\]` enclose **non-printing** sequences.

```bash
PS1='\u@\h \w\$ '                                # the classic (Debian adds a colon after \h)
PS1='\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ '   # coloured, correctly bracketed
```
Every colour code **must** be inside `\[ \]`; otherwise bash miscounts the prompt width and
long commands wrap over the prompt or history recall leaves garbage.

## 2. Dynamic pieces via PROMPT_COMMAND
```bash
__prompt() {
    local rc=$?                                   # must be first
    local red='\[\e[31m\]' grn='\[\e[32m\]' blu='\[\e[34m\]' yel='\[\e[33m\]' rst='\[\e[0m\]'
    local status=""; (( rc )) && status="${red}[$rc]${rst} "
    local uc=$grn; (( EUID == 0 )) && uc=$red    # root glows red
    local git=""; command -v __git_ps1 >/dev/null && git=$(__git_ps1 ' (%s)')
    PS1="${status}${uc}\u@\h${rst}:${blu}\w${rst}${yel}${git}${rst}\\$ "
}
PROMPT_COMMAND=__prompt
```
- `$?` is clobbered by anything else you run — capture it on line one.
- `__git_ps1` comes from `git-prompt.sh` (`/usr/share/git-core/contrib/completion/` on RHEL,
  `/usr/lib/git-core/git-sh-prompt` on Debian); `GIT_PS1_SHOWDIRTYSTATE=1` adds `*`/`+`.
  On huge repos or network filesystems it can make every prompt slow — gate it with
  `GIT_PS1_SHOWDIRTYSTATE` unset or a timeout.
- Keep `PROMPT_COMMAND` cheap: no network, no `git fetch`. Measure with
  `time __prompt`.

## 3. Terminal title and extras
```bash
PS1='\[\e]0;\u@\h: \w\a\]'"$PS1"          # OSC 0 sets the window/tab title (inside \[ \])
PS1='\n'"$PS1"                             # blank line before each prompt
PS2='> '                                   # continuation; PS4 is for set -x
```
tmux/screen read the title; VTE terminals also want `PROMPT_COMMAND` to emit the cwd
(`/etc/profile.d/vte.sh` handles it — append, do not replace: `PROMPT_COMMAND="__prompt;$PROMPT_COMMAND"`).

## 4. Shell-specific and environment hints
```bash
[[ -n $SSH_CONNECTION ]] && hostcolor='\[\e[1;35m\]'     # remote shells in magenta
[[ -n $VIRTUAL_ENV ]] && venv="(${VIRTUAL_ENV##*/}) "
[[ -n $container ]] && tag='[ctr] '
```
Set root's prompt system-wide in `/etc/bashrc`/`/etc/bash.bashrc` so every admin sees a
red `#` — cheap insurance against `rm -rf` in the wrong shell.

## 5. Debugging
```bash
echo "$PS1" | cat -v          # see the raw escapes
PS1='\$ '                     # reset to minimal to test if the prompt causes wrapping issues
```

## Failure modes
- Long lines wrap onto the prompt / Ctrl-R draws garbage: missing `\[ \]`.
- Exit status always 0: `$?` read after another command in the function.
- Prompt slow in big git repos: dirty-state check; disable or use `git config bash.showDirtyState false` per repo.
- Colours bleed into command output: missing reset `\e[0m` at the end.
- `PROMPT_COMMAND` from `vte.sh` overwritten → terminal tabs no longer open in cwd.

## Verify
- [ ] Type a command longer than the terminal width, press Home/End — cursor lands correctly.
- [ ] `false` then Enter shows `[1]`; `sudo -i` shows a red `#` prompt.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; bash prompt section and git-prompt.sh fetched but not read claim by claim; distro paths and vte.sh not checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
