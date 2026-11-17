---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-mvvm-relaycommand
name: wpf-mvvm-relaycommand
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-mvvm-relaycommand, wpf-mvvm, wpf, mvvm, communitytoolkit, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Expose commands with [RelayCommand], async methods, CanExecute and NotifyCanExecuteChangedFor."
sources:
  - https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/generators/relaycommand
  - https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/asyncrelaycommand
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CommunityToolkit.Mvvm RelayCommand

**Goal:** ICommand without hand-written classes.

```csharp
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    private bool isDirty;

    [RelayCommand(CanExecute = nameof(CanSave))]
    private async Task SaveAsync(CancellationToken ct) { await _repo.SaveAsync(ct); IsDirty = false; }
    private bool CanSave() => IsDirty;
}
// XAML: <Button Command="{Binding SaveCommand}" Content="Save"/>
```

**Gotcha:** The command does not know when `CanExecute` changes: call `NotifyCanExecuteChanged` (or use `NotifyCanExecuteChangedFor`). By default an async command signals disabled while an execution is pending (`AllowConcurrentExecutions` is false), and a method taking a `CancellationToken` gets a token that is cancelled if a concurrent execution is requested. Exceptions are awaited and rethrown by default (they can crash the app); only with `FlowExceptionsToTaskScheduler` do they surface through `ExecutionTask`.

## Verify
- The Save button disables when not dirty and while a save is running.

## Checked

2026-11-03. Confirmed in the MVVM Toolkit RelayCommand generator and AsyncRelayCommand pages: `CanExecute = nameof(...)`, `NotifyCanExecuteChangedFor`, CancellationToken propagation, `AllowConcurrentExecutions` default false, default await-and-rethrow exception handling, `FlowExceptionsToTaskScheduler` and `ExecutionTask`. Fixed an error: the draft said exceptions in async commands surface through `ExecutionTask` by default; the docs say they are rethrown by default.

Method: documentation only; no commands were run.
