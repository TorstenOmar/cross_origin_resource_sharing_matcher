import unittest
from cross_origin_resource_sharing_matcher import match_origin, is_valid_origin


class TestIsValidOrigin(unittest.TestCase):
    def test_valid_http(self):
        self.assertTrue(is_valid_origin("http://example.com"))

    def test_valid_https(self):
        self.assertTrue(is_valid_origin("https://example.com"))

    def test_valid_with_port(self):
        self.assertTrue(is_valid_origin("http://example.com:8080"))

    def test_valid_null(self):
        self.assertTrue(is_valid_origin("null"))

    def test_invalid_scheme(self):
        self.assertFalse(is_valid_origin("ftp://example.com"))

    def test_invalid_no_scheme(self):
        self.assertFalse(is_valid_origin("example.com"))

    def test_invalid_port(self):
        self.assertFalse(is_valid_origin("http://example.com:99999"))

    def test_invalid_ipv6(self):
        self.assertFalse(is_valid_origin("http://[::1"))

    def test_valid_ipv6(self):
        self.assertTrue(is_valid_origin("http://[::1]"))

    def test_invalid_host_characters(self):
        self.assertFalse(is_valid_origin("http://exa mple.com"))


class TestMatchOrigin(unittest.TestCase):
    def test_wildcard_matches_any(self):
        self.assertTrue(match_origin("http://example.com", "*"))
        self.assertTrue(match_origin("null", "*"))

    def test_exact_match(self):
        self.assertTrue(match_origin("http://example.com", "http://example.com"))

    def test_exact_match_with_port(self):
        self.assertTrue(match_origin("http://example.com:8080", "http://example.com:8080"))

    def test_mismatch(self):
        self.assertFalse(match_origin("http://example.com", "http://other.com"))

    def test_invalid_allow_origin(self):
        self.assertFalse(match_origin("http://example.com", "not-an-origin"))

    def test_null_origin(self):
        self.assertTrue(match_origin("null", "null"))
        self.assertFalse(match_origin("null", "http://example.com"))

    def test_case_sensitivity(self):
        self.assertFalse(match_origin("http://Example.com", "http://example.com"))


if __name__ == "__main__":
    unittest.main()
