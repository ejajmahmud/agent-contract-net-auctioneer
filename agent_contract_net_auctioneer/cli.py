"""CLI for agent-contract-net-auctioneer."""
import sys
import argparse
from .auctioneer import ContractNetAuctioneer, AgentBid


def main():
    parser = argparse.ArgumentParser(description="Agent Contract Net Auctioneer CLI")
    parser.add_argument("--demo", action="store_true", help="Run contract net task auction demo")
    args = parser.parse_args()

    if args.demo:
        auctioneer = ContractNetAuctioneer()
        task = auctioneer.announce_task("task_rag_query", "Execute vector search & re-rank", max_cost=50.0)
        print(f"Announced Task: {task.task_id} (Max Cost: {task.max_cost})")

        auctioneer.submit_bid(AgentBid("agent_fast", task.task_id, bid_cost=30.0, estimated_latency_sec=0.2, confidence=0.85))
        auctioneer.submit_bid(AgentBid("agent_accurate", task.task_id, bid_cost=45.0, estimated_latency_sec=1.1, confidence=0.99))

        award = auctioneer.close_auction(task.task_id)
        if award:
            print(f"Auction Closed! Winning Agent: {award.winning_agent_id}")
            print(f"  Contract ID: {award.contract_id} | Winning Cost: {award.winning_bid.bid_cost}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
