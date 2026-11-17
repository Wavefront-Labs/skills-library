---
id: computing-software.software-engineering.csharp-dotnet.mvvm-community-toolkit-and-wpf-data-binding
name: mvvm-community-toolkit-and-wpf-data-binding
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-desktop-ui, mvvm-community-toolkit, wpf-data-binding, inotifypropertychanged, relaycommand, observableproperty]
level: practitioner
status: draft
description: "Build MVVM desktop UIs for WPF and MAUI with CommunityToolkit.Mvvm source generators (ObservableProperty, RelayCommand), WPF binding modes, converters, validation and threading rules."
sources: ["https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/", "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/", "https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/generators/observableproperty"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MVVM Toolkit and WPF data binding

```csharp
public partial class CustomerViewModel : ObservableValidator
{
    [ObservableProperty, NotifyPropertyChangedFor(nameof(Display)), NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    [NotifyDataErrorInfo, Required, MinLength(2)]
    private string _name = "";                                     // generates public string Name with change notification

    public string Display => $"Customer: {Name}";
    public ObservableCollection<Order> Orders { get; } = new();

    [RelayCommand(CanExecute = nameof(CanSave))]
    private async Task SaveAsync(CancellationToken ct) { ValidateAllProperties(); if (!HasErrors) await _repo.SaveAsync(this, ct); }
    private bool CanSave() => !string.IsNullOrWhiteSpace(Name);
}
```
Packages: `CommunityToolkit.Mvvm` (source generators; class must be `partial`; C# 14 `field` keyword/partial properties are the newer style). `[RelayCommand]` on async methods creates `AsyncRelayCommand` with cancellation and `IsRunning`. `WeakReferenceMessenger` decouples view models (`Messenger.Send/Register`), and `Ioc.Default` or Microsoft.Extensions.DependencyInjection supplies services.

```xml
<TextBox Text="{Binding Name, UpdateSourceTrigger=PropertyChanged, ValidatesOnNotifyDataErrors=True}" />
<Button Content="Save" Command="{Binding SaveCommand}" />
<ItemsControl ItemsSource="{Binding Orders}"><ItemsControl.ItemTemplate><DataTemplate>
    <TextBlock Text="{Binding Total, StringFormat=C, Converter={StaticResource RedIfNegative}}" /></DataTemplate></ItemsControl.ItemTemplate></ItemsControl>
```
## Binding rules
- Modes: `OneWay` (default for most), `TwoWay` (TextBox.Text default), `OneTime`, `OneWayToSource`. `UpdateSourceTrigger` default for Text is `LostFocus`.
- Set `DataContext` at the root; use `x:DataType` with compiled bindings in MAUI/WinUI (`{x:Bind}` / `x:DataType`) for speed and compile-time checks.
- Collections: `ObservableCollection<T>` notifies add/remove, not property changes inside items; items need `INotifyPropertyChanged`. Bulk updates raise many events: replace the collection or use a range-capable collection.
- UI thread: only touch UI-bound collections on the dispatcher (`Application.Current.Dispatcher.InvokeAsync`, MAUI `MainThread.InvokeOnMainThreadAsync`); property change from background threads is marshalled for scalars but not for collections.
- Binding errors are silent: watch the Output window ("System.Windows.Data Error") or set `PresentationTraceSources.TraceLevel=High`.
- Avoid code-behind logic; keep view models UI-framework agnostic for unit testing.

## Gotchas
- Memory leaks: strong event subscriptions or static binding sources keep views alive; use weak messenger.
- `async void` commands swallow exceptions; use `AsyncRelayCommand` and `FlowExceptionsToTaskScheduler`.
- Virtualisation breaks when an `ItemsControl` sits in a `ScrollViewer`; use `ListBox`/`DataGrid` with `VirtualizingPanel`.

## Verify
Unit-test the view model with no UI (property change events raised, command CanExecute transitions); run the app with trace output and confirm zero binding errors.
