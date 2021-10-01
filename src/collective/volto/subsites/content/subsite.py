# -*- coding: utf-8 -*-
from collective.volto.subsites import _
from plone.app.textfield import RichText as RichTextField
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.schema import Choice
from plone.schema import SourceText
from plone.supermodel import model
from zope.interface import implementer


class ISubsite(model.Schema):
    """ """

    subsite_header = RichTextField(
        title=_("subsite_header_label", default="Subsite header"),
        description=_(
            "subsite_header_help",
            default="Insert some text that will be shown as the subsite header"
            " in each content inside a subsite.",
        ),
        required=False,
    )
    subsite_logo = NamedBlobImage(
        title=_("subsite_logo_label", default="Logo"),
        description=_(
            "subsite_logo_help",
            default="Insert a logo that can be shown in subsite header.",
        ),
        required=False,
    )
    subsite_footer = RichTextField(
        title=_("subsite_footer_label", default="Subsite footer"),
        description=_(
            "subsite_footer_help",
            default="Insert some text that will be shown as the subsite footer"
            " in each content inside a subsite.",
        ),
        required=False,
    )

    subsite_css_class = Choice(
        title=_("subsite_css_class_label", default="Subsite style"),
        description=_(
            "subsite_css_class_help",
            default="If this subsite should have a custom layout, please "
            "select one from the following list.",
        ),
        required=False,
        vocabulary="volto.subsites.colors",
    )

    subsite_social_links = SourceText(
        title=_("subsite_social_links_label", default="Social links"),
        description=_(
            "subsite_social_links_help",
            default="Insert a list of values for social links that will be "
            "shown in the frontend (if expected).",
        ),
        default="[]",
    )

    directives.widget("subsite_header", RichTextFieldWidget)
    directives.widget("subsite_footer", RichTextFieldWidget)


@implementer(ISubsite)
class Subsite(Container):
    """ """
