# Serverless Resume API on AWS

## Project Overview
A serverless Resume API built using AWS Lambda, Amazon API Gateway, and Amazon DynamoDB. It provides structured access to resume information through REST endpoints.

## Technologies
- Python 3.13
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- AWS SAM / CloudFormation
- Boto3
- Pytest and Moto

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /personal | Personal information |
| GET | /experience | Work experience |
| GET | /education | Education details |
| GET | /skills | Technical skills |

All endpoints require an API key when deployed using the provided infrastructure template.

## Project Structure
- `src/` - Lambda function and resume data loader
- `data/` - Resume JSON data
- `infrastructure/` - AWS deployment template
- `tests/` - Automated tests
- `documentation/` - Project documentation

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -v
```

## AWS Deployment
The infrastructure template provisions:
- AWS Lambda
- API Gateway
- DynamoDB
- API key and usage plan
- Request throttling and monthly quota

Deployment requires AWS CLI, AWS SAM CLI, and an AWS account configured with suitable permissions.

## Testing
The project uses Pytest and Moto to simulate DynamoDB operations locally.

**Test Result:** 7 tests passed.

## Security
- DynamoDB access is controlled through IAM permissions.
- API requests require an API key.
- API usage is limited through a usage plan.
- Resume data is stored in DynamoDB.

## Author
**Nayana Gowda**  
BSc Computer Science Student