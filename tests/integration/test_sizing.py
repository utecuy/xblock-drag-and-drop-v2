from __future__ import division
import base64
from collections import namedtuple
import os.path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from xblockutils.resources import ResourceLoader

from .test_base import BaseIntegrationTest
from .test_interaction import InteractionTestBase

loader = ResourceLoader(__name__)


def _svg_to_data_uri(path):
    """ Convert an SVG image (by path) to a data URI """
    data_path = os.path.dirname(__file__) + "/data/"
    with open(data_path + path, "rb") as svg_fh:
        encoded = base64.b64encode(svg_fh.read())
    return "data:image/svg+xml;base64,{}".format(encoded)


Expectation = namedtuple('Expectation', [
    'item_id',
    'zone_id',
    'width_percent',  # we expect this item to have this width relative to its container (item bank or image target)
    'fixed_width_percent',  # we expect this item to have this width (always relative to the target image)
    'img_pixel_size_exact',  # we expect the image inside the draggable to have the exact size [w, h] in pixels
])
Expectation.__new__.__defaults__ = (None,) * len(Expectation._fields)  # pylint: disable=protected-access
ZONE_33 = "Zone 1/3"  # Title of top zone in each image used in these tests (33% width)
ZONE_50 = "Zone 50%"
ZONE_75 = "Zone 75%"
AUTO_MAX_WIDTH = 30  # Maximum width (as % of the parent container) for items with automatic sizing


class SizingTests(InteractionTestBase, BaseIntegrationTest):
    """
    Tests that cover features like draggable blocks with automatic sizes vs. specified sizes,
    different background image ratios, and responsive behavior.

    Tip: To see how these tests work, throw in an 'import time; time.sleep(200)' at the start of
    one of the tests, so you can check it out in the selenium browser window that opens.

    These tests intentionally do not use ddt in order to run faster. Instead, each test iterates
    through data and uses verbose assertion messages to clearly indicate where failures occur.
    """
    PAGE_TITLE = 'Drag and Drop v2 Sizing'
    PAGE_ID = 'drag_and_drop_v2_sizing'

    @staticmethod
    def _get_scenario_xml():
        """
        Set up the test scenario:
            * An upper dndv2 xblock with a wide image (1600x900 SVG)
              (on desktop and mobile, this background image will always fill the available width
                and should have the same width as the item bank above)
            * A lower dndv2 xblock with a small square image (500x500 SVG)
              (on desktop, the square image is not as wide as the item bank, but on mobile it
               may take up the whole width of the screen)
        """
        params = {
            "img": "wide",
            "img_wide_url": _svg_to_data_uri('dnd-bg-wide.svg'),
            "img_square_url": _svg_to_data_uri('dnd-bg-square.svg'),
            "img_400x300_url": _svg_to_data_uri('400x300.svg'),
            "img_200x200_url": _svg_to_data_uri('200x200.svg'),
            "img_60x60_url": _svg_to_data_uri('60x60.svg'),
        }
        upper_block = "<drag-and-drop-v2 data='{data}'/>".format(
            data=loader.render_django_template("data/test_sizing_template.json", params)
        )
        params["img"] = "square"
        lower_block = "<drag-and-drop-v2 data='{data}'/>".format(
            data=loader.render_django_template("data/test_sizing_template.json", params)
        )

        return "<vertical_demo>{}\n{}</vertical_demo>".format(upper_block, lower_block)

    EXPECTATIONS = [
        # The text 'Auto' with no fixed size specified should be 5-20% wide
        Expectation(item_id=0, zone_id=ZONE_33, width_percent=[5, 20]),
        # The long text with no fixed size specified should be wrapped at the maximum width
        Expectation(item_id=1, zone_id=ZONE_33, width_percent=AUTO_MAX_WIDTH),
        # The text items that specify specific widths as a percentage of the background image:
        Expectation(item_id=2, zone_id=ZONE_33, fixed_width_percent=33.3),
        Expectation(item_id=3, zone_id=ZONE_50, fixed_width_percent=50),
        Expectation(item_id=4, zone_id=ZONE_75, fixed_width_percent=75),
        # A 400x300 image with automatic sizing should be constrained to the maximum width
        Expectation(item_id=5, zone_id=ZONE_50, width_percent=AUTO_MAX_WIDTH),
        # A 200x200 image with automatic sizing
        Expectation(item_id=6, zone_id=ZONE_50, width_percent=[25, 30.2]),
        # A 400x300 image with a specified width of 50%
        Expectation(item_id=7, zone_id=ZONE_50, fixed_width_percent=50),
        # A 200x200 image with a specified width of 50%
        Expectation(item_id=8, zone_id=ZONE_50, fixed_width_percent=50),
        # A 60x60 auto-sized image should appear with pixel dimensions of 60x60 since it's
        # too small to be shrunk be the default max-size.
        Expectation(item_id=9, zone_id=ZONE_33, img_pixel_size_exact=[60, 60]),
    ]

    def test_wide_image_desktop(self):
        """ Test the upper, larger, wide image in a desktop-sized window """
        self._check_sizes(0, self.EXPECTATIONS)

    def test_square_image_desktop(self):
        """ Test the lower, smaller, square image in a desktop-sized window """
        self._check_sizes(1, self.EXPECTATIONS, expected_img_width=500)

    def _size_for_mobile(self):
        self.browser.set_window_size(375, 627)  # iPhone 6 viewport size
        wait = WebDriverWait(self.browser, 2)
        wait.until(lambda browser: browser.get_window_size()["width"] == 375)
        # Fix platform inconsistencies caused by scrollbar size:
        self.browser.execute_script('$("body").css("margin-right", "40px")')
        scrollbar_width = self.browser.execute_script(
            "var $outer = $('<div>').css({visibility: 'hidden', width: 100, overflow: 'scroll'}).appendTo('body');"
            "var widthWithScroll = $('<div>').css({width: '100%'}).appendTo($outer).outerWidth();"
            "$outer.remove();"
            "return 100 - widthWithScroll;"
        )
        self.browser.execute_script('$(".wrapper-workbench").css("margin-right", "-{}px")'.format(40 + scrollbar_width))
        # And reduce the wasted space around our XBlock in the workbench:
        self.browser.execute_script('return $(".workbench .preview").css("margin", "0")')

    def test_wide_image_mobile(self):
        """ Test the upper, larger, wide image in a mobile-sized window """
        self._size_for_mobile()
        self._check_sizes(0, self.EXPECTATIONS, is_desktop=False)

    def test_square_image_mobile(self):
        """ Test the lower, smaller, square image in a mobile-sized window """
        self._size_for_mobile()
        self._check_sizes(1, self.EXPECTATIONS, is_desktop=False)

    def _check_width(self, item_description, item, container_width, expected_percent):
        """
        Check that item 'item' has a width that is approximately the specified percentage
        of container_width, or if expected_percent is a pair of numbers, that it is within
        that range.
        """
        width_pixels = item.size["width"]
        width_percent = width_pixels / container_width * 100
        if isinstance(expected_percent, (list, tuple)):
            min_expected, max_expected = expected_percent
            msg = "{} should have width of {}% - {}%. Actual: {}px ({:.2f}% of {}px)".format(
                item_description, min_expected, max_expected, width_pixels, width_percent, container_width
            )
            self.assertGreaterEqual(width_percent, min_expected, msg)
            self.assertLessEqual(width_percent, max_expected, msg)
        else:
            self.assertAlmostEqual(
                width_percent, expected_percent, delta=1,
                msg="{} should have width of ~{}% (+/- 1%). Actual: {}px ({:.2f}% of {}px)".format(
                    item_description, expected_percent, width_pixels, width_percent, container_width
                )
            )

        if item.find_elements_by_css_selector("img"):
            # This item contains an image. The image should always fill the width of the draggable.
            image = item.find_element_by_css_selector("img")
            image_width_expected = item.size["width"] - 22
            self.assertAlmostEqual(
                image.size["width"], image_width_expected, delta=1,
                msg="{} image does not take up the full width of the draggable (width is {}px; expected {}px)".format(
                    item_description, image.size["width"], image_width_expected,
                )
            )

    def _check_img_pixel_dimensions(self, item_description, item, expect_w, expect_h):
        img_element = item.find_element_by_css_selector("img")
        self.assertEqual(
            img_element.size, {"width": expect_w, "height": expect_h},
            msg="Expected {}'s image to have exact dimensions {}x{}px; found {}x{}px instead.".format(
                item_description, expect_w, expect_h, img_element.size["width"], img_element.size["height"]
            )
        )

    def _check_sizes(self, block_index, expectations, expected_img_width=None, is_desktop=True):
        """ Test the actual dimensions that each draggable has, in the bank and when placed """
        # Check assumptions - the container wrapping this XBlock should be 770px wide
        self._switch_to_block(block_index)
        target_img = self._page.find_element_by_css_selector('.target-img')
        target_img_width = target_img.size["width"]
        item_bank = self._page.find_element_by_css_selector('.item-bank')
        item_bank_width = item_bank.size["width"]

        if is_desktop:
            # If using a desktop-sized window, we can know the exact dimensions of various containers:
            self.assertEqual(self._page.size["width"], 770)  # self._page is the .xblock--drag-and-drop div
            self.assertEqual(target_img_width, expected_img_width or 755)
            self.assertEqual(item_bank_width, 755)
        else:
            self.assertEqual(self._page.size["width"], 335)  # self._page is the .xblock--drag-and-drop div
            self.assertEqual(target_img_width, expected_img_width or 328)
            self.assertEqual(item_bank_width, 328)

        # Test each element, before it is placed (while it is in the item bank).
        for expect in expectations:
            if expect.width_percent is not None:
                self._check_width(
                    item_description="Unplaced item {}".format(expect.item_id),
                    item=self._get_unplaced_item_by_value(expect.item_id),
                    container_width=item_bank_width,
                    expected_percent=expect.width_percent,
                )
            if expect.fixed_width_percent is not None:
                self._check_width(
                    item_description="Unplaced item {} with fixed width".format(expect.item_id),
                    item=self._get_unplaced_item_by_value(expect.item_id),
                    container_width=target_img_width,
                    expected_percent=expect.fixed_width_percent,
                )
            if expect.img_pixel_size_exact is not None:
                self._check_img_pixel_dimensions(
                    "Unplaced item {}".format(expect.item_id),
                    self._get_unplaced_item_by_value(expect.item_id),
                    *expect.img_pixel_size_exact
                )

        # Test each element, after it it placed.
        for expect in expectations:
            self.place_item(expect.item_id, expect.zone_id, action_key=Keys.RETURN)
            expected_width_percent = expect.fixed_width_percent or expect.width_percent
            if expected_width_percent is not None:
                self._check_width(
                    item_description="Placed item {}".format(expect.item_id),
                    item=self._get_placed_item_by_value(expect.item_id),
                    container_width=target_img_width,
                    expected_percent=expected_width_percent,
                )
            if expect.img_pixel_size_exact is not None:
                self._check_img_pixel_dimensions(
                    "Placed item {}".format(expect.item_id),
                    self._get_placed_item_by_value(expect.item_id),
                    *expect.img_pixel_size_exact
                )


class SizingBackwardsCompatibilityTests(InteractionTestBase, BaseIntegrationTest):
    """
    Test backwards compatibility with data generated in older versions of this block.

    Older versions allowed authors to specify a fixed width and height for each draggable, in
    pixels (new versions only have a configurable width, and it is a percent width).
    """
    PAGE_TITLE = 'Drag and Drop v2 Sizing Backwards Compatibility'
    PAGE_ID = 'drag_and_drop_v2_sizing_backwards_compatibility'

    @staticmethod
    def _get_scenario_xml():
        """
        Set up the test scenario:
            * One DndDv2 block using 'old_version_data.json'
        """
        dnd_block = "<drag-and-drop-v2 data='{data}'/>".format(
            data=loader.load_unicode("data/old_version_data.json")
        )
        return "<vertical_demo>{}</vertical_demo>".format(dnd_block)

    def test_draggable_sizes(self):
        """ Test the fixed pixel widths set in old versions of the block """
        self._expect_width_px(item_id=0, width_px=190, zone_id="Zone 1")
        self._expect_width_px(item_id=1, width_px=190, zone_id="Zone 2")
        self._expect_width_px(item_id=2, width_px=100, zone_id="Zone 1")

    def _expect_width_px(self, item_id, width_px, zone_id):
        item = self._get_unplaced_item_by_value(item_id)
        self.assertEqual(item.size["width"], width_px)
        self.place_item(item_id, zone_id)
        item = self._get_placed_item_by_value(item_id)
        self.assertEqual(item.size["width"], width_px)
