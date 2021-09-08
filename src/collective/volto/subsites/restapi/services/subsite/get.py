# -*- coding: utf-8 -*-
from collective.volto.subsites.content.subsite import ISubsite
from plone.dexterity.utils import iterSchemata
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFields

FIELDS = [
    "subsite_header",
    "subsite_logo",
    "subsite_footer",
    "subsite_css_class",
    "subsite_social_links",
    "image",
]


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Subsite(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"subsite": {"@id": "{}/@subsite".format(self.context.absolute_url())}}
        if not expand:
            return result

        result["subsite"] = self.get_subsite_info()
        return result

    def get_subsite_info(self):
        subsite = None
        for item in self.context.aq_chain:
            if ISubsite.providedBy(item):
                subsite = item
        if not subsite:
            return {}

        serializer = queryMultiAdapter((subsite, self.request), ISerializeToJsonSummary)

        data = serializer()

        for schema in iterSchemata(subsite):
            for name, field in getFields(schema).items():
                if name not in FIELDS:
                    continue
                serializer = queryMultiAdapter(
                    (field, subsite, self.request), IFieldSerializer
                )
                value = serializer()
                data[json_compatible(name)] = value

        return data


class SubsiteGet(Service):
    def reply(self):
        subsite = Subsite(self.context, self.request)
        return subsite(expand=True)["subsite"]
