# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.volto.subsites.testing import (
    VOLTO_SUBSITES_API_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISearchSchema
from zope.component import getUtility

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.volto.subsites is properly installed."""

    layer = VOLTO_SUBSITES_API_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.volto.subsites is installed."""
        self.assertTrue(
            self.installer.isProductInstalled("collective.volto.subsites")
        )

    def test_browserlayer(self):
        """Test that ICollectiveVoltoSubsitesLayer is registered."""
        from collective.volto.subsites.interfaces import (
            ICollectiveVoltoSubsitesLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(ICollectiveVoltoSubsitesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = VOLTO_SUBSITES_API_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["collective.volto.subsites"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.volto.subsites is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled("collective.volto.subsites")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveVoltoSubsitesLayer is removed."""
        from collective.volto.subsites.interfaces import (
            ICollectiveVoltoSubsitesLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveVoltoSubsitesLayer, utils.registered_layers()
        )

    def test_subsite_not_searchable(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchSchema, prefix="plone")
        self.assertIn("Subsite", settings.types_not_searched)
