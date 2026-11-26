# System Architecture

## Overview
The Serverless Resume API provides resume information through REST endpoints using AWS services.

## Architecture Components
1. Amazon API Gateway: Receives HTTP GET requests and validates API keys.
2. AWS Lambda: Processes requests and retrieves resume information.
3. Amazon DynamoDB: Stores personal, experience, education, and skills data.
4. IAM: Controls Lambda access to DynamoDB.

## Request Flow
Client -> API Gateway -> Lambda -> DynamoDB -> Lambda -> API Gateway -> Client

## Security
- API key authentication.
- IAM-based access control.
- API request throttling.
- Monthly request quota.

## Error Handling
- 200: Successful request.
- 404: Resource not found.
- 405: Unsupported HTTP method.
- 500: Internal server error.

## Testing
Pytest and Moto simulate DynamoDB operations locally.

Result: 7 tests passed.
