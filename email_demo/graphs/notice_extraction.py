from typing import Optional, TypedDict
from email_demo.chains.escalation_check import ESCALATION_CHECK_CHAIN
from email_demo.chains.notice_extraction import NOTICE_PARSER_CHAIN, NoticeEmailExtract
from langgraph.graph import END, START, StateGraph
from pydantic import EmailStr
from email_demo.utils.graph_utils import create_legal_ticket, send_escalation_email
from email_demo.utils.logging_config import LOGGER

class GraphState(TypedDict):
    notice_message: str
    notice_email_extract: Optional[NoticeEmailExtract]
    escalation_text_criteria: str
    escalation_dollar_criteria: float
    requires_escalation: bool
    escalation_emails: Optional[list[EmailStr]]
    follow_ups: Optional[dict[str, bool]]
    current_follow_up: Optional[str]

workflow = StateGraph(GraphState)

def parse_notice_message_node(state: GraphState) -> GraphState:
    """Use the notice parser chain to extract fields from the notice"""
    LOGGER.info("Parsing notice...")
    notice_email_extract = NOTICE_PARSER_CHAIN.invoke(
        {"message": state["notice_message"]}
    )
    state["notice_email_extract"] = notice_email_extract
    return state

def check_escalation_status_node(state: GraphState) -> GraphState:
    """Determine whether a notice needs escalation"""
    LOGGER.info("Determining escalation status...")
    text_check = ESCALATION_CHECK_CHAIN.invoke(
        {
            "escalation_criteria": state["escalation_text_criteria"],
            "message": state["notice_message"],
        }
    ).needs_escalation

    if (
        text_check
        or (state["notice_email_extract"].max_potential_fine or 0)
        >= state["escalation_dollar_criteria"]
    ):
        state["requires_escalation"] = True
    else:
        state["requires_escalation"] = False

    return state

def send_escalation_email_node(state: GraphState) -> GraphState:
    """Send an escalation email"""
    send_escalation_email(
        notice_email_extract=state["notice_email_extract"],
        escalation_emails=state["escalation_emails"],
    )
    return state

def create_legal_ticket_node(state: GraphState) -> GraphState:
    """Node to create a legal ticket"""
    follow_up = create_legal_ticket(
        current_follow_ups=state.get("follow_ups"),
        notice_email_extract=state["notice_email_extract"],
    )
    state["current_follow_up"] = follow_up
    return state

def route_escalation_status_edge(state: GraphState) -> str:
    """Determine whether to send an escalation email or
    create a legal ticket"""
    if state["requires_escalation"]:
        LOGGER.info("Escalation needed!")
        return "send_escalation_email"

    LOGGER.info("No escalation needed")
    return "create_legal_ticket"

workflow.add_node("parse_notice_message", parse_notice_message_node)
workflow.add_node("check_escalation_status", check_escalation_status_node)
workflow.add_node("send_escalation_email", send_escalation_email_node)
workflow.add_node("create_legal_ticket", create_legal_ticket_node)

workflow.add_edge(START, "parse_notice_message")
workflow.add_edge("parse_notice_message", "check_escalation_status")
workflow.add_conditional_edges(
    "check_escalation_status",
    route_escalation_status_edge,
    {
        "send_escalation_email": "send_escalation_email",
        "create_legal_ticket": "create_legal_ticket",
    },
)
workflow.add_edge("send_escalation_email", "create_legal_ticket")
workflow.add_edge("create_legal_ticket", END)

NOTICE_EXTRACTION_GRAPH = workflow.compile()