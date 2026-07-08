"""Integration tests for eea.stringinterp setup."""

import unittest

from plone import api

from eea.stringinterp.testing import EEA_STRINGINTERP_INTEGRATION_TESTING

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that eea.stringinterp is properly installed."""

    layer = EEA_STRINGINTERP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if eea.stringinterp is installed."""
        self.assertTrue(self.installer.is_product_installed("eea.stringinterp"))

    def test_browserlayer(self):
        """Test that browser layer is registered."""
        from plone.browserlayer import utils

        from eea.stringinterp.interfaces import IEeaStringinterpLayer

        self.assertIn(IEeaStringinterpLayer, utils.registered_layers())


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
