from unittest import TestCase
from lxml import etree

from smartetailing.objects import WebOrder


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
