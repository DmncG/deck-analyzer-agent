from email_demo.chains.notice_extraction import NOTICE_PARSER_CHAIN
from email_demo.example_emails import EMAILS
from email_demo.chains.escalation_check import ESCALATION_CHECK_CHAIN

escalation_criteria = """There is currently water leaks, water damage or potential water damage reported"""

message = """Several cracks in the foundation have been identified along with water leaks"""

escalation_result = ESCALATION_CHECK_CHAIN.invoke({"message": message, "escalation_criteria": escalation_criteria})
print(escalation_result)

result = NOTICE_PARSER_CHAIN.invoke({"message": EMAILS[0]})
print(result)