"""Unit tests for agent-contract-net-auctioneer."""
import unittest
from agent_contract_net_auctioneer.auctioneer import ContractNetAuctioneer, AgentBid


class TestContractNetAuctioneer(unittest.TestCase):
    def setUp(self):
        self.auctioneer = ContractNetAuctioneer()

    def test_auction_flow(self):
        task = self.auctioneer.announce_task("t1", "Process logs", 100.0)
        bid1 = AgentBid("a1", "t1", 50.0, 1.0, 0.9)
        bid2 = AgentBid("a2", "t1", 20.0, 0.5, 0.95)

        self.assertTrue(self.auctioneer.submit_bid(bid1))
        self.assertTrue(self.auctioneer.submit_bid(bid2))

        award = self.auctioneer.close_auction("t1")
        self.assertIsNotNone(award)
        self.assertEqual(award.winning_agent_id, "a2")

    def test_over_budget_bid_rejected(self):
        self.auctioneer.announce_task("t2", "Expensive job", 50.0)
        bid = AgentBid("a1", "t2", 150.0, 0.1, 1.0)
        self.assertFalse(self.auctioneer.submit_bid(bid))
