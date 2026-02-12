# Tool for convert option text to new text+image anwser (version)

import json
json_data = json.load(
    open("json-sample/sample_question.json", 'r', encoding="utf-8"))
for item in json_data["bank"]:
    assert isinstance(item["options"], list), "Item Options is not list"
    assert len(item["options"]) > 0, "Item Options doesn't have any answers"

    if isinstance(item["options"][0], str):
        item["options"] = [{"text": opt, "images": []}
                           for opt in item["options"]]
print(json.dumps(json_data, indent=4))
