---
id: computing-software.software-engineering.cpp.pimpl-idiom-and-compilation-firewalls
name: pimpl-idiom-and-compilation-firewalls
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, pimpl-idiom, compilation-firewall, abi-stability, unique-ptr, incomplete-types, build-times, cpp-library-design]
level: advanced
status: docs-checked
description: "Implement the pimpl idiom in modern C++ with unique_ptr: out-of-line special members for incomplete types, const propagation, ABI stability and when the indirection is worth it."
sources: ["https://en.cppreference.com/w/cpp/language/pimpl", "https://herbsutter.com/gotw/_100/", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-pimpl"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Pimpl idiom and compilation firewalls

**Goal:** hide a class's private members behind a pointer so headers stop leaking dependencies,
rebuilds shrink, and a shared library's ABI survives implementation changes.

## Header
```cpp
// widget.h
#pragma once
#include <memory>
#include <string_view>

class Widget {
public:
    explicit Widget(std::string_view name);
    ~Widget();                                   // declared here, DEFINED in .cpp
    Widget(Widget&&) noexcept;
    Widget& operator=(Widget&&) noexcept;
    Widget(const Widget&);                       // only if copy is wanted
    Widget& operator=(const Widget&);

    void draw() const;
private:
    struct Impl;                                 // forward declaration only
    std::unique_ptr<Impl> impl_;
};
```

## Source
```cpp
// widget.cpp
#include "widget.h"
#include "heavy/renderer.h"                      // dependencies stay here
struct Widget::Impl {
    std::string name;
    heavy::Renderer renderer;
    void draw() const { renderer.render(name); }
};
Widget::Widget(std::string_view n) : impl_(std::make_unique<Impl>(Impl{std::string(n), {}})) {}
Widget::~Widget() = default;                     // Impl is complete here
Widget::Widget(Widget&&) noexcept = default;
Widget& Widget::operator=(Widget&&) noexcept = default;
Widget::Widget(const Widget& o) : impl_(std::make_unique<Impl>(*o.impl_)) {}
Widget& Widget::operator=(const Widget& o) { *impl_ = *o.impl_; return *this; }
void Widget::draw() const { impl_->draw(); }
```

## The rule that breaks builds
`std::unique_ptr<Impl>`'s deleter needs `Impl` complete. If the destructor (or move assignment)
is implicitly defined in the header, every includer instantiates it with an incomplete type:
an incomplete-type compile error. Fix: **declare** destructor and
moves in the header, **define** them (even as `= default`) in the .cpp after `Impl` is defined.

## Details
- **Moved-from state**: `impl_` is null after a move; methods called on a moved-from object crash.
  Document "valid but unusable" or check `impl_`.
- **const propagation**: in a `const` method `impl_->mutate()` compiles because `unique_ptr::operator->`
  is const. Use `std::experimental::propagate_const<std::unique_ptr<Impl>>` where available, or
  route through `const Impl& impl() const`.
- `shared_ptr<Impl>` tolerates incomplete types in the destructor but gives shared (surprising)
  copy semantics; avoid unless you want that.
- Cost: one heap allocation per object and a pointer indirection per call; prevents inlining of
  member functions across the boundary. Do not pimpl small value types or hot inner-loop classes.

## When it pays
- Public headers of shared libraries: you can add/remove private members without breaking ABI
  (object size and layout unchanged).
- Classes whose private members drag in heavy or platform headers (windows.h, Qt, protobuf).
- Headers included by hundreds of translation units where a private change triggers huge rebuilds.
Alternatives: abstract interface + factory (`std::unique_ptr<IWidget> make_widget()`), or C++20
modules for build isolation without the runtime cost.

## Checked
2026-10-28: Confirmed against the cppreference PImpl page, Herb Sutter GotW 100 and Core Guidelines I.27 (pimpl for stable ABI): unique_ptr to a forward-declared Impl, destructor defined where Impl is complete. Replaced the compiler-specific error text with a generic description.
Method: documentation only; no commands were run.

## Verify
- [ ] Header compiles with only forward declarations (include it alone in a test TU).
- [ ] Changing `Impl` rebuilds only widget.cpp (check with ninja -d explain or build timing).
- [ ] Moved-from objects handled per documentation.
