"""
Cross Origin Resource Sharing Matcher

Validates and matches HTTP Origin and Access-Control-Allow-Origin header pairs
per the CORS specification.
"""

from .core import match_origin, is_valid_origin

__all__ = ["match_origin", "is_valid_origin"]
