import json
from unittest import TestCase
from lxml import etree

from smartetailing.connection import SmartetailingConnection, get_dollars
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

    def test_money_parse(self):
        d1 = get_dollars("123")
        d2 = get_dollars("2,345")
        d3 = get_dollars("123.456")
        d4 = get_dollars("001,234.567")
        d5 = get_dollars("")

        self.assertEqual(123.0, d1)
        self.assertEqual(2345.0, d2)
        self.assertEqual(123.456, d3)
        self.assertEqual(1234.567, d4)
        self.assertEqual(0.0, d5)

    def test_download_orders(self):
        connection = _get_connection()
        self.assertTrue(len(list(connection.export_orders())) > 0)

