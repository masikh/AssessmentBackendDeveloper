""" __init__ file"""
from generic_helpers.memoize import Memoize

# Initialize memoization
memoize = Memoize(ttl=300, max_items=300)
