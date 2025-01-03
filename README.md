# AWS MFA Session Token Updater

A simple Python script to update AWS credentials using MFA (Multi-Factor Authentication). This tool helps you manage temporary session credentials when MFA is required for AWS CLI access.

## Prerequisites

1. Python 3.6 or higher
2. AWS CLI v2 installed and configured
    - Install from: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
3. MFA device configured in your AWS IAM account
4. **IMPORTANT**: Your AWS credentials must be stored in `~/.aws/credentials` with the following format:
    ```ini
    [default-long_term]
    aws_access_key_id = YOUR_ACCESS_KEY_ID
    aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
    ```

## Installation

1. Clone this repository
2. Make the script executable:
    ```bash
    chmod +x update_aws_credentials.py
    ```

## Usage

1. Run the script:

    ```bash
    ./update_aws_credentials.py
    ```

2. The script will:
    - Read your original access key and secret key from `~/.aws/credentials`
    - Get your AWS identity information
    - List your MFA devices (if you have multiple)
    - Prompt for your MFA token code
    - Update your `~/.aws/credentials` file with the new temporary session credentials

## Security Considerations

1. Never commit AWS credentials to Github
2. Keep your `~/.aws/credentials` files secure with appropriate permissions
3. Always use MFA for enhanced security
4. Regularly rotate your AWS access keys

## Troubleshooting

1. If you get permission errors:

    - Check your AWS credentials are correctly configured
    - Verify your MFA device is properly set up
    - Ensure you have these IAM permissions: getCallerIdentity, listMfaDevices, getSessionToken.

2. If the script fails to run:
    - Ensure Python 3.6+ is installed
    - Verify AWS CLI is installed and configured
    - Check file permissions

## License

MIT License - See LICENSE file for details
