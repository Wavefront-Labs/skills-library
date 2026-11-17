---
id: computing-software.software-engineering.ruby.ruby-tracepoint-debugging
name: ruby-tracepoint-debugging
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, tracepoint-debugging, introspection]
level: advanced
status: docs-checked
description: "Trace Ruby execution with TracePoint: call/return/raise events, finding who raises or defines a method, scoped with target."
sources: ["https://docs.ruby-lang.org/en/master/TracePoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TracePoint

```ruby
calls = []
tp = TracePoint.new(:call, :return, :raise) do |t|
  calls << [t.event, t.defined_class, t.method_id, t.path, t.lineno]
  puts "raised #{t.raised_exception.inspect}" if t.event == :raise
end
tp.enable { run_scenario }          # block form: auto-disabled afterwards
tp.enable(target: method(:price))   # trace one method only (lower overhead)
```
Events: `:line`, `:class`, `:end`, `:call`, `:return`, `:c_call`, `:c_return`, `:raise`, `:rescue`, `:b_call`, `:b_return`, `:thread_begin`, `:thread_end`, `:fiber_switch`, `:script_compiled`. Accessors: `method_id`, `callee_id`, `defined_class`, `self`, `binding`, `return_value`, `parameters`, `path`, `lineno`.

Practical recipes:
```ruby
# who raises this error? (find origin of swallowed exceptions)
TracePoint.new(:raise) { |t| puts t.raised_exception.backtrace&.first(3) if t.raised_exception.is_a?(KeyError) }.enable
# where is a method defined? no tracing needed:
Foo.instance_method(:bar).source_location
```

## Gotchas
- Scope tracing with `target:` or the block form of `enable`, which (with no target) enables the trace only for the block and the current thread; `target:`, `target_line:` and `target_thread:` limit what is traced.
- While a TracePoint callback is running, other registered callbacks are not called, to avoid reentrance; `TracePoint.allow_reentry { }` permits it and the docs warn about infinite callback invocation.
- Accessors such as `raised_exception` work only for the matching events (otherwise `RuntimeError: 'raised_exception' not supported by this event`), and any accessor called outside the hook block raises `RuntimeError` ("access from outside").
- `return_value` is for `:return`, `:c_return` and `:b_return`; `raised_exception` is for `:raise` and `:rescue`.

Verify: trace a trivial method call and confirm the `:call` and `:return` events arrive with the right line numbers.

## Checked
2026-11-03. Confirmed against ruby/ruby `trace_point.rb` rdoc (event list, accessors, `enable` arguments and block behaviour, `allow_reentry`, RuntimeError cases) and `proc.c` (`source_location`). Removed: performance "orders of magnitude" claim, and YJIT interaction (not stated in the docs read).
Method: documentation only; no commands were run.
