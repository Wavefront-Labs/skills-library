---
id: computing-software.software-engineering.csharp-dotnet.interpolated-string-handlers
name: interpolated-string-handlers
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-strings-text, interpolated-string-handler, logging, performance, short-circuit]
level: advanced
status: docs-checked
description: "Write a custom C# interpolated string handler: required members, InterpolatedStringHandlerArgument, bool-returning Append short-circuit, overload preference, ref struct limits."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/performance/interpolated-string-handler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpolated string handlers

Without a custom handler, an interpolated string is processed like `string.Format`: each placeholder is formatted as text and the parts are concatenated. A custom handler lets a method know how the string will be used (for example a logger whose level is off) and skip the work. `DefaultInterpolatedStringHandler` ships with .NET 6 and has nine `AppendFormatted` overloads you can use as a reference.

## Required shape
A handler type must have:
- `InterpolatedStringHandlerAttribute` applied to the type;
- a constructor with two `int` parameters, `literalLength` and `formattedCount` (more parameters are allowed);
- `public void AppendLiteral(string s)`;
- a generic `public void AppendFormatted<T>(T t)`.
```csharp
[InterpolatedStringHandler]
public struct LogHandler {
    private readonly StringBuilder _sb;
    private readonly bool _enabled;
    public LogHandler(int literalLength, int formattedCount, Logger logger, LogLevel level) {
        _enabled = logger.IsEnabled(level);
        _sb = new StringBuilder(literalLength);
    }
    public void AppendLiteral(string s) { if (_enabled) _sb.Append(s); }
    public void AppendFormatted<T>(T t) { if (_enabled) _sb.Append(t?.ToString()); }
    public override string ToString() => _sb.ToString();
}

public void LogMessage(LogLevel level, [InterpolatedStringHandlerArgument("", nameof(level))] LogHandler message) { ... }
```
- `InterpolatedStringHandlerArgument` maps arguments of the public method to the extra constructor parameters after `literalLength` and `formattedCount`; the empty string `""` is the receiver (`this`). An empty list behaves as if the attribute were omitted.
- The compiler constructs the handler, calls `AppendLiteral`/`AppendFormatted` per part, then passes the handler to your method. When the argument is an interpolated string, it prefers a method with a handler parameter over a `string` parameter; a plain `string` argument still calls the `string` overload.
- A constant interpolated string (no placeholders) uses target type `string`, so custom handlers are bypassed.

## Short-circuiting
Change the `Append` methods to return `bool` (all of them, or you get a compile error). Returning `false` stops processing the rest of the interpolated expression, so later placeholder expressions are not evaluated; `true` continues. Use it to stop when the result is unused or a fixed buffer is full.

## More overloads
Add an `AppendFormatted` overload whose type argument is constrained to `IFormattable` to support format strings such as `{time:t}`, or overloads for specific types (the runtime does this for `Span<T>`), or an `int` parameter for alignment. The compiler picks the best overload.

## ref struct caution
Microsoft: use `ref struct` handlers only if absolutely necessary. They must live on the stack and do not work if a placeholder contains `await`.

## Verify
A test with a counting side-effect inside a placeholder shows whether it ran when the handler is disabled and short-circuits.

## Checked
2026-11-03. Confirmed against the dotnet/docs tutorial "Write a custom string interpolation handler". Removed because not found there: the `out bool isEnabled` constructor skip, `Debug.Assert`, `StringBuilder` and `MemoryExtensions.TryWrite` handler examples, `CompositeFormat`, ILogger behaviour with interpolated strings, the culture remark, and the claim that custom-handler expressions are always lazy (only short-circuiting stops them).
Method: documentation only; no commands were run.
