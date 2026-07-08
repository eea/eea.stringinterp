"""Tests for LazyDict adapter."""

import unittest

from zope.interface import Interface, implementer
from zope.component import getGlobalSiteManager

from plone.stringinterp.interfaces import IStringSubstitution
from eea.stringinterp.adapters.dollarReplace import LazyDict, _marker


@implementer(IStringSubstitution)
class SuccessAdapter:
    """Test adapter that returns a value."""

    def __init__(self, context):
        self.context = context

    def __call__(self, key=None):
        return f"value_for_{key}"


@implementer(IStringSubstitution)
class UnauthorizedAdapter:
    """Test adapter that raises Unauthorized."""

    def __init__(self, context):
        self.context = context

    def __call__(self, key=None):
        from AccessControl import Unauthorized
        raise Unauthorized("Not allowed")


class DummyContext:
    """Simple context for testing."""
    pass


class TestLazyDictKeyFiltering(unittest.TestCase):
    """Test LazyDict key filtering — no adapters needed."""

    def setUp(self):
        self.ldict = LazyDict(DummyContext())

    def test_underscore_key_raises_keyerror(self):
        """Test that keys starting with _ raise KeyError."""
        with self.assertRaises(KeyError):
            self.ldict["_test"]

    def test_dot_key_raises_keyerror(self):
        """Test that keys starting with . raise KeyError."""
        with self.assertRaises(KeyError):
            self.ldict[".test"]

    def test_empty_key_raises_keyerror(self):
        """Test that empty key raises KeyError."""
        with self.assertRaises(KeyError):
            self.ldict[""]

    def test_none_key_raises_keyerror(self):
        """Test that None key raises KeyError."""
        with self.assertRaises(KeyError):
            self.ldict[None]


class TestLazyDictNoAdapter(unittest.TestCase):
    """Test LazyDict with no adapters registered — both paths fail."""

    def setUp(self):
        self.ldict = LazyDict(DummyContext())

    def test_unregistered_key_raises_keyerror(self):
        """Test that unregistered key raises KeyError."""
        with self.assertRaises(KeyError):
            self.ldict["nonexistent_key"]


class TestLazyDictNamedAdapter(unittest.TestCase):
    """Test LazyDict with named adapter — parent path succeeds."""

    def setUp(self):
        self.sm = getGlobalSiteManager()
        self.sm.registerAdapter(
            SuccessAdapter, (Interface,), IStringSubstitution, name="named_key"
        )
        self.ldict = LazyDict(DummyContext())

    def tearDown(self):
        self.sm.unregisterAdapter(
            SuccessAdapter, (Interface,), IStringSubstitution, name="named_key"
        )

    def test_named_adapter_returns_value(self):
        """Test that named adapter returns value via parent path."""
        result = self.ldict["named_key"]
        self.assertEqual(result, "value_for_None")


class TestLazyDictUnnamedAdapter(unittest.TestCase):
    """Test LazyDict with unnamed adapter — fallback path succeeds."""

    def setUp(self):
        self.sm = getGlobalSiteManager()
        self.sm.registerAdapter(
            SuccessAdapter, (Interface,), IStringSubstitution
        )
        self.ldict = LazyDict(DummyContext())

    def tearDown(self):
        self.sm.unregisterAdapter(
            SuccessAdapter, (Interface,), IStringSubstitution
        )

    def test_unnamed_adapter_fallback(self):
        """Test that fallback path with unnamed adapter returns value."""
        result = self.ldict["fallback_key"]
        self.assertEqual(result, "value_for_fallback_key")


class TestLazyDictUnauthorized(unittest.TestCase):
    """Test LazyDict with Unauthorized adapter."""

    def setUp(self):
        self.sm = getGlobalSiteManager()
        self.sm.registerAdapter(
            UnauthorizedAdapter, (Interface,), IStringSubstitution
        )
        self.ldict = LazyDict(DummyContext())

    def tearDown(self):
        self.sm.unregisterAdapter(
            UnauthorizedAdapter, (Interface,), IStringSubstitution
        )

    def test_unauthorized_returns_unauthorized_string(self):
        """Test that Unauthorized exception returns 'Unauthorized' string."""
        result = self.ldict["protected_key"]
        self.assertEqual(result, "Unauthorized")


class TestLazyDictCaching(unittest.TestCase):
    """Test LazyDict caching behavior."""

    def setUp(self):
        self.sm = getGlobalSiteManager()
        self.sm.registerAdapter(
            SuccessAdapter, (Interface,), IStringSubstitution
        )
        self.ldict = LazyDict(DummyContext())

    def tearDown(self):
        self.sm.unregisterAdapter(
            SuccessAdapter, (Interface,), IStringSubstitution
        )

    def test_result_is_cached(self):
        """Test that result is cached in _cache."""
        result1 = self.ldict["cache_key"]
        self.assertEqual(result1, "value_for_cache_key")
        self.assertIn("cache_key", self.ldict._cache)

    def test_cached_value_used_on_second_call(self):
        """Test that second call uses cached value."""
        result1 = self.ldict["cache_key"]
        # Manually change cache to verify it's used
        self.ldict._cache["cache_key"] = "cached_value"
        result2 = self.ldict["cache_key"]
        self.assertEqual(result2, "cached_value")


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)