import argparse
import requests

def read_usernames_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_passwords_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def main():
    parser = argparse.ArgumentParser(description='API Request Script')
    parser.add_argument('usernames_file', help='Path to the file containing usernames')
    parser.add_argument('passwords_file', help='Path to the file containing passwords')
    parser.add_argument('-o', '--output', help='Path to the output file', default='output.txt')
    args = parser.parse_args()

    base_url = 'https://t.service-now.com/api/now/table/sys_user'
    headers = {'Accept': 'application/json'}

    usernames = read_usernames_from_file(args.usernames_file)
    passwords = read_passwords_from_file(args.passwords_file)

    if len(usernames) != len(passwords):
        print("Error: The number of usernames and passwords must be the same.")
        return

    with open(args.output, 'w') as output_file:
        for username, password in zip(usernames, passwords):
            response = requests.get(base_url, params={'sysparm_query': f'user_name={username}'}, headers=headers, auth=(username, password))

            output_file.write(f"Username: {username} - Query: {username} - Response Code: {response.status_code}\n")

if __name__ == '__main__':
    main()
