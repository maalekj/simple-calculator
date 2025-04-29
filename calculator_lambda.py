import json


def lambda_handler(event, context):
    # Support both REST API and HTTP API v2.0 structure
    method = event.get("httpMethod") or event.get("requestContext", {}).get(
        "http", {}
    ).get("method", "")

    if method not in ["GET", "POST"]:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": f"Method {method} not allowed"}),
        }

    try:
        if method == "GET":
            params = event.get("queryStringParameters") or {}
        else:  # POST
            params = json.loads(event.get("body") or "{}")

        num1 = float(params.get("num1"))
        num2 = float(params.get("num2"))
        operation = params.get("operation")

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                raise ValueError("Cannot divide by zero")
            result = num1 / num2
        else:
            raise ValueError("Invalid operation")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"num1": num1, "num2": num2, "operation": operation, "result": result}
            ),
        }

    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}
