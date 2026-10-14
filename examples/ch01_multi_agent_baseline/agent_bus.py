"""
輕量級多 Agent 訊息總線 (Zero-dependency Multi-Agent Message Bus)
使用 Python 標準庫 (dataclasses, asyncio, enum) 實作事件契約與訊息路由。
"""

from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional
import uuid


class AgentState(str, Enum):
    IDLE = "IDLE"
    WORKING = "WORKING"
    WAITING_INPUT = "WAITING_INPUT"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


@dataclass
class MessageEnvelope:
    """結構化訊息信封 (Message Envelope Contract)"""
    topic: str
    sender: str
    recipient: str
    payload: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reply_to: Optional[str] = None


class MessageBus:
    """異步訊息路由中樞 (Asynchronous In-Memory Message Bus)"""

    def __init__(self, max_history: int = 1000):
        self._subscribers: Dict[str, List[Callable[[MessageEnvelope], Coroutine[Any, Any, None]]]] = {}
        self._history: List[MessageEnvelope] = []
        self._max_history = max_history
        self._lock = asyncio.Lock()

    def subscribe(self, topic: str, handler: Callable[[MessageEnvelope], Coroutine[Any, Any, None]]) -> None:
        """訂閱特定主題 (支援萬用字元 '*')"""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)

    async def publish(self, envelope: MessageEnvelope) -> None:
        """發布訊息至總線，分發給符合的主題訂閱者"""
        async with self._lock:
            self._history.append(envelope)
            if len(self._history) > self._max_history:
                self._history.pop(0)

        handlers = list(self._subscribers.get(envelope.topic, []))
        if envelope.topic != "*":
            handlers.extend(self._subscribers.get("*", []))

        # 並行分發給所有處理程序
        if handlers:
            await asyncio.gather(*(h(envelope) for h in handlers), return_exceptions=True)

    def get_history(self) -> List[MessageEnvelope]:
        return list(self._history)
