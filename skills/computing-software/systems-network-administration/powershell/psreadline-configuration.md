---
id: computing-software.systems-network-administration.powershell.psreadline-configuration
name: psreadline-configuration
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-environment, psreadline, set-psreadlineoption, predictive-intellisense, command-history, key-handlers, history-security]
level: practitioner
status: gated
description: "Configure PSReadLine for admin work: predictive IntelliSense, history search, key handlers, edit modes, and keeping passwords out of the persistent history file."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/psreadline/about/about_psreadline
  - https://learn.microsoft.com/en-us/powershell/module/psreadline/set-psreadlineoption
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/using-predictors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSReadLine configuration

PSReadLine provides command-line editing, syntax colouring, history and prediction in the
console. PS 7.6.7 ships 2.4.5; Windows PowerShell 5.1.26100 ships 2.0.0 and should be updated:
`Install-PSResource PSReadLine -Scope CurrentUser` (run from a non-PSReadLine host such as
`powershell -NoProfile -NonInteractive` if the module is in use) (gated: unconfirmed, source is paywalled or blocked). The install was not run (it writes into the user module folder).

## Recommended profile block
```powershell
if (Get-Module -ListAvailable PSReadLine | Where-Object Version -ge '2.2') {
  Set-PSReadLineOption -PredictionSource HistoryAndPlugin -PredictionViewStyle ListView
}
Set-PSReadLineOption -EditMode Windows -HistorySearchCursorMovesToEnd -BellStyle None
Set-PSReadLineOption -MaximumHistoryCount 10000
Set-PSReadLineKeyHandler -Key UpArrow   -Function HistorySearchBackward    # type prefix, then Up
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
Set-PSReadLineKeyHandler -Key Tab       -Function MenuComplete
```
- `PredictionSource` values are `None`, `History`, `Plugin`, `HistoryAndPlugin` (enum names read from 2.4.5); the docs say `Plugin` and
  `HistoryAndPlugin` were added in PSReadLine 2.2.0, and plugin predictors include `Az.Tools.Predictor` and `CompletionPredictor`
  (both exist on the PowerShell Gallery). Windows PowerShell 5.1's 2.0.0 has no `PredictionSource` parameter at all, so the guarded
  block in the profile example is needed there. The PS 7.2+ requirement for plugins (gated: unconfirmed, source is paywalled or blocked). Prediction only works in a console with virtual-terminal
  support: `Set-PSReadLineOption -PredictionSource ...` failed in this non-interactive run.
- `F2` toggles InlineView/ListView (bound to `SwitchPredictionView`). `Ctrl+r` is `ReverseSearchHistory`; `Ctrl+Space` is
  `MenuComplete`; `Alt+.` is `YankLastArg` (inserts the last argument of the previous command).
- `Get-PSReadLineKeyHandler` lists every binding; its switches are `-Bound` and `-Unbound` (use `-Unbound` for functions with no key).
- Emacs or Vi users: `-EditMode Emacs|Vi`.

## History file: where and what
```powershell
(Get-PSReadLineOption).HistorySavePath     # %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```
- Shared across sessions by default (`-HistorySaveStyle SaveIncrementally`).
- It is **plain text** and readable by anyone with access to the profile; attackers and
  incident responders both read it.
- Current PSReadLine versions skip saving lines that look sensitive by default (the source's pattern is
  `password|asplaintext|token|apikey|secret`, with special handling of `-AsPlainText`); extend with `-AddToHistoryHandler`
  (return `MemoryAndFile`, `MemoryOnly`, `SkipAdding`, or `$true`/`$false`; the block below was accepted by `Set-PSReadLineOption`
  in 5.1 and 7, but its effect on a real history file needs an interactive session):
```powershell
Set-PSReadLineOption -AddToHistoryHandler {
  param([string]$line)
  if ($line -match 'ConvertTo-SecureString|-Password\s|Bearer\s') { return 'MemoryOnly' }
  return 'MemoryAndFile'
}
```
- `-HistorySaveStyle SaveNothing` on shared jump hosts; clear with
  `Remove-Item (Get-PSReadLineOption).HistorySavePath` after an accidental paste.

## Colours and accessibility
`Set-PSReadLineOption -Colors @{ Command = 'Cyan'; Parameter = 'DarkCyan'; InlinePrediction = '#8A8A8A' }`
fixes low-contrast predictions on dark themes. It ran in 7.6.7; the `InlinePrediction` key threw in 5.1's PSReadLine 2.0.0 (which has no
prediction), so drop that key there.

## Verify
- [ ] Typing a prefix and pressing Up recalls matching history.
- [ ] A test line containing `-Password x` does not appear in the history file.

## Checked
Ran on PowerShell 7.6.7 (PSReadLine 2.4.5) and Windows PowerShell 5.1.26100 (2.0.0): `Get-PSReadLineOption` fields and history path
(`%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`, `SaveIncrementally`), every `Set-PSReadLineOption` and
`Set-PSReadLineKeyHandler` line of the profile block (accepted; prediction refused without VT support), enum names, key-handler
bindings, the `-Colors` hashtable, and `Get-PSReadLineKeyHandler` switches. The sensitive-history regular expression was read from
PSReadLine's `History.cs` on GitHub; `-AddToHistoryHandler` return values, `PredictionSource` versions and the plugin names from the
Set-PSReadLineOption page and the PowerShell Gallery. Interactive behaviour (Up-arrow prefix search, what lands in the history file) was not run.
