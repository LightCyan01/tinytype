import logging
import types
import inspect
from typing import get_type_hints, get_origin, get_args

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def matches(value, expected_type) -> bool:
    logger.debug(f"Value: {value}, Expected Type: {getattr(expected_type, "__name__", expected_type)}")
    logger.debug(f"Expected Type: {expected_type}")
    
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
        
        return all(matches(elem, type) for elem, type in zip(value, args))
    
    return isinstance(value, expected_type)

def typecheck(func):
    hints = get_type_hints(func)
    sig = inspect.signature(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        logger.debug(f"sig bind: {bound}")
        bound.apply_defaults()
        
        for name, value in bound.arguments.items():
            expected_type = hints.get(name)
            logger.debug(f"Expected Type: {expected_type}")
            if expected_type is not None and not matches(value, expected_type):
                raise TypeError(f"Argument '{name}' = {value!r} does not match expected type {expected_type}")
        return func(*args, **kwargs)
    return wrapper