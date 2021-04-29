# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import ISearchSchema
from zope.component import getUtility
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.volto.subsites:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    disable_searchable_type()


def disable_searchable_type():
    # remove Subsite from searchable types
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISearchSchema, prefix="plone")

    types = list(settings.types_not_searched) + ["Subsite"]
    settings.types_not_searched = tuple(types)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
