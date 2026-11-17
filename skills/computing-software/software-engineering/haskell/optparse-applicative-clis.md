---
id: computing-software.software-engineering.haskell.optparse-applicative-clis
name: optparse-applicative-clis
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, optparse-applicative, cli, subcommands, option-parser, execparser, help-text, completions, process, optparse-applicative-clis, haskell-cli]
level: practitioner
status: docs-checked
description: "Build CLIs with optparse-applicative (Parser, switch, option, strArgument, hsubparser, execParser, customExecParser) and run subprocesses with the process package."
sources: ["https://hackage.haskell.org/package/optparse-applicative/docs/Options-Applicative.html", "https://hackage.haskell.org/package/process/docs/System-Process.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# optparse-applicative CLIs

**Goal:** typed argument parsing with generated --help. Package: `optparse-applicative`.

```haskell
import Options.Applicative

data Opts = Opts { verbose :: Bool, port :: Int, file :: FilePath, cmd :: Cmd }
data Cmd = Build | Clean String

optsP :: Parser Opts
optsP = Opts
  <$> switch (long "verbose" <> short 'v' <> help "chatty output")
  <*> option auto (long "port" <> metavar "N" <> value 8080 <> showDefault <> help "port")
  <*> strArgument (metavar "FILE")
  <*> hsubparser
        ( command "build" (info (pure Build) (progDesc "build it"))
       <> command "clean" (info (Clean <$> strArgument (metavar "TARGET")) (progDesc "clean")) )

main :: IO ()
main = do
  o <- execParser (info (optsP <**> helper) (fullDesc <> progDesc "my tool" <> header "mytool"))
  run o
```
`customExecParser (prefs showHelpOnError)` shows help after errors. The library also exports `completer` for custom shell completion and `footer` for extra help text.

## Subprocesses (package `process`)
```haskell
import System.Process
(code, out, err) <- readProcessWithExitCode "git" ["rev-parse", "HEAD"] ""
callProcess "make" ["-j4"]                  -- shorthand for callCreateProcess (proc cmd args)
withCreateProcess (proc "cmd" args) { std_out = CreatePipe } $ \_ (Just h) _ ph -> ...
```
`proc` takes the program and an argument list; `shell` takes one command string (`callCommand cmd` is `callCreateProcess (shell cmd)`), so prefer `proc` when any part of the command comes from input.

## Gotchas
- Parser is applicative: you cannot make later options depend on earlier ones; use subcommands.
- `execParser` handles parse failures and `--help` itself; use `renderFailure` or `execParserPure` if you need to handle them yourself.
- `readProcessWithExitCode` returns `(ExitCode, String, String)`: exit code, stdout, stderr.

## Self-check
- [ ] `--help` text is readable and examples are in `footer`.
- [ ] Bad input prints usage and exits non-zero.

## Checked
2026-11-03. Confirmed against the Haddock pages for `Options.Applicative` and `System.Process`: `switch`, `option`, `auto`, `strArgument`, `hsubparser`, `execParser`, `customExecParser`, `prefs`, `showHelpOnError`, `showDefault`, `fullDesc`, `progDesc`, `header`, `footer`, `helper`, `metavar`, `completer`, `readProcessWithExitCode`, `callProcess`, `withCreateProcess`, `proc`, `shell`, `CreatePipe`, `std_out`. Removed: the `--bash-completion-script` invocation and zsh/fish claims, the throws-on-non-zero claim, env defaults advice and OsPath advice (not on these pages).
Method: documentation only; no commands were run.
