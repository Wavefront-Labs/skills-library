---
id: computing-software.software-engineering.cpp.unit-tests-with-googletest-and-catch2
name: unit-tests-with-googletest-and-catch2
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-testing, googletest, catch2, gmock, ctest, parameterized-tests, cpp-test-quality]
level: practitioner
status: docs-checked
description: "Test C++ with GoogleTest/GoogleMock or Catch2: fixtures, parameterized tests, matchers and mocks, CTest discovery and running under sanitizers in CI."
sources: ["https://google.github.io/googletest/primer.html", "https://google.github.io/googletest/gmock_for_dummies.html", "https://google.github.io/googletest/advanced.html", "https://github.com/catchorg/Catch2/blob/devel/docs/tutorial.md", "https://github.com/catchorg/Catch2/blob/devel/docs/cmake-integration.md", "https://cmake.org/cmake/help/latest/module/GoogleTest.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Unit tests with GoogleTest or Catch2

**Goal:** fast, isolated C++ tests discovered by CTest, run in CI under sanitizers.

## 1. GoogleTest
```cpp
#include <gtest/gtest.h>
#include "money.h"

TEST(MoneyTest, AddsSameCurrency) {
    EXPECT_EQ(Money(5, "EUR") + Money(7, "EUR"), Money(12, "EUR"));
}
TEST(MoneyTest, RejectsMixedCurrency) {
    EXPECT_THROW(Money(5, "EUR") + Money(1, "USD"), CurrencyMismatch);
}

class LedgerTest : public ::testing::Test {
protected:
    void SetUp() override { ledger.open("acc-1"); }
    Ledger ledger;
};
TEST_F(LedgerTest, StartsEmpty) { ASSERT_EQ(ledger.balance("acc-1"), 0); }

class RoundingTest : public ::testing::TestWithParam<std::pair<double, long>> {};
TEST_P(RoundingTest, RoundsHalfEven) {
    auto [in, expected] = GetParam();
    EXPECT_EQ(round_cents(in), expected);
}
INSTANTIATE_TEST_SUITE_P(Cases, RoundingTest, ::testing::Values(std::pair{0.125, 12L}, std::pair{0.135, 14L}));
```
`EXPECT_*` continues after failure; `ASSERT_*` aborts the test (use when later lines would crash).

## 2. GoogleMock
```cpp
class Gateway { public: virtual ~Gateway() = default; virtual Receipt charge(const Card&, long cents) = 0; };
class MockGateway : public Gateway {
public:
    MOCK_METHOD(Receipt, charge, (const Card&, long cents), (override));
};
TEST(CheckoutTest, ChargesTotal) {
    ::testing::StrictMock<MockGateway> gw;
    EXPECT_CALL(gw, charge(::testing::_, 1200)).WillOnce(::testing::Return(Receipt{"r1"}));
    Checkout(gw).pay(cart_of(1200));
}
```
Mocking requires virtual interfaces (or templates for static polymorphism). Use `NiceMock` to silence uninteresting calls, `StrictMock` to forbid them.

## 3. Catch2 v3
```cpp
#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>
TEST_CASE("money addition", "[money]") {
    Money a(5, "EUR");
    SECTION("same currency") { REQUIRE(a + Money(7, "EUR") == Money(12, "EUR")); }
    SECTION("different currency") { REQUIRE_THROWS_AS(a + Money(1, "USD"), CurrencyMismatch); }
}
TEST_CASE("rounding") {
    auto [in, out] = GENERATE(table<double, long>({{0.125, 12}, {0.135, 14}}));
    CHECK(round_cents(in) == out);
}
```
Each leaf `SECTION` gets a fresh run of the enclosing `TEST_CASE`, giving fresh setup without fixtures.

## 4. CMake integration
```cmake
enable_testing()
find_package(GTest CONFIG REQUIRED)
add_executable(money_tests tests/money_test.cpp)
target_link_libraries(money_tests PRIVATE acme::money GTest::gtest_main GTest::gmock)
include(GoogleTest)
gtest_discover_tests(money_tests DISCOVERY_MODE PRE_TEST)
# Catch2: target_link_libraries(... Catch2::Catch2WithMain) + include(Catch) + catch_discover_tests(t)
```
```bash
ctest --test-dir build --output-on-failure -j8 -R Money
./build/money_tests --gtest_filter='MoneyTest.*' --gtest_repeat=100 --gtest_shuffle
```

## Gotchas
- Floating point: `EXPECT_DOUBLE_EQ`/`EXPECT_NEAR`; in Catch2 prefer the `WithinAbs`/`WithinRel`/`WithinULP` matchers (its docs recommend against `Approx`).
- Death tests (`EXPECT_DEATH`) spawn a child process and should run in a single-threaded context.
- Tests touching global state or the filesystem in parallel CTest runs collide; use unique temp dirs.
- Test binaries without sanitizers miss memory bugs that tests "pass" through.

## Verify
- CI runs `ctest` in a sanitizer preset (ASan+UBSan) and a TSan preset for concurrent code; `--gtest_shuffle` with repeats stays green.

## Checked

Date: 2026-10-25. Documentation: GoogleTest docs (google/googletest docs/primer.md, advanced.md, gmock_for_dummies.md, gmock_cook_book.md, quickstart-cmake.md), Catch2 docs (catchorg/Catch2 docs/tutorial.md, cmake-integration.md, generators.md, comparing-floating-point-numbers.md) and CMake GoogleTest module (Kitware/CMake, head 2026-10-25).

Confirmed: `TEST_P` with `INSTANTIATE_TEST_SUITE_P`; `MOCK_METHOD(ret, name, (args), (override))`; `StrictMock` and `NiceMock`; `--gtest_filter`, `--gtest_repeat`, `--gtest_shuffle`; death tests fork/clone a child and need single-threaded context; `GTest::gtest_main` with `gtest_discover_tests` and `DISCOVERY_MODE <POST_BUILD|PRE_TEST>` (CMake 3.18); Catch2 `catch2/catch_test_macros.hpp`, `catch2/generators/catch_generators.hpp`, `table<...>`, `Catch2::Catch2WithMain`, `include(Catch)` and `catch_discover_tests`, `WithinRel`; Catch2 advises against `Approx`.
Removed as unconfirmed: the claim that Catch2 expression decomposition shows operand values (not re-read) and the "slow, platform-sensitive" wording on death tests.

Method: documentation only; no commands were run.
