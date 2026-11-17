---
id: computing-software.software-engineering.cpp.object-slicing-and-value-semantics
name: object-slicing-and-value-semantics
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-hierarchies, cpp-hi-slicing, object-slicing, polymorphism, copy-constructor, clone, value-semantics]
level: practitioner
status: docs-checked
description: "Recognise and prevent C++ object slicing when copying polymorphic types: delete copying in bases, pass by reference or pointer, and implement clone."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c67-a-polymorphic-class-should-suppress-public-copymove", "https://en.cppreference.com/w/cpp/language/copy_constructor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object slicing

Copying a derived object into a base object keeps only the base subobject. The dynamic type and derived data are lost.

```cpp
struct Animal { virtual std::string speak() const { return "..."; } virtual ~Animal() = default; };
struct Dog : Animal { std::string speak() const override { return "woof"; } int tricks = 3; };

void by_value(Animal a) { a.speak(); }          // SLICED: always "..."
std::vector<Animal> zoo; zoo.push_back(Dog{});   // sliced: element is a pure Animal
```

## Prevention (C.67)
- A polymorphic class (one that defines or inherits a virtual function) suppresses public copy/move. If the class has no data, `=delete` the copy/move functions; otherwise make them protected. A clone that copies the derived type needs the derived copy constructor to be usable, so a base with data keeps a protected defaulted copy constructor:
```cpp
struct Animal {
  Animal() = default;
  Animal& operator=(const Animal&) = delete;
  virtual ~Animal() = default;
protected:
  Animal(const Animal&) = default;    // only derived classes can copy the base part
public:
  virtual std::unique_ptr<Animal> clone() const = 0;    // explicit polymorphic copy
};
struct Dog final : Animal {
  std::unique_ptr<Animal> clone() const override { return std::make_unique<Dog>(*this); }   // Dog's implicit copy ctor, which uses the protected base copy ctor
};
```
- Pass polymorphic objects by `const Animal&`, `Animal&`, or smart pointer.
- Store `std::vector<std::unique_ptr<Animal>>` (or `std::variant<Dog, Cat>` for closed sets).
- If you need deep copies of polymorphic objects, use `clone()` functions (C.130 in the Core Guidelines).

## Gotchas
- C.67 enforcement also flags assignment of polymorphic class objects, not only copy construction.
- Exception classes are the stated exception: they must be both polymorphic and copy-constructible.
- If the base copy constructor is deleted, the derived class's implicit copy constructor is deleted too, so `std::make_unique<Dog>(*this)` fails: use the protected defaulted base copy constructor shown above.

## Verify
- [ ] Compile fails for `Animal a = Dog{};`, and the clang-tidy `cppcoreguidelines-slicing` check reports none.
- [ ] A test clones through a base pointer and checks `typeid(*copy) == typeid(Dog)`.

## Checked
2026-11-09. Confirmed on the C++ Core Guidelines (C.67 protected defaulted copy in polymorphic bases, slicing rules), cppreference copy constructor pages and the clang-tidy cppcoreguidelines-slicing check page. Fixed the example so the base has a protected defaulted copy constructor and clone uses the derived class's implicit copy constructor. Removed -Wslicing, exception-slicing and std::function claims not stated on those pages.
Method: documentation only; no commands were run.
