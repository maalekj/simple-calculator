import json


def respond(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    method = event.get("httpMethod") or event.get("requestContext", {}).get(
        "http", {}
    ).get("method", "")

    if method == "OPTIONS":
        return respond(200, {})  # Preflight CORS support

    if method not in ["GET", "POST"]:
        return respond(405, {"error": f"Method {method} not allowed"})

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

        return respond(
            200, {"num1": num1, "num2": num2, "operation": operation, "result": result}
        )

    except Exception as e:
        return respond(400, {"error": str(e)})
