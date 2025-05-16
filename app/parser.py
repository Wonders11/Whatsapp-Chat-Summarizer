import re
from datetime import datetime

def parse_whatsapp_chat(file_content):
    chat_lines = file_content.split("\n")
    messages = []
    # Regex: Date [MM/DD/YY], Time with optional special spaces + AM/PM, sender, message
    pattern = r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s([\d:]+)\s*([APMapm]{2})\]\s(.+?):\s(.+)"
    
    for line in chat_lines:
        match = re.match(pattern, line)
        if match:
            date_str, time_str, am_pm, sender, message = match.groups()
            
            # Clean spaces/unicode in time
            clean_time_str = time_str.replace('\u202f', '').replace('\xa0', '').strip()
            datetime_str = f"{date_str} {clean_time_str} {am_pm.upper()}"
            
            # Try parsing with multiple date formats for robustness
            for fmt in ["%m/%d/%y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p"]:
                try:
                    timestamp = datetime.strptime(datetime_str, fmt)
                    messages.append({
                        "timestamp": timestamp,
                        "sender": sender,
                        "message": message
                    })
                    break
                except ValueError:
                    continue
    return messages
