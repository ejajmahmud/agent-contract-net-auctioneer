"""Core Contract Net Auctioneer implementation."""
import time
import uuid
from typing import Dict, List, Optional, Any


class TaskCall:
    def __init__(self, task_id: str, description: str, max_cost: float, timeout_seconds: float = 5.0):
        self.task_id = task_id
        self.description = description
        self.max_cost = max_cost
        self.timeout_seconds = timeout_seconds
        self.created_at = time.time()


class AgentBid:
    def __init__(self, agent_id: str, task_id: str, bid_cost: float, estimated_latency_sec: float, confidence: float):
        self.agent_id = agent_id
        self.task_id = task_id
        self.bid_cost = bid_cost
        self.estimated_latency_sec = estimated_latency_sec
        self.confidence = confidence  # 0.0 to 1.0


class ContractAward:
    def __init__(self, contract_id: str, task_id: str, winning_agent_id: str, winning_bid: AgentBid):
        self.contract_id = contract_id
        self.task_id = task_id
        self.winning_agent_id = winning_agent_id
        self.winning_bid = winning_bid
        self.is_completed = False
        self.result: Any = None


class ContractNetAuctioneer:
    def __init__(self):
        self.tasks: Dict[str, TaskCall] = {}
        self.bids: Dict[str, List[AgentBid]] = {}
        self.awards: Dict[str, ContractAward] = {}

    def announce_task(self, task_id: str, description: str, max_cost: float, timeout_seconds: float = 5.0) -> TaskCall:
        task = TaskCall(task_id, description, max_cost, timeout_seconds)
        self.tasks[task_id] = task
        self.bids[task_id] = []
        return task

    def submit_bid(self, bid: AgentBid) -> bool:
        if bid.task_id not in self.tasks:
            return False
        task = self.tasks[bid.task_id]
        if bid.bid_cost > task.max_cost:
            return False
        self.bids[bid.task_id].append(bid)
        return True

    def close_auction(self, task_id: str) -> Optional[ContractAward]:
        if task_id not in self.tasks or not self.bids.get(task_id):
            return None

        task = self.tasks[task_id]
        valid_bids = self.bids[task_id]

        # Multi-objective scoring: higher confidence, lower cost, lower latency
        def score_bid(b: AgentBid) -> float:
            cost_factor = 1.0 - (b.bid_cost / max(1.0, task.max_cost))
            latency_factor = 1.0 / (1.0 + b.estimated_latency_sec)
            return (b.confidence * 0.5) + (cost_factor * 0.3) + (latency_factor * 0.2)

        best_bid = max(valid_bids, key=score_bid)
        contract_id = f"cnt_{uuid.uuid4().hex[:8]}"
        award = ContractAward(contract_id, task_id, best_bid.agent_id, best_bid)
        self.awards[contract_id] = award
        return award

    def complete_contract(self, contract_id: str, result: Any) -> bool:
        if contract_id in self.awards:
            self.awards[contract_id].is_completed = True
            self.awards[contract_id].result = result
            return True
        return False
