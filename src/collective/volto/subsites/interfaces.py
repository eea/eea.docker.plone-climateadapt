# -*- coding: utf-8 -*-
from collective.volto.subsites import _
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine, List


class ICollectiveVoltoSubsitesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IVoltoSubsitesSettings(Interface):
    """ Interface for Volto Subsites controlpanel """

    available_colors = List(
        title=_("available_colors_label", default="Available colors"),
        description=_(
            "available_colors_help",
            default="Fill this field with a list of available colors for "
            "Subsistes. Write one color per row with the following format:"
            " css_class|label "
            'where: "css_class" is the name of the css class that will be '
            'used in the frontend and "label" is a human-friendly name for'
            "that color.",
        ),
        default=[],
        value_type=TextLine(),
    )
