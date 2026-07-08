"""Test layer for eea.stringinterp."""

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

import eea.stringinterp


class EeaStringinterpLayer(PloneSandboxLayer):
    """Test layer for eea.stringinterp."""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.stringinterp

        self.loadZCML(package=plone.stringinterp)
        self.loadZCML(package=eea.stringinterp)

    def setUpPloneSite(self, portal):
        """Set up Plone site."""
        applyProfile(portal, "eea.stringinterp:default")


EEA_STRINGINTERP_FIXTURE = EeaStringinterpLayer()

EEA_STRINGINTERP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_STRINGINTERP_FIXTURE,),
    name="EeaStringinterpLayer:IntegrationTesting",
)
