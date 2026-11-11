import unittest
from transit.engine import InterWarehouseTransitEngine


class TestInterWarehouseTransit(unittest.TestCase):
    def setUp(self):
        self.engine = InterWarehouseTransitEngine()

    def test_full_transit_reconciliation(self):
        # 100 units transferred from Delhi Central Hub to Bangalore Regional DC
        order = self.engine.dispatch_stock_transfer(
            source_wh="Central Hub - Delhi",
            target_wh="Regional DC - Bangalore",
            sku="CERAMIC-TILES-BOX",
            qty=100,
            unit_cost=500.0,
            transporter="VRL Logistics",
            lr_no="LR-882190",
            vehicle_no="KA-01-E-9912",
            freight_charge=5000.0,
            dispatch_date="2026-09-01"
        )
        self.assertEqual(order.status, "IN_TRANSIT")

        # Received: 95 sound, 5 broken in transit
        audit = self.engine.receive_and_reconcile_at_destination(
            transfer_id=order.transfer_id,
            received_sound_qty=95,
            damaged_or_lost_qty=5
        )
        self.assertEqual(audit.status, "RECEIVED_WITH_LOSS")
        self.assertEqual(audit.transit_loss_or_damaged_qty, 5)
        self.assertEqual(audit.total_transit_loss_value, 2500.0)  # 5 * 500
        self.assertTrue(audit.claim_against_transporter_eligible)
        self.assertGreater(audit.adjusted_unit_landed_cost, 500.0)  # freight absorbed


if __name__ == "__main__":
    unittest.main()
