# -*- coding: utf-8 -*-
from plone import api
from collective.volto.subsites.interfaces import IVoltoSubsitesSettings
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@implementer(IVocabularyFactory)
class SubsitesColorsVocabularyFactory(object):
    @property
    def terms(self):
        terms = []
        colors = api.portal.get_registry_record(
            "available_styles", interface=IVoltoSubsitesSettings, default=[]
        )
        for color in colors:
            if "|" in color:
                value, label = color.split("|")
            else:
                label = value = color
            terms.append(SimpleTerm(value=value, token=value, title=label))
        return terms

    def __call__(self, context):
        self.context = context
        return SimpleVocabulary(self.terms)


SubsitesColorsVocabulary = SubsitesColorsVocabularyFactory()
