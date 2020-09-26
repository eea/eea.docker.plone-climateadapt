# -*- coding: utf-8 -*-
from collective.volto.subsites.interfaces import IVoltoSubsitesSettings
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, Interface)
class SubsitesSettingsControlpanel(RegistryConfigletPanel):
    schema = IVoltoSubsitesSettings
    configlet_id = "SubsitesSettings"
    configlet_category_id = "Products"
    schema_prefix = None
