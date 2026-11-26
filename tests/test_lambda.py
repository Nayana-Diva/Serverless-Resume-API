
import os
import sys

import boto3
import pytest
from moto import mock_aws

sys.path.insert(0, os.path.abspath("src"))

from lambda_function import lambda_handler


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        os.environ["AWS_DEFAULT_REGION"] = "ap-south-1"
        os.environ["RESUME_TABLE"] = "TestResumeTable"

        dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")

        table = dynamodb.create_table(
            TableName="TestResumeTable",
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        sections = {
            "PERSONAL": {"name": "Nayana Gowda"},
            "EXPERIENCE": [],
            "EDUCATION": [{"degree": "BSc Computer Science"}],
            "SKILLS": {"programming": ["Python", "C++"]}
        }

        for section, data in sections.items():
            table.put_item(
                Item={"PK": "RESUME", "SK": section, "data": data}
            )

        yield table

        os.environ.pop("RESUME_TABLE", None)


@pytest.mark.parametrize(
    "path",
    ["/personal", "/experience", "/education", "/skills"]
)
def test_all_endpoints(path, dynamodb_table):
    result = lambda_handler(
        {"httpMethod": "GET", "path": path}, None
    )

    assert result["statusCode"] == 200


def test_personal_data(dynamodb_table):
    result = lambda_handler(
        {"httpMethod": "GET", "path": "/personal"}, None
    )

    assert result["statusCode"] == 200
    assert "Nayana Gowda" in result["body"]


def test_invalid_endpoint(dynamodb_table):
    result = lambda_handler(
        {"httpMethod": "GET", "path": "/invalid"}, None
    )

    assert result["statusCode"] == 404


def test_unsupported_method(dynamodb_table):
    result = lambda_handler(
        {"httpMethod": "POST", "path": "/personal"}, None
    )

    assert result["statusCode"] == 405
