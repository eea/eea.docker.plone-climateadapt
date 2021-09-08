# -*- coding: utf-8 -*-
from collective.volto.subsites.testing import (
    VOLTO_SUBSITES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobImage
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest
import os


class TestExpansion(unittest.TestCase):

    layer = VOLTO_SUBSITES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        image_file = os.path.join(os.path.dirname(__file__), u"image.png")
        with open(image_file, "rb") as f:
            image_data = f.read()

        self.folder = api.content.create(
            container=self.portal, type="Folder", title="Normal folder"
        )
        self.subsite = api.content.create(
            container=self.portal,
            type="Subsite",
            title="Subsite",
            subsite_header=RichTextValue(
                raw="<p>header</p>",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
            subsite_footer=RichTextValue(
                raw="<p>footer</p>",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
            subsite_css_class="red",
            image=NamedBlobImage(
                data=image_data, contentType="image/png", filename=u"image.png"
            ),
            subsite_logo=NamedBlobImage(
                data=image_data, contentType="image/png", filename=u"image.png"
            ),
        )
        self.document_in_subsite = api.content.create(
            container=self.subsite,
            type="Document",
            title="Document in subsite",
        )
        self.document_outside_subsite = api.content.create(
            container=self.folder,
            type="Document",
            title="Document outside subsite",
        )

        commit()

    def tearDown(self):
        self.api_session.close()

    def test_subsite_expansion_visible_inside_subsite(self):
        response = self.api_session.get(self.subsite.absolute_url())
        result = response.json()
        self.assertIn("subsite", result["@components"])

        response = self.api_session.get(self.document_in_subsite.absolute_url())
        result = response.json()
        self.assertIn("subsite", result["@components"])

    def test_subsite_expansion_visible_outside_subsite(self):
        response = self.api_session.get(self.document_outside_subsite.absolute_url())
        result = response.json()

        self.assertIn("subsite", result["@components"])

    def test_expansion_not_expanded_by_default(self):
        response = self.api_session.get(self.document_in_subsite.absolute_url())
        result = response.json()
        self.assertEqual(
            result["@components"]["subsite"],
            {"@id": "{}/@subsite".format(self.document_in_subsite.absolute_url())},
        )

    def test_expansion_expanded_if_passed_parameter(self):
        response = self.api_session.get(
            "{}?expand=subsite".format(self.document_in_subsite.absolute_url())
        )
        result = response.json()
        data = result["@components"]["subsite"]

        self.assertEqual(data["@id"], self.subsite.absolute_url())
        self.assertEqual(data["@type"], self.subsite.portal_type)
        self.assertEqual(data["title"], self.subsite.title)
        self.assertEqual(data["description"], "")
        self.assertIn("image", data)
        self.assertIn("subsite_logo", data)
        self.assertEqual(data["subsite_css_class"], self.subsite.subsite_css_class)
        self.assertEqual(
            data["subsite_header"]["data"], self.subsite.subsite_header.output
        )
        self.assertEqual(
            data["subsite_footer"]["data"], self.subsite.subsite_footer.output
        )

    def test_expansion_expanded_empty_for_contents_outside_subsite(self):
        response = self.api_session.get(
            "{}?expand=subsite".format(self.document_outside_subsite.absolute_url())
        )
        result = response.json()
        data = result["@components"]["subsite"]

        self.assertEqual(data, {})

    def test_calling_expansion_directly_returns_data(self):
        response = self.api_session.get(
            "{}/@subsite".format(self.document_in_subsite.absolute_url())
        )
        data = response.json()

        self.assertEqual(data["@id"], self.subsite.absolute_url())
        self.assertEqual(data["@type"], self.subsite.portal_type)
        self.assertEqual(data["title"], self.subsite.title)
        self.assertEqual(data["description"], "")
        self.assertIn("image", data)
        self.assertIn("subsite_logo", data)
        self.assertEqual(data["subsite_css_class"], self.subsite.subsite_css_class)
        self.assertEqual(
            data["subsite_header"]["data"], self.subsite.subsite_header.output
        )
        self.assertEqual(
            data["subsite_footer"]["data"], self.subsite.subsite_footer.output
        )

    def test_calling_expansion_directly_returns_empty_data_outside_a_subsite(self):
        response = self.api_session.get(
            "{}/@subsite".format(self.document_outside_subsite.absolute_url())
        )
        data = response.json()

        self.assertEqual(data, {})
