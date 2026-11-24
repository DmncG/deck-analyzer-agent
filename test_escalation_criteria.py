from email_demo.chains.escalation_check import ESCALATION_CHECK_CHAIN
from email_demo.example_emails import EMAILS

ESCALATION_TEXT_CRITERIA = [
    "The notice explicitly mentions a risk of fire or water damage",
    "Any mention of fire hazard or water damage risk in the notice",
    "The notice describes a safety violation that could lead to fire or water damage",
    "the notice/message mentions/describes/states a possibility/risk that there is water damage",
]

message = EMAILS[0]

for criteria in ESCALATION_TEXT_CRITERIA:
    result = ESCALATION_CHECK_CHAIN.invoke(
        {"escalation_criteria": criteria, "message": message}
    )
    print(f"criteria: {criteria}")
    print(f"needs_escalation: {result.needs_escalation}")
    print(f"reasoning: {result.reasoning}")
    print("-" * 80)
