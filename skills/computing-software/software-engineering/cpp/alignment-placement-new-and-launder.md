---
id: computing-software.software-engineering.cpp.alignment-placement-new-and-launder
name: alignment-placement-new-and-launder
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-memory-model, cpp-mm-align, cpp-mm-placement, alignas, placement-new, std-launder, object-lifetime, strict-aliasing, alignment-padding, placement-new-launder]
level: advanced
status: docs-checked
description: "Control C++ object storage: alignof/alignas and padding, aligned allocation, placement new, explicit destructor calls, std::launder, start_lifetime_as and the aliasing rules."
sources: ["https://en.cppreference.com/w/cpp/language/object", "https://en.cppreference.com/w/cpp/utility/launder", "https://en.cppreference.com/w/cpp/language/new"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alignment, placement new and launder

## Alignment and padding
Every object type has an alignment requirement: a power-of-two byte count (type `std::size_t`) between successive addresses where objects of that type can be allocated. Query it with `alignof` (or `std::alignment_of`); `std::align` finds a suitably aligned pointer inside a buffer. Padding bits are bits of the object representation that are not part of the value representation; they may be introduced to satisfy alignment requirements and bit-field sizes.
```cpp
struct A { char c; int i; char d; };          // padding after c and after d (exact sizeof is ABI-dependent)
struct B { int i; char c; char d; };          // same members, different order: compare sizeof(A) and sizeof(B) on your target
alignas(64) char buf[256];                    // storage aligned to 64 bytes
auto* p = ::operator new(1024, std::align_val_t{64});   // over-aligned allocation (C++17, <new>)
```
Print `sizeof` and `alignof` for your target rather than assuming numbers.

## Placement new and manual lifetime
```cpp
alignas(Widget) std::byte storage[sizeof(Widget)];
Widget* w = ::new (static_cast<void*>(storage)) Widget(args);   // construct in existing memory; no allocation
w->~Widget();                                                    // you must destroy explicitly; storage is not freed
```
The standard placement allocation function `void* operator new(std::size_t, void*)` simply returns its second argument, so the new expression only constructs the object. The destructor must be called manually. For a placement allocation function, a matching deallocation function (same parameter list apart from the first) is what a new expression uses if construction throws.

## std::launder
`std::launder` (C++17, `<new>`) is `constexpr T* launder(T* p) noexcept`: it returns a pointer to the object of type `T` (ignoring cv-qualifiers) at the address `p` represents, provided that object is within its lifetime and every byte reachable through the result is reachable through `p`; otherwise the behavior is undefined. It does nothing to its argument, so its return value must be used, and it is ill-formed for function types and `void`.

Typical uses: getting a pointer to an object created in the storage of an existing object of the same type when pointers to the old object cannot be reused (for example base class subobjects), and getting a pointer to an object created by placement new from a pointer to the object that provides its storage. The pointer value returned by the new expression itself can be used directly.

## Reading bytes as an object
Casting a buffer address with `reinterpret_cast` does not create an object of the target type. Copy the bytes into a `T` (`std::memcpy`) or use `std::bit_cast`; `std::start_lifetime_as` (C++23) is listed under explicit lifetime management in `<memory>`, so check your standard library for it.

## Gotchas
- Never use `delete` on an object created by placement new into storage you own; call the destructor.
- Storage alignment must be at least `alignof(T)`: a plain `char buf[sizeof(T)]` needs `alignas(T)`.
- A placement new with a null pointer passed to the non-allocating form is undefined.
- Compilers differ in layout details; check `sizeof` and `alignof` with `static_assert` for the targets you ship.

## Verify
- [ ] `static_assert(alignof(Storage) >= alignof(T))` for every hand-rolled storage buffer.
- [ ] Tests build the storage, construct, use and destroy the object, and run under your usual sanitizers.

## Checked
2026-11-08. Confirmed on cppreference Objects (alignment requirement, alignof/alignment_of/std::align, object and value representation, padding bits), std::launder (signature, header, conditions, ill-formed cases, notes on typical uses) and new-expression (placement new description, manual destructor call, matching deallocation function, null-pointer placement case). Removed: the const-member launder example, sizeof numbers, -fsanitize options, std::optional/variant internals, construct_at/destroy_at, packed-struct and Standard-library over-alignment claims (not on the pages read).
Method: documentation only; no commands were run.
