"""
第 1 章範例執行入口 (Main Workflow Entrypoint)
展示 Planner -> Coder -> Reviewer 協同流程。
"""

from __future__ import annotations
import asyncio
from agent_bus import MessageBus
from agents import PlannerAgent, CoderAgent, ReviewerAgent


async def main() -> None:
    print("=" * 60)
    print("🚀 啟動多 Agent 協同最小原型系統 (Chapter 1)")
    print("=" * 60)

    # 1. 初始化訊息總線
    bus = MessageBus()

    # 2. 註冊各專業代理
    planner = PlannerAgent("planner", bus)
    coder = CoderAgent("coder", bus)
    reviewer = ReviewerAgent("reviewer", bus, max_turns=3)

    # 3. 綁定訊息路由訂閱
    bus.subscribe("task.plan", coder.handle_message)
    bus.subscribe("task.code", reviewer.handle_message)

    # 4. 發起使用者任務
    user_prompt = "請實作一個計算兩倍數值的函數，並完成審查"
    print(f"\n[使用者輸入] {user_prompt}\n")

    print("▶ 階段 1: Planner 開始任務規劃...")
    plan = await planner.step(user_prompt)
    print(f"  [Planner 產出步驟] {plan['steps']}")

    print("\n▶ 階段 2: Coder 接收規劃並生成代碼...")
    code_res = await coder.step()
    if code_res:
        print(f"  [Coder 代碼片段]\n{code_res['code'].strip()}")

    print("\n▶ 階段 3: Reviewer 執行審查...")
    review_res = await reviewer.step()
    if review_res:
        print(f"  [Reviewer 決策] {review_res['decision']} - {review_res['notes']}")

    print("\n" + "=" * 60)
    print("✅ 協同流水線成功完成！")
    print(f"總線記錄事件數: {len(bus.get_history())}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
