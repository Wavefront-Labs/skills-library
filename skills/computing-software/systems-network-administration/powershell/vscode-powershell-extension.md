---
id: computing-software.systems-network-administration.powershell.vscode-powershell-extension
name: vscode-powershell-extension
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-environment, vscode-powershell, debugging, launch-json, compiled-cmdlets, session-menu]
level: practitioner
status: docs-checked
description: "Set up VS Code for PowerShell: install the extension, choose the PowerShell session, add exe paths, set encoding, create launch.json, and debug compiled cmdlets."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/dev-cross-plat/vscode/using-vscode
  - https://learn.microsoft.com/en-us/powershell/scripting/dev-cross-plat/vscode/using-vscode-for-debugging-compiled-cmdlets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VS Code PowerShell extension

VS Code with the Microsoft PowerShell extension is the recommended editor for PowerShell scripts. Supported: PowerShell 7.2 and later
(Windows, macOS, Linux) and Windows PowerShell 5.1 (Windows only, with .NET Framework 4.8). The Windows PowerShell ISE only works with 5.1 and older
and is no longer in active feature development, though it stays supported for security and high-priority fixes.

## Install
Quick Open (Ctrl+P / Cmd+P), type `ext install powershell`, pick the Microsoft extension, Install, then Reload if prompted.

If "Language server startup failed" appears because execution policy is set by Group Policy, approve PowerShell Editor Services manually:
```powershell
Import-Module $HOME\.vscode\extensions\ms-vscode.powershell*\modules\PowerShellEditorServices\PowerShellEditorServices.psd1
```
and answer `A` to the untrusted-publisher prompt.

## Choose the PowerShell version
Command Palette > **PowerShell: Show Session Menu** (also the `{}` status-bar icon, which can be pinned to show the version number).
Add installs the menu does not find with the object setting (key = menu name, value = absolute exe path), and set the default by that key:
```json
{
  "powershell.powerShellAdditionalExePaths": { "Built PowerShell": "<path>/pwsh.exe" },
  "powershell.powerShellDefaultVersion": "Built PowerShell"
}
```
Restart VS Code or run `Developer: Reload Window` afterwards. Before extension 2022.5.0 the setting was a list of `exePath` / `versionName` objects; convert old values.

## Encoding settings the page suggests
```json
{ "[powershell]": { "files.encoding": "utf8bom", "files.autoGuessEncoding": true } }
```
Other suggested global settings: `editor.renderWhitespace: all`, `editor.renderControlCharacters: true`, `files.trimTrailingWhitespace: true`.
Use `[<language-name>]` blocks to limit settings to one language.

## Debug scripts
- No workspace (VS Code 1.9+): File > Open File, F9 to set a breakpoint, F5 to debug.
- Workspace: open a folder, Debug view (Ctrl+Shift+D), "create a launch.json file", choose **PowerShell**, then pick **Launch Current File**, **Launch Script**,
  **Interactive Session** or **Attach** (to a running PowerShell host process). The file is `.vscode/launch.json` and usually committed.
  Generated entries use `"type": "PowerShell"` with `"request": "launch"` or `"attach"` (`processId: ${command.PickPSHostProcess}`, `runspaceId: 1`).
- Choose the configuration in the Debug toolbar drop-down.

## Debug compiled C# cmdlets
1. Install the C# extension. Create `tasks.json` from the **.NET Core** template (Configure Default Build Task). If the build says "Project file doesn't exist", add the explicit
   project path (`${workspaceFolder}/myModule`) after `build` in `args`.
2. Add a `launch.json` entry of `"type": "coreclr"`, `"program": "pwsh"`, `"preLaunchTask": "build"`, `"console": "integratedTerminal"`, and
   `"args": ["-NoExit","-NoProfile","-Command","Import-Module ${workspaceFolder}/myModule/bin/Debug/netstandard2.0/myModule.dll"]`.
   Use the manifest path if you have a `.psd1`.
3. For Windows PowerShell make a second entry with `"type": "clr"` and `"program": "powershell"`.
4. Set a breakpoint, press F5, run the cmdlet in the integrated terminal. If it does not stop and the Debug Console says "Skipped loading symbols ... Just My Code",
   add `"justMyCode": false`.
5. The imported DLL is locked while the terminal session lives; close it (Shift+F5 ends debugging) before rebuilding, or you get "Could not copy ... .dll".

## Checked
Method: 2026-11-08, read both cited learn.microsoft.com pages in full (PowerShell-Docs markdown). Rewritten to what they state. Removed unsupported claims from the earlier draft: F8 selection run, PSScriptAnalyzer settings file and `codeFormatting` presets, `psedit` over remoting, the extension-terminal behaviour notes and the "Restart Session" advice, and the setting value `"PowerShell (x64)"`. Not executed.
