from typing import Any
from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    hook_config
)
from langchain.messages import AIMessage, HumanMessage
from langgraph.runtime import Runtime
from langgraph.types import interrupt
from src.schema import HitlDecision, PlanOutput
from src.utils import logger


class ApprovePlanState(AgentState):
    plan: PlanOutput


class ApprovePlan(AgentMiddleware):
    """Human-in-the-loop middleware after agent execution.
    User can approve, edit or ask for revise the plan.
    After this workflow jump back to model"""
    @hook_config(can_jump_to=["model", "end"])
    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        logger.info("Fallback into HITL")

        filesystem = state.get("files", {})
        plan_file = filesystem.get("/workspace/plan_draft.md", {})
        plan = plan_file.get("content", "")
        if not plan:
            plan = state['messages'][-1].content


        decision: HitlDecision = interrupt({
            "question": "Approve this plan?",
            "details": plan,
            "options": ["approve", "revise", "edit"]
        })

        if decision.get("action") == "approve":
            logger.info("Approve the plan")
            return {
                "files":{
                    "/workspace/plan_draft.md":
                        {"content":
                             plan}
                }
            }

        elif decision.get("action") == "revise":
            logger.info("Revise the plan")
            user_feedback = decision.get("feedback", "")
            return {
                "messages": [
                    HumanMessage(content=f"Revise the plan based on this feedback: {user_feedback}")
                ],
                "jump_to": "model"
            }

        elif decision.get("action") == "edit":
            logger.info("Edit the plan")
            user_feedback = decision.get("feedback", "")
            return {
                "files": {
                    "/workspace/plan_draft.md":
                        {"content":
                             user_feedback}
                },
                "messages": [
                    AIMessage(content=user_feedback)
                ]
            }