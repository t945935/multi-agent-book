"""
第 1 章單元測試套件 (Chapter 1 Unit Tests)
零外掛依賴：直接使用 asyncio.run 執行異步測試，相容任何標準 pytest 環境。
"""

import asyncio
from agent_bus import MessageBus, MessageEnvelope, AgentState
from agents import PlannerAgent, CoderAgent, ReviewerAgent


def test_message_bus_routing():
    """測試訊息總線主題訂閱與路由機制"""
    async def _test():
        bus = MessageBus()
        received_messages = []

        async def custom_handler(msg: MessageEnvelope):
            received_messages.append(msg)

        bus.subscribe("test.topic", custom_handler)

        test_msg = MessageEnvelope(
            topic="test.topic",
            sender="sender_a",
            recipient="recipient_b",
            payload={"data": 123}
        )
        await bus.publish(test_msg)

        assert len(received_messages) == 1
        assert received_messages[0].payload["data"] == 123
        assert len(bus.get_history()) == 1

    asyncio.run(_test())


def test_multi_agent_pipeline():
    """測試完整協同流水線：Planner -> Coder -> Reviewer"""
    async def _test():
        bus = MessageBus()
        planner = PlannerAgent("planner", bus)
        coder = CoderAgent("coder", bus)
        reviewer = ReviewerAgent("reviewer", bus)

        bus.subscribe("task.plan", coder.handle_message)
        bus.subscribe("task.code", reviewer.handle_message)

        # 執行流程
        plan = await planner.step("測試任務")
        assert plan["status"] == "planned"

        code_res = await coder.step()
        assert code_res is not None
        assert "def solve" in code_res["code"]

        review_res = await reviewer.step()
        assert review_res is not None
        assert review_res["decision"] == "APPROVED"
        assert reviewer.state == AgentState.COMPLETED

    asyncio.run(_test())


def test_circuit_breaker():
    """測試審查輪數超過上限時的熔斷保護機制"""
    async def _test():
        bus = MessageBus()
        reviewer = ReviewerAgent("reviewer", bus, max_turns=1)

        # 模擬兩次審查請求
        msg1 = MessageEnvelope("task.code", "coder", "reviewer", {"task_id": "T-1"})
        msg2 = MessageEnvelope("task.code", "coder", "reviewer", {"task_id": "T-1"})

        await reviewer.handle_message(msg1)
        await reviewer.handle_message(msg2)

        res1 = await reviewer.step()
        assert res1["decision"] == "APPROVED"

        res2 = await reviewer.step()
        assert res2["decision"] == "APPROVED_BY_CIRCUIT_BREAKER"

    asyncio.run(_test())
