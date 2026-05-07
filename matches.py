import logging
import types
import inspect
from typing import get_type_hints, get_origin, get_args
from functools import wraps

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def matches(value, expected_type) -> bool:
    if isinstance(expected_type, types.UnionType):
        logger.debug(expected_type.__args__)
        return any(matches(value, t) for t in expected_type.__args__)
    
    origin = get_origin(expected_type)
    args = get_args(expected_type)
    if origin is list:
        if not isinstance(value, list):
            return False
        if not args:
            return True
        
        element_type = args[0]
        return all(matches(item, element_type) for item in value)
    
    if origin is dict:
        if not isinstance(value, dict):
            return False
        if not args: 
            return True
        
        key_type, val_type = args
        return all(matches(k, key_type) and matches(v, val_type) for k,v in value.items())
    
    if origin is tuple:
        if not isinstance(value, tuple):
            return False
        if not args:
            return True
        if not value:
            return True
        
        return all(matches(elem, elem_type) for elem, elem_type in zip(value, args))
    
    return isinstance(value, expected_type)

def typecheck(func):
    hints = get_type_hints(func)
    sig = inspect.signature(func)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        
        for param_name, param_value in bound.arguments.items():
            param = sig.parameters[param_name]
            expected_type = hints.get(param_name)
            logger.debug(f"Param: {param}")
            logger.debug(f"Expected Type: {expected_type}")
            
            if expected_type is None:
                continue
            
            #optional, default handling
            type_args = get_args(expected_type)
            
            is_union = isinstance(expected_type, types.UnionType)
            is_optional = is_union and type(None) in type_args
            has_default = param.default is not inspect._empty
            is_default_value = has_default and param_value == param.default
            
            if is_optional and is_default_value:
                continue
    
            if not matches(param_value, expected_type):
                raise TypeError(f"Argument '{param_name}' = {param_value!r} does not match expected type {expected_type}")
            
        return func(**bound.arguments)
    return wrapper

@typecheck
def greet(name: str, times: int) -> str:
    return name * times

@typecheck
def greet_opt(name: str, times: int | None = None) -> str:
    if times is None:
        times = 1
    return name * times
