import logging
import types
import typing

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def matches(value, expected_type) -> bool:
    logger.debug(f"Value: {value}, Expected Type: {getattr(expected_type, "__name__", expected_type)}")
    logger.debug(f"Expected Type: {expected_type}")
    
    if isinstance(expected_type, types.UnionType):
        logger.debug(expected_type.__args__)
        return any(matches(value, t) for t in expected_type.__args__)
    
    
        
    return isinstance(value, expected_type)

print(typing.get_origin(list[int]))
print(typing.get_args(list[int]))
print(typing.get_origin(int))