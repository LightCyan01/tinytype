import pytest
from matches import matches

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