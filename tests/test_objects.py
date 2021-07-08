import json
from unittest import TestCase
from lxml import etree

from smartetailing.connection import SmartetailingConnection
from smartetailing.objects import WebOrder


def _get_connection():
    with open("config.json", "r") as fp:
        config = json.load(fp)["smartetailing"]
    return SmartetailingConnection(config["base_url"], config["merchant_id"], config["url_key"],
                                   config["web_url"], config["username"], config["password"])


class TestWebOrder(TestCase):
    def test_from_xml_collection(self):
        # Load the demo xml file
        with open("demo_export.xml", "r") as fid:
            order_xml = etree.XML("\n".join(fid.readlines()))
        # Parse it.
        orders = WebOrder().from_xml_collection(order_xml)
        # One order, me, 2 items, pickup at shop (but check address
        self.assertEqual(1, len(orders))
        order = orders[0].order
        self.assertIn("Scott Phillips", order.bill_address.name.full)
        self.assertIn("Curbside Pickup", order.shipping.method)
        self.assertEqual("888818539079", order.items[0].gtin1)
        self.assertEqual(444.13, order.order_total.total)

    def test_connect(self):
        connection = _get_connection()
        connection.export_orders_via_web()

    def test_download_orders(self):
        connection = _get_connection()
        self.assertTrue(len(list(connection.export_orders())) > 0)

