"""
Core logic for matching HTTP Origin and Access-Control-Allow-Origin headers.

This module implements the CORS origin matching rules described in the
Fetch Standard (https://fetch.spec.whatwg.org/#cors-protocol).
"""

import re
from typing import Optional


def is_valid_origin(origin: str) -> bool:
    """
    Return True if *origin* is a syntactically valid serialized origin.

    A serialized origin is either the string "null" or a scheme, host, and
    optional port. The scheme must be "http" or "https" (case-insensitive).
    The host must be a valid hostname or IP address. The port, if present,
    must be a decimal integer between 0 and 65535 inclusive.

    We intentionally do not perform DNS resolution; this is a syntactic check
    only, matching the browser's behaviour when serializing an origin.
    """
    if origin == "null":
        return True

    # Scheme
    m = re.match(r"^(https?)://", origin, re.IGNORECASE)
    if not m:
        return False
    scheme = m.group(1).lower()
    rest = origin[m.end():]

    # Split host and port
    if rest.startswith("["):
        # IPv6 literal
        end = rest.find("]")
        if end == -1:
            return False
        host = rest[1:end]
        port_part = rest[end + 1:]
        if port_part and not port_part.startswith(":"):
            return False
        port_str = port_part[1:] if port_part else None
        # Validate IPv6 address (simplified: hex digits and colons)
        if not re.match(r"^[0-9a-fA-F:]+$", host):
            return False
    else:
        # Hostname or IPv4
        if ":" in rest:
            host, port_str = rest.rsplit(":", 1)
        else:
            host, port_str = rest, None
        if not host:
            return False
        # Hostname validation: letters, digits, hyphens, dots
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            return False
        # No leading/trailing dots or hyphens, no consecutive dots
        if host.startswith(".") or host.endswith(".") or ".." in host:
            return False
        if host.startswith("-") or host.endswith("-"):
            return False

    if port_str is not None:
        if not port_str.isdigit():
            return False
        port = int(port_str)
        if port < 0 or port > 65535:
            return False

    return True


def match_origin(origin: str, allow_origin: str) -> bool:
    """
    Return True if the Access-Control-Allow-Origin header value *allow_origin*
    permits the request *origin* according to CORS rules.

    The matching rules are:

    - If *allow_origin* is the literal string ``"*"``, it matches any origin,
      including ``"null"``.
    - Otherwise, *allow_origin* must be a valid origin (as per
      :func:`is_valid_origin`) and must be byte-for-byte identical to
      *origin*.

    Note: The CORS spec also defines a case-insensitive match for the scheme
    and host, but the serialized origin produced by browsers is already
    lowercase. To avoid surprising mismatches, we require an exact match.
    """
    if allow_origin == "*":
        return True
    if not is_valid_origin(allow_origin):
        return False
    return origin == allow_origin
