import re

def email_from_formatter(msg_from):
    regex = '<(.*)>'
    result = re.search(regex , msg_from)
    return result.group(0).strip('<>')