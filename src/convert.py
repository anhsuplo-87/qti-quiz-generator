# Tool: convert old JSON format to new schema (text + images support)

import os
import json
import argparse
from copy import deepcopy


def normalize_option(option):
    """
    Convert option to:
    {
        "text": "...",
        "images": []
    }
    """

    # Old format: string
    if isinstance(option, str):
        return {
            "text": option,
            "images": []
        }

    # Already dict
    if isinstance(option, dict):
        return {
            "text": option.get("text", ""),
            "images": option.get("images", []) or []
        }

    raise TypeError(f"Unsupported option format: {type(option)}")


def convert_json_schema(json_data):

    assert "bank" in json_data, "Missing 'bank' key"

    for item in json_data["bank"]:

        # Ensure question images exists
        if "images" not in item or item["images"] is None:
            item["images"] = []

        # Validate options
        assert isinstance(item["options"], list), "Item Options is not list"
        assert len(item["options"]
                   ) > 0, "Item Options doesn't have any answers"

        # Convert options
        item["options"] = [
            normalize_option(opt)
            for opt in item["options"]
        ]

    return json_data


if __name__ == "__main__":

    # Argument Parser
    parser = argparse.ArgumentParser(
        description="Convert old question JSON format to new format (text + images support)."
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input JSON file"
    )

    parser.add_argument(
        "-o", "--output",
        help="Path to output JSON file (ignored if --inplace is used)"
    )

    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Overwrite input file instead of creating a new one"
    )

    args = parser.parse_args()

    # Prepare input and output
    input_path = args.input

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not args.inplace and not args.output:
        parser.error("You must specify --output unless using --inplace")

    output_path = input_path if args.inplace else args.output

    # Convert
    with open(input_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    new_json = convert_json_schema(json_data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_json, f, indent=4, ensure_ascii=False)

    print("Convert completed successfully.")
