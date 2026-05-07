# tinytype

A minimal runtime type checker built from scratch. Validates Python function arguments against type hints at call time.

## Quick Start

```python
from matches import typecheck

@typecheck
def greet(name: str, times: int) -> str:
    return name * times

greet("hi", 3)       # ✓ returns "hihihi"
greet("hi", "three") # ✗ raises TypeError
```

## Features

- **Basic types**: `int`, `str`, `float`, `bool`, `None`
- **Union types**: `int | str`
- **Collection types**: `list[int]`, `dict[str, int]`, `tuple[int, str]`
- **Optional types**: any `T | None` (e.g. `int | None`, `str | None`), skipping checks when the parameter is left at its default `None` value.

## API

### `matches(value, expected_type) -> bool`

Check if a value matches a type at runtime:

```python
matches(42, int)                  # True
matches([1, 2, 3], list[int])     # True
matches([1, "x", 3], list[int])   # False
matches(None, int | None)         # True
```

### `@typecheck`

Decorator that validates all function arguments before execution:

```python
@typecheck
def add(a: int, b: int = 0) -> int:
    return a + b

add(5)           # ✓ uses default b=0
add(5, 3)        # ✓
add(5, "3")      # ✗ TypeError
```

## Tests

Run the test suite:

```bash
pytest -v
```

30 tests covering all type matchers, decorators, and edge cases.