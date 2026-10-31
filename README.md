# cross_origin_resource_sharing_matcher

Validates and matches HTTP Origin and Access-Control-Allow-Origin header pairs per the CORS specification.

```python
from cross_origin_resource_sharing_matcher import match_origin, is_valid_origin

is_valid_origin("https://example.com:8080")  # True
match_origin("https://example.com", "*")     # True
match_origin("https://example.com", "https://example.com")  # True
match_origin("https://example.com", "https://other.com")    # False
```

## Why this exists

Browsers enforce CORS, but servers and proxies often need to validate or simulate the same rules. The trade-off here is strictness: we perform a syntactic check on the origin and require an exact match for non-wildcard allow-origins. This avoids the complexity of case-insensitive scheme/host matching and punycode normalisation, which are rarely needed in server-side validation where the Origin header is already serialized by the browser.

## Awkward edge

The `null` origin is valid and matches only the literal `null` allow-origin (or `*`). Do not treat it as an empty string.
