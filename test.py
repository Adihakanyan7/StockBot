import re

message = "send me info about AAPL" # Replace this with the exact message you sent
print(message)
info_pattern = r"send me info about\s+([\w.]+)"
match_info = re.match(info_pattern, message)

add_pattern = r"add alert\s+([\w.]+)\s*,\s*([<>])\s*,\s*([\d.]+)"
add_match = re.match(add_pattern, message)

remove_pattern = r"remove alert\s+([\w.]+)\s+([<>])\s+([\d.]+)"
match_remove = re.match(remove_pattern, message)

print("Info Match:", match_info)
print("Add Match:", add_match)
print("Remove Match:", match_remove)
