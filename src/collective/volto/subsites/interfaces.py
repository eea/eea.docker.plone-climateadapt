# -*- coding: utf-8 -*-
from collective.volto.subsites import _
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine, List


class ICollectiveVoltoSubsitesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IVoltoSubsitesSettings(Interface):
    """ Interface for Volto Subsites controlpanel """

    available_styles = List(
        title=_("available_styles_label", default="Available styles"),
        description=_(
            "available_styles_help",
            default="Fill this field with a list of available styles for "
            "Subsistes. A style is a css class that will provide some custom "
            "layout to the Subsite and its children."
            "Write one style per row with the following format:"
            " css_class|label "
            'where "css_class" is the name of the css class that will be '
            'used in the theme and "label" is a human-friendly name for'
            "that style.",
        ),
        default=[],
        value_type=TextLine(),
    )
