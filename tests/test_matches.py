import pytest
from matches import matches, typecheck

def test_int() -> None:
    assert matches(42, int) == True
    
def test_mismatch() -> None:
    assert matches("hi", int) == False

def test_bool() -> None:
    assert matches(True, bool) == True

def test_union_int() -> None:
    assert matches(42, int | str) == True

def test_mismatch_union() -> None:
    assert matches(3.14, int | str) == False

def test_none() -> None:
    with pytest.raises(TypeError):
        matches(None, None)
        
def test_none_type() -> None:
    assert matches(None, type(None)) == True
    
def test_int_bool() -> None:
    assert matches(True, int) == True
    
def test_second_type_union() -> None:
    assert matches("hi", int | str) == True
    
def test_union_numeric() -> None:
    assert matches(42, str | float) == False
    
# Collection Types
def test_list_type() -> None:
    assert matches([1, 2, 3], list[int]) == True

def test_list_type_mismatch() -> None:
    assert matches([1, "bleh", 3], list[int]) == False

def test_list_type_empty() -> None:
    assert matches([], list[int]) == True
    
def test_dict_type() -> None:
    assert matches({"key": 1}, dict[str, int]) == True

def test_dict_type_mismatch() -> None:
    assert matches({1: "test"}, dict[str, int]) == False
    
def test_dict_type_empty() -> None:
    assert matches({}, dict[str, int]) == True
    
def test_tuple_type() -> None:
    assert matches((1, "test"), tuple[int, str]) == True

def test_tuple_type_mismatch() -> None:
    assert matches(("test", 1), tuple[int, str]) == False

def test_tuple_type_empty() -> None:
    assert matches((), tuple[int, str]) == True
    
def test_tuple_type_extra() -> None:
    assert matches((1, "test", 2), tuple[int, str]) == True

@typecheck
def greet(name: str, times: int) -> str:
    return name * times

def test_typecheck_valid_call() -> None:
    assert greet("hi", 3) == "hihihi"
    
@typecheck
def repeat(msg: str, times: int = 2) -> str:
    return msg * times
    
def test_typecheck_invalid_call() -> None:
    with pytest.raises(TypeError):
        greet("hi", "three")

def test_typecheck_default_arg_valid() -> None:
    assert repeat("ha") == "haha" 
    
@typecheck
def combine(a: int, b: str, c: list[int]) -> str:
    return b * a + str(sum(c))

def test_typecheck_multi_param_valid() -> None:
    assert combine(2, "x", [1, 2]) == "xx3"

def test_typecheck_multi_param_invalid() -> None:
    with pytest.raises(TypeError):
        combine("2", "x", [1, 2])
        
@typecheck
def mixed_func(a: int, b: int | None = None, c: str | None = None) -> str:
    # just return something so we can assert on it
    return f"{a}-{b}-{c}"        
        
def test_mixed_required_optional_only_required() -> None:
    result = mixed_func(1)
    assert result == "1-None-None"

def test_mixed_optional_given_valid_values() -> None:
    result = mixed_func(2, 10, "x")
    assert result == "2-10-x"
    
def test_mixed_optional_given_none() -> None:
    result = mixed_func(3, None, None)
    assert result == "3-None-None"

def test_mixed_required_wrong_type() -> None:
    with pytest.raises(TypeError):
        mixed_func("not-an-int")  # a should be int

def test_mixed_optional_wrong_type() -> None:
    with pytest.raises(TypeError):
        mixed_func(1, "not-an-int")  # b should be int | None