"""
具體 Agent 角色實作 (Concrete Agent Implementations)
包含 PlannerAgent、CoderAgent 與 ReviewerAgent，具備狀態管理與熔斷機制。
"""

from __future__ import annotations
import asyncio
from typing import Any, Dict, Optional
from agent_bus import AgentState, MessageBus, MessageEnvelope


class BaseAgent:
    """Agent 抽象基底類別"""

    def __init__(self, name: str, bus: MessageBus):
        self.name = name
        self.bus = bus
        self.state = AgentState.IDLE
        self.inbox: asyncio.Queue[MessageEnvelope] = asyncio.Queue()

    async def handle_message(self, envelope: MessageEnvelope) -> None:
        """接收路由到該 Agent 的訊息"""
        if envelope.recipient in (self.name, "*"):
            await self.inbox.put(envelope)

    async def send(self, recipient: str, topic: str, payload: Dict[str, Any], reply_to: Optional[str] = None) -> None:
        """向總線發送訊息"""
        msg = MessageEnvelope(
            topic=topic,
            sender=self.name,
            recipient=recipient,
            payload=payload,
            reply_to=reply_to,
        )
        await self.bus.publish(msg)


class PlannerAgent(BaseAgent):
    """規劃代理 (負責將使用者需求拆解為具體步驟)"""

    async def step(self, prompt: str) -> Dict[str, Any]:
        self.state = AgentState.WORKING
        # 模擬任務拆解 (在真實場景中此處調用 LLM)
        plan = {
            "task_id": "T-001",
            "original_prompt": prompt,
            "steps": ["實作驗證模組", "加上型別註記", "編寫單元測試"],
            "status": "planned"
        }
        await self.send(
            recipient="coder",
            topic="task.plan",
            payload=plan
        )
        self.state = AgentState.IDLE
        return plan


class CoderAgent(BaseAgent):
    """代碼實作代理 (負責根據規劃生成代碼)"""

    async def step(self) -> Optional[Dict[str, Any]]:
        if self.inbox.empty():
            return None

        msg = await self.inbox.get()
        self.state = AgentState.WORKING

        plan = msg.payload
        # 模擬代碼產出
        code_artifact = {
            "task_id": plan["task_id"],
            "code": "def solve(x: int) -> int:\n    return x * 2\n",
            "version": 1
        }

        await self.send(
            recipient="reviewer",
            topic="task.code",
            payload=code_artifact,
            reply_to=msg.message_id
        )
        self.state = AgentState.IDLE
        return code_artifact


class ReviewerAgent(BaseAgent):
    """審查代理 (負責審查代碼品質並決定通過或退回修正)"""

    def __init__(self, name: str, bus: MessageBus, max_turns: int = 3):
        super().__init__(name, bus)
        self.max_turns = max_turns
        self.turn_count = 0

    async def step(self) -> Optional[Dict[str, Any]]:
        if self.inbox.empty():
            return None

        msg = await self.inbox.get()
        self.state = AgentState.WORKING
        self.turn_count += 1

        payload = msg.payload
        # 熔斷保護機制：若超過最大輪數強制中斷或通過
        if self.turn_count > self.max_turns:
            result = {
                "task_id": payload["task_id"],
                "decision": "APPROVED_BY_CIRCUIT_BREAKER",
                "notes": f"達到最大審查輪數 ({self.max_turns})，強制熔斷完成。"
            }
        else:
            result = {
                "task_id": payload["task_id"],
                "decision": "APPROVED",
                "notes": "型別註記完整，邏輯通過審查。"
            }

        await self.send(
            recipient="coordinator",
            topic="task.review",
            payload=result,
            reply_to=msg.message_id
        )
        self.state = AgentState.COMPLETED
        return result
