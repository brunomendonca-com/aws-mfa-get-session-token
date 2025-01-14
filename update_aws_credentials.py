#!/usr/bin/env python3

import json
import os
import subprocess
import configparser
from pathlib import Path

CREDENTIALS_PATH = os.getenv("AWS_SHARED_CREDENTIALS_FILE") or "~/.aws/credentials"


def get_long_term_credentials():
    """Read long term credentials from aws credentials file"""
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CREDENTIALS_PATH))
    return {
        'aws_access_key_id': config['default-long_term']['aws_access_key_id'],
        'aws_secret_access_key': config['default-long_term']['aws_secret_access_key']
    }


def update_credentials(credentials):
    """Update credentials file with new session credentials"""
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CREDENTIALS_PATH))
    config['default'] = {
        'aws_access_key_id': credentials['AccessKeyId'],
        'aws_secret_access_key': credentials['SecretAccessKey'],
        'aws_session_token': credentials['SessionToken']
    }

    with open(os.path.expanduser(CREDENTIALS_PATH), 'w') as f:
        config.write(f)


def run_aws_command(command):
    """Run AWS CLI command and return JSON response"""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"AWS command failed: {result.stderr}")
    return json.loads(result.stdout)


def main():
    long_term_credentials = get_long_term_credentials()
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CREDENTIALS_PATH))
    config['default'] = {
        'aws_access_key_id': long_term_credentials['aws_access_key_id'],
        'aws_secret_access_key': long_term_credentials['aws_secret_access_key']
    }
    with open(os.path.expanduser(CREDENTIALS_PATH), 'w') as f:
        config.write(f)

    # Get caller identity
    identity = run_aws_command(['aws', 'sts', 'get-caller-identity'])
    print("Current identity:", json.dumps(identity, indent=2))

    # Get MFA devices to retrieve the serial number
    mfa_devices = run_aws_command(['aws', 'iam', 'list-mfa-devices'])

    # Check the number of MFA devices
    if len(mfa_devices['MFADevices']) > 1:
        # List MFA devices and let the user choose one
        print("Available MFA devices:")
        for index, device in enumerate(mfa_devices['MFADevices']):
            print(f"{index + 1}: {device['SerialNumber']}")

        choice = int(
            input("Select the MFA device number you want to use: ")) - 1
        # Get the selected device's serial number
        serial_number = mfa_devices['MFADevices'][choice]['SerialNumber']
    else:
        # Use the only available MFA device
        serial_number = mfa_devices['MFADevices'][0]['SerialNumber']

    # Get MFA token from user
    token_code = input("Enter your MFA token code: ")

    # Get session token
    session = run_aws_command([
        'aws', 'sts', 'get-session-token',
        '--serial-number', serial_number,
        '--token-code', token_code
    ])

    # Update credentials file
    update_credentials(session['Credentials'])
    print("Credentials updated successfully!")


if __name__ == "__main__":
    main()
