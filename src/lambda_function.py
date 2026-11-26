from decimal import Decimal
import json
import os
import boto3


def get_table():
    """Connect to the DynamoDB resume table."""
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["RESUME_TABLE"]
    return dynamodb.Table(table_name)


def response(status_code, body):
    """Create a standard API Gateway response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body, default=str)
    }


def lambda_handler(event, context):
    """Handle requests for resume information."""

    try:
        method = event.get("httpMethod", "GET")
        path = event.get("path", "/")

        if method != "GET":
            return response(405, {"error": "Method not allowed"})

        routes = {
            "/personal": "PERSONAL",
            "/experience": "EXPERIENCE",
            "/education": "EDUCATION",
            "/skills": "SKILLS"
        }

        section = routes.get(path)

        if section is None:
            return response(404, {"error": "Endpoint not found"})

        table = get_table()

        result = table.get_item(
            Key={
                "PK": "RESUME",
                "SK": section
            }
        )

        item = result.get("Item")

        if item is None:
            return response(
                404,
                {"error": "Resume information not found"}
            )

        return response(200, item["data"])

    except Exception:
        print("Error processing resume API request")
        return response(
            500,
            {"error": "Internal server error"}
        )
