import requests
import json
from datetime import datetime


USER_DETAILS = {
    "name": "Harshit Lodhi",
    "regNo": "300",  
    "email": "harshitlodhi220593@acropolis.in"
}

SQL_QUERY = """
SELECT 
    PAY.AMOUNT AS SALARY,
    CONCAT(E.FIRST_NAME, ' ', E.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURRENT_DATE, E.DOB)/365) AS AGE,
    D.DEPARTMENT_NAME
FROM PAYMENTS PAY
JOIN EMPLOYEE E ON PAY.EMP_ID = E.EMP_ID
JOIN DEPARTMENT D ON E.DEPARTMENT = D.DEPARTMENT_ID
WHERE DAY(PAY.PAYMENT_TIME) != 1
ORDER BY PAY.AMOUNT DESC
LIMIT 1;
""".strip()

# --- FUNCTION TO GENERATE WEBHOOK AND TOKEN ---
def generate_webhook():
    """
    Sends a POST request to generate the webhook and receive an access token.
    Returns:
        dict: Contains 'webhook' URL and 'accessToken'.
    """
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    try:
        print(f"Sending request to: {url}")
        print(f"With payload: {USER_DETAILS}")
        response = requests.post(url, json=USER_DETAILS)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(" X  Failed to generate webhook:", e)
        return None


def submit_solution(webhook_url, token):
    """
    Submit the SQL query to the webhook using the provided access token.
    Args:
        webhook_url (str): The URL to submit the query to.
        token (str): The access token for authentication.
    """
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "finalQuery": SQL_QUERY
    }
    try:
        print(f"Submitting to webhook: {webhook_url}")
        print(f"Using headers: {headers}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = requests.post(webhook_url, headers=headers, json=payload)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()
        print("Submission successful.")
        print("Response:", response.json())
    except Exception as e:
        print("Error, Failed to submit solution:", e)
        if 'response' in locals():
            try:
                print(f"Response text: {response.text}")
            except:
                pass

def main():
    """
    flow: generates webhook, retrieves token, and submits solution.
    """
    print("\n🚀 [{}] Starting application...".format(datetime.now()))

    result = generate_webhook()
    if result:
        webhook_url = result.get("webhook")
        token = result.get("accessToken")

        if webhook_url and token:
            print("\n🔗 Webhook URL:", webhook_url)
            print("🔐 Access Token:", token)
            print("\n📤 Submitting your SQL solution...")
            submit_solution(webhook_url, token)
        else:
            print("Caution: Webhook or token missing from response.")
    else:
        print("Error, Unable to proceed without webhook info.")

if __name__ == "__main__":
    main()
