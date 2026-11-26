
import json
import os
from decimal import Decimal
from pathlib import Path

import boto3


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "resume.json"

SECTIONS = {
    "personal": "PERSONAL",
    "experience": "EXPERIENCE",
    "education": "EDUCATION",
    "skills": "SKILLS"
}


def load_resume():
    """Load resume data from the JSON source file."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Resume file not found: {DATA_FILE}")

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file, parse_float=Decimal)


def upload_resume():
    """Upload resume sections to DynamoDB."""

    table_name = os.environ.get("RESUME_TABLE")

    if not table_name:
        raise ValueError("RESUME_TABLE environment variable is required")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    resume = load_resume()

    for section, sort_key in SECTIONS.items():
        if section not in resume:
            raise ValueError(f"Missing resume section: {section}")

        table.put_item(
            Item={
                "PK": "RESUME",
                "SK": sort_key,
                "data": resume[section]
            }
        )

        print(f"Uploaded section: {section}")

    print("Resume data uploaded successfully.")


if __name__ == "__main__":
    upload_resume()
