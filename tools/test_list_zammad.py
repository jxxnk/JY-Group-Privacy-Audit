import unittest

from list_zammad import validate_base_url


class ListZammadUrlTests(unittest.TestCase):
    def test_allows_loopback_8080(self):
        self.assertEqual(
            validate_base_url("http://127.0.0.1:8080"),
            "http://127.0.0.1:8080",
        )
        self.assertEqual(
            validate_base_url("http://localhost:8080/"),
            "http://localhost:8080",
        )

    def test_rejects_remote_host(self):
        with self.assertRaises(ValueError):
            validate_base_url("http://example.com:8080")

    def test_rejects_https_or_wrong_port(self):
        with self.assertRaises(ValueError):
            validate_base_url("https://127.0.0.1:8080")
        with self.assertRaises(ValueError):
            validate_base_url("http://127.0.0.1:3000")

    def test_rejects_credentials_query_and_fragment(self):
        for value in (
            "http://user:pass@127.0.0.1:8080",
            "http://127.0.0.1:8080?next=remote",
            "http://127.0.0.1:8080/#fragment",
        ):
            with self.assertRaises(ValueError):
                validate_base_url(value)


if __name__ == "__main__":
    unittest.main()
