# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.volto.subsites.interfaces import IVoltoSubsitesSettings
from collective.volto.subsites import _


class SubsitesSettingsForm(controlpanel.RegistryEditForm):

    schema = IVoltoSubsitesSettings
    label = _("volto_subsites_settings_label", default=u"Subsites Settings")
    description = u""


class SubsitesSettings(controlpanel.ControlPanelFormWrapper):
    form = SubsitesSettingsForm
