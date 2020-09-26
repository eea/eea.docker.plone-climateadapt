# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import collective.volto.subsites
import plone.restapi


class VoltoSubsitesRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(VoltoSubsitesRestApiLayer, self).setUpZope(
            app, configurationContext
        )

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.subsites)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.subsites:default")


VOLTO_SUBSITES_API_FIXTURE = VoltoSubsitesRestApiLayer()
VOLTO_SUBSITES_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_SUBSITES_API_FIXTURE,),
    name="VoltoSubsitesRestApiLayer:Integration",
)

VOLTO_SUBSITES_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_SUBSITES_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VoltoSubsitesRestApiLayer:Functional",
)
