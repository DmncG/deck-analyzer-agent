from email_demo.example_emails import EMAILS
from email_demo.graphs.notice_extraction import NOTICE_EXTRACTION_GRAPH

initial_state = {
    "notice_message": EMAILS[0],
    "notice_email_extract": None,
    "escalation_text_criteria": """There's a risk of fire or water damage at the site""",
    "escalation_dollar_criteria": 100_000,
    "requires_escalation": False,
    "escalation_emails": ["brog@abc.com", "bigceo@company.com"],
}

final_state = NOTICE_EXTRACTION_GRAPH.invoke(initial_state)

details = final_state["notice_email_extract"]

escalation_needed = final_state["requires_escalation"]

print(details, escalation_needed)