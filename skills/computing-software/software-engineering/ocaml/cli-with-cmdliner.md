---
id: computing-software.software-engineering.ocaml.cli-with-cmdliner
name: cli-with-cmdliner
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, cmdliner, cli-arguments, command-line-parsing]
level: practitioner
status: docs-checked
description: "Define flags, options, positional args and subcommands with Cmdliner; get --help man pages and --version for free."
sources: ["https://erratique.ch/software/cmdliner", "https://erratique.ch/software/cmdliner/doc/Cmdliner/Cmd/index.html", "https://erratique.ch/software/cmdliner/doc/Cmdliner/Arg/index.html", "https://erratique.ch/software/cmdliner/doc/cli.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cmdliner

```ocaml
(* dune: (libraries cmdliner) *)
open Cmdliner
let name = Arg.(value & opt string "world" & info ["n"; "name"] ~docv:"NAME" ~doc:"Who to greet.")
let loud = Arg.(value & flag & info ["l"; "loud"] ~doc:"Shout.")
let file = Arg.(required & pos 0 (some file) None & info [] ~docv:"FILE")
let run name loud = print_endline ((if loud then String.uppercase_ascii else Fun.id) ("hello " ^ name)); 0
let cmd = Cmd.v (Cmd.info "greet" ~version:"0.1" ~doc:"Greet") Term.(const run $ name $ loud)
let () = exit (Cmd.eval' cmd)
```

## Notes
- Cmdliner defines declarative command lines, handles syntax errors, help, completion and man pages, supports single or multi-command programs, and has no dependencies.
- `Cmd.v` is documented as an old name for `Cmd.make`, which is preferred; both take a `Cmd.info` and a `Term.t`.
- `Cmd.info ~version` gives an automatic `--version`, only for the main command; `~doc` is the one-line description used in the man page NAME section.
- `Arg.opt conv default info`, `Arg.flag info`, `Arg.pos n conv default info` (zero-based); `required` is meant for use with `some`; `Arg.file` checks the file exists (`-` is accepted).
- In `info`, a one-character name is a short option (`-n`), a longer one a long option (`--name`); the name list must be empty for positional args.
- `Cmd.group info ?default cmds` builds subcommands; without `default`, omitting the subcommand is an error.
- `Cmd.eval` returns the ok exit code when the term gives `()`; `Cmd.eval'` returns the integer your term yields. Parse errors give `Exit.cli_error`, uncaught exceptions `Exit.internal_error` (default `~catch:true`).
- `--help` renders the man page; `--help=groff` gives other formats.

## Self-check
- [ ] `./greet --help` shows documented options.

## Checked
Checked 2026-11-08 against the Cmdliner home, Cmd, Arg and command line syntax pages. Removed: the numeric exit codes 0/123/124/125 (the docs give only symbolic names), the "1.1+" version claim and "Term.eval deprecated" remark, how to write an Arg.conv, and the stdlib Arg comparison. Corrected: Cmd.v is described as an old name for make. Unchanged: the example code, whose Arg/Cmd usage matches the signatures; it was not compiled.

Method: documentation only; no commands were run.
