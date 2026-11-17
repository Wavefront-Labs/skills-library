---
id: computing-software.software-engineering.cpp.virtual-destructors-and-polymorphic-base-classes
name: virtual-destructors-and-polymorphic-base-classes
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-classes, cpp-cl-virtual-dtor, virtual-destructor, polymorphism, base-class, protected-destructor, delete-through-base, virtual-destructors]
level: practitioner
status: docs-checked
description: "Prevent undefined behaviour deleting through base pointers: virtual or protected non-virtual destructors, pure virtual destructors and abstract interfaces."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c35-a-base-class-destructor-should-be-either-public-and-virtual-or-protected-and-non-virtual", "https://en.cppreference.com/w/cpp/language/destructor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual destructors and polymorphic bases

Deleting a derived object through a pointer to a base whose destructor is not virtual is **undefined behaviour** (cppreference, Destructor). C.35's bad example shows `unique_ptr<Base>` destroying a `D` via `~Base()`, which leaks `D`'s members.

```cpp
struct Shape {
  virtual ~Shape() = default;               // public and virtual: deletable through Shape*
  virtual double area() const = 0;
protected:
  Shape() = default;                         // protect copy/move to prevent slicing
  Shape(const Shape&) = default;
  Shape& operator=(const Shape&) = default;
};
struct Circle final : Shape {
  explicit Circle(double r) : r_(r) {}
  double area() const override { return 3.14159265 * r_ * r_; }
private: double r_;
};
std::unique_ptr<Shape> s = std::make_unique<Circle>(2);   // destroys Circle correctly
```

## Rule (C.35)
A base destructor is either **public and virtual** (owners delete through base) or **protected and non-virtual** (nobody can delete through base). The enforcement rule flags a class with any virtual functions whose destructor is neither. A destructor must also be non-private, or the type cannot be destroyed.

## Details
- A pure virtual destructor makes a base abstract when it has no other pure virtual function, and it still needs a definition because all base destructors run when the derived object is destroyed: `AbstractBase::~AbstractBase() {}` (cppreference).
- C.67: a polymorphic class should suppress public copy/move, which is why the example protects them.

## Gotchas
- A destructor that is not virtual in a base with virtual functions is the bug C.35 describes, even when no code deletes through the base today.
- Destructors should not exit by throwing (C.36); a throwing destructor called during stack unwinding calls `std::terminate`.

## Verify
- [ ] A test destroys a derived object via `unique_ptr<Base>` and asserts the derived destructor ran.

## Checked
2026-11-03. Confirmed on Core Guidelines C.35 (rule, bad example, non-private destructor, enforcement), C.36 and cppreference Destructor (virtual destructors UB, pure virtual destructors need a definition, throwing during unwinding). Removed: Rule-of-Five and implicit-move claim, `shared_ptr` deleter claim, virtual-call-in-constructor note, compiler warning flags and MSVC C4265, the vptr size claim, `final` note, the destruction-order note and the AddressSanitizer check.
Method: documentation only; no commands were run.
