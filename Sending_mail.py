#!/usr/bin/env python3
"""
Enhanced Email Sender from CSV
Automate bulk email outreach with improved security, error handling, and features.

Author: Quang-Ng-Duong (Enhanced)
"""

import csv
import os
import sys
import time
import logging
import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from tqdm import tqdm

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables only.")


class EmailSenderConfig:
    """Configuration class for email sender."""

    def __init__(self):
        self.email_address = os.getenv('EMAIL_ADDRESS', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.default_subject = os.getenv('DEFAULT_SUBJECT', 'Explore Vietnam')
        self.rate_limit_delay = float(os.getenv('RATE_LIMIT_DELAY', '1.0'))

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.email_address or not self.email_password:
            return False
        if not self._is_valid_email(self.email_address):
            return False
        return True

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class EmailSender:
    """Enhanced email sender with improved error handling and features."""

    def __init__(self, config: EmailSenderConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.smtp_connection: Optional[smtplib.SMTP] = None

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger('EmailSender')
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # File handler
        file_handler = logging.FileHandler(log_dir / 'email_sender.log')
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter - uses standard Python logging format attributes
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def connect_smtp(self) -> bool:
        """Establish SMTP connection with error handling."""
        try:
            self.logger.info(f"Connecting to SMTP server: {self.config.smtp_server}:{self.config.smtp_port}")
            self.smtp_connection = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            self.smtp_connection.ehlo()
            self.smtp_connection.starttls()
            self.smtp_connection.ehlo()

            self.logger.info("Authenticating with email credentials...")
            self.smtp_connection.login(self.config.email_address, self.config.email_password)
            self.logger.info("Successfully connected and authenticated!")
            return True

        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"Authentication failed: {e}")
            return False
        except smtplib.SMTPConnectError as e:
            self.logger.error(f"Connection failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during SMTP connection: {e}")
            return False

    def disconnect_smtp(self):
        """Safely disconnect from SMTP server."""
        if self.smtp_connection:
            try:
                self.smtp_connection.quit()
                self.logger.info("SMTP connection closed successfully")
            except Exception as e:
                self.logger.warning(f"Error closing SMTP connection: {e}")
            finally:
                self.smtp_connection = None

    def load_email_list(self, csv_file: str) -> List[Dict[str, str]]:
        """Load and validate email list from CSV file."""
        email_list = []

        if not Path(csv_file).exists():
            self.logger.error(f"CSV file not found: {csv_file}")
            return email_list

        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file_handle:
                # Try to detect if file has headers
                sample = csv_file_handle.read(1024)
                csv_file_handle.seek(0)

                # Check if first line looks like headers
                first_line = csv_file_handle.readline().strip()
                csv_file_handle.seek(0)

                has_header = 'email' in first_line.lower() or '@' not in first_line

                reader = csv.DictReader(csv_file_handle) if has_header else csv.reader(csv_file_handle)

                for row_num, row in enumerate(reader, 1):
                    try:
                        if isinstance(row, dict):
                            # DictReader case
                            email = row.get('email', '').strip()
                            name = row.get('name', '').strip()
                        else:
                            # Regular reader case
                            email = row[0].strip() if row else ''
                            name = row[1].strip() if len(row) > 1 else ''

                        if email and self.config._is_valid_email(email):
                            email_list.append({
                                'email': email,
                                'name': name or email.split('@')[0]
                            })
                        elif email:
                            self.logger.warning(f"Invalid email format at row {row_num}: {email}")

                    except Exception as e:
                        self.logger.warning(f"Error processing row {row_num}: {e}")

        except Exception as e:
            self.logger.error(f"Error reading CSV file: {e}")

        self.logger.info(f"Loaded {len(email_list)} valid email addresses")
        return email_list

    def create_message(self, subject: str, body: str, recipient_email: str,
                      recipient_name: str = "", html_body: str = "",
                      attachments: List[str] = None) -> EmailMessage:
        """Create email message with optional HTML and attachments."""

        if html_body or attachments:
            message = MIMEMultipart('alternative')
        else:
            message = EmailMessage()

        # Personalize the message
        personalized_body = body.replace('{name}', recipient_name or recipient_email.split('@')[0])
        personalized_subject = subject.replace('{name}', recipient_name or recipient_email.split('@')[0])

        message['Subject'] = personalized_subject
        message['From'] = self.config.email_address
        message['To'] = recipient_email

        if isinstance(message, MIMEMultipart):
            # Add text part
            text_part = MIMEText(personalized_body, 'plain', 'utf-8')
            message.attach(text_part)

            # Add HTML part if provided
            if html_body:
                personalized_html = html_body.replace('{name}', recipient_name or recipient_email.split('@')[0])
                html_part = MIMEText(personalized_html, 'html', 'utf-8')
                message.attach(html_part)

            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {Path(file_path).name}'
                            )
                            message.attach(part)
                    else:
                        self.logger.warning(f"Attachment not found: {file_path}")
        else:
            message.set_content(personalized_body)

        return message

    def send_bulk_emails(self, email_list: List[Dict[str, str]], subject: str,
                        body: str, html_body: str = "", attachments: List[str] = None,
                        dry_run: bool = False) -> Dict[str, int]:
        """Send bulk emails with progress tracking and error handling."""

        results = {'sent': 0, 'failed': 0, 'skipped': 0}

        if not email_list:
            self.logger.warning("No valid email addresses to send to")
            return results

        if dry_run:
            self.logger.info(f"DRY RUN: Would send {len(email_list)} emails")
            for recipient in email_list:
                self.logger.info(f"Would send to: {recipient['email']} ({recipient['name']})")
            return results

        if not self.connect_smtp():
            self.logger.error("Failed to connect to SMTP server")
            return results

        try:
            self.logger.info(f"Starting to send {len(email_list)} emails...")

            with tqdm(total=len(email_list), desc="Sending emails") as progress_bar:
                for recipient in email_list:
                    try:
                        message = self.create_message(
                            subject=subject,
                            body=body,
                            recipient_email=recipient['email'],
                            recipient_name=recipient['name'],
                            html_body=html_body,
                            attachments=attachments
                        )

                        self.smtp_connection.send_message(message)
                        results['sent'] += 1
                        self.logger.info(f"✓ Sent to {recipient['email']}")

                        # Rate limiting
                        time.sleep(self.config.rate_limit_delay)

                    except smtplib.SMTPRecipientsRefused as e:
                        results['failed'] += 1
                        self.logger.error(f"✗ Recipient refused {recipient['email']}: {e}")
                    except smtplib.SMTPDataError as e:
                        results['failed'] += 1
                        self.logger.error(f"✗ Data error for {recipient['email']}: {e}")
                    except Exception as e:
                        results['failed'] += 1
                        self.logger.error(f"✗ Unexpected error for {recipient['email']}: {e}")

                    progress_bar.update(1)
                    progress_bar.set_postfix({
                        'Sent': results['sent'],
                        'Failed': results['failed']
                    })

        finally:
            self.disconnect_smtp()

        self.logger.info(f"Email sending completed. Sent: {results['sent']}, Failed: {results['failed']}")
        return results


def load_template(template_file: str) -> Tuple[str, str]:
    """Load email template from file."""
    if not Path(template_file).exists():
        return "", ""

    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple template format: subject and body separated by ---
        if '---' in content:
            parts = content.split('---', 1)
            subject = parts[0].strip()
            body = parts[1].strip()
        else:
            subject = ""
            body = content.strip()

        return subject, body
    except Exception as e:
        print(f"Error loading template: {e}")
        return "", ""


def create_sample_files():
    """Create sample configuration and template files."""

    # Create sample CSV
    sample_csv = """email,name
john.doe@example.com,John Doe
jane.smith@example.com,Jane Smith
vietnam.lover@example.com,Vietnam Enthusiast"""

    with open('sample_emails.csv', 'w', encoding='utf-8') as f:
        f.write(sample_csv)

    # Create sample template
    sample_template = """Discover the Beauty of Vietnam, {name}!
---
Dear {name},

Vietnam is a country located in Southeast Asia, known for its diverse landscapes and rich culture.

Vietnam is also famous for its unique cuisine, from pho and banh mi to regional specialties.

The country's folk culture, traditional festivals, and warm hospitality make it a truly special destination.

We hope you'll consider visiting Vietnam soon!

Best regards,
Vietnam Tourism Team"""

    with open('vietnam_template.txt', 'w', encoding='utf-8') as f:
        f.write(sample_template)

    print("Sample files created:")
    print("- sample_emails.csv")
    print("- vietnam_template.txt")
    print("- .env.example (configure with your credentials)")


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(description='Enhanced Email Sender from CSV')
    parser.add_argument('--csv', default='emails.csv', help='CSV file with email addresses')
    parser.add_argument('--subject', help='Email subject (overrides template)')
    parser.add_argument('--body', help='Email body (overrides template)')
    parser.add_argument('--template', help='Template file to use')
    parser.add_argument('--html-template', help='HTML template file')
    parser.add_argument('--attachments', nargs='*', help='Files to attach')
    parser.add_argument('--dry-run', action='store_true', help='Test run without sending emails')
    parser.add_argument('--create-samples', action='store_true', help='Create sample files')

    args = parser.parse_args()

    if args.create_samples:
        create_sample_files()
        return

    # Load configuration
    config = EmailSenderConfig()

    if not config.validate():
        print("❌ Configuration validation failed!")
        print("Please check your .env file or environment variables:")
        print("- EMAIL_ADDRESS: Your Gmail address")
        print("- EMAIL_PASSWORD: Your Gmail app password")
        print("\nRun with --create-samples to create example files.")
        sys.exit(1)

    # Initialize email sender
    sender = EmailSender(config)

    # Load email list
    email_list = sender.load_email_list(args.csv)
    if not email_list:
        print(f"❌ No valid email addresses found in {args.csv}")
        sys.exit(1)

    # Determine subject and body
    subject = args.subject or config.default_subject
    body = args.body or ""
    html_body = ""

    # Load template if specified
    if args.template:
        template_subject, template_body = load_template(args.template)
        if not args.subject and template_subject:
            subject = template_subject
        if not args.body and template_body:
            body = template_body

    # Load HTML template if specified
    if args.html_template:
        _, html_body = load_template(args.html_template)

    # Use default body if none provided
    if not body:
        body = """Vietnam is a country located in Southeast Asia,
known for its diverse landscapes and rich culture.

Vietnam is also famous for its unique cuisine,
from pho and banh mi (Vietnamese sandwiches) to regional specialties.

The country's folk culture, traditional festivals make it truly special."""

    print(f"📧 Preparing to send emails to {len(email_list)} recipients")
    print(f"📝 Subject: {subject}")

    if args.dry_run:
        print("🧪 DRY RUN MODE - No emails will be sent")

    # Send emails
    results = sender.send_bulk_emails(
        email_list=email_list,
        subject=subject,
        body=body,
        html_body=html_body,
        attachments=args.attachments or [],
        dry_run=args.dry_run
    )

    print(f"\n✅ Email sending completed!")
    print(f"📊 Results: {results['sent']} sent, {results['failed']} failed")


if __name__ == "__main__":
    main()