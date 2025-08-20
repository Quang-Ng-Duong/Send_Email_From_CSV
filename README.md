# 📧 Enhanced Email Sender from CSV

*Automate Outreach, Amplify Impact Instantly - Now with Advanced Features!*

![Last Commit](https://img.shields.io/badge/last%20commit-december%202024-blue)
![Language](https://img.shields.io/badge/python-100%25-blue)
![Version](https://img.shields.io/badge/version-2.0-green)

*Built with modern Python and enhanced security:*
![Python](https://img.shields.io/badge/-Python-blue?logo=python)
![Security](https://img.shields.io/badge/-Security-red?logo=shield)
![Templates](https://img.shields.io/badge/-Templates-purple?logo=template)

---

## 🚀 What's New in Version 2.0

- ✅ **Enhanced Security**: Environment variables and .env file support
- ✅ **Advanced Error Handling**: Comprehensive logging and error recovery
- ✅ **Email Templates**: Support for text and HTML templates with personalization
- ✅ **Progress Tracking**: Real-time progress bars and detailed reporting
- ✅ **Rate Limiting**: Built-in protection against Gmail rate limits
- ✅ **CLI Interface**: Command-line interface for easy automation
- ✅ **Attachment Support**: Send files with your emails
- ✅ **Dry Run Mode**: Test your campaigns before sending
- ✅ **Better CSV Handling**: Support for headers and validation

---

## Table of Contents

- [🚀 What's New in Version 2.0](#-whats-new-in-version-20)
- [📋 Overview](#-overview)
- [🛠️ Getting Started](#️-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Quick Start](#quick-start)
- [📖 Usage](#-usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Features](#advanced-features)
  - [Command Line Options](#command-line-options)
- [📁 File Formats](#-file-formats)
- [🔧 Configuration](#-configuration)
- [🧪 Testing](#-testing)
- [📊 Examples](#-examples)
- [🔒 Security](#-security)
- [🐛 Troubleshooting](#-troubleshooting)

---

## 📋 Overview

**Enhanced Email Sender from CSV** is a professional-grade tool that automates bulk email outreach through Gmail's SMTP server. This enhanced version provides enterprise-level features while maintaining simplicity and ease of use.

### 🌟 Key Features

- 🔐 **Secure Credential Management**: Environment variables and .env file support
- 📧 **Smart Email Delivery**: Intelligent retry logic and rate limiting
- 🎨 **Template System**: Rich text and HTML templates with personalization
- 📊 **Progress Tracking**: Real-time progress bars and detailed statistics
- 🛡️ **Error Handling**: Comprehensive error handling and logging
- 📎 **Attachment Support**: Send files with your emails
- 🧪 **Testing Mode**: Dry run capability for safe testing
- 📈 **Reporting**: Detailed success/failure reporting
- 🔄 **Batch Processing**: Handle large email lists efficiently

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.7+**
- **Gmail Account** with App Password enabled
- **Internet Connection**

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Quang-Ng-Duong/Send_Email_From_CSV
   cd Send_Email_From_CSV
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create sample files** (optional):

   ```bash
   python Sending_mail.py --create-samples
   ```

### Configuration

1. **Copy the example environment file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials**:

   ```env
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   DEFAULT_SUBJECT=Explore Vietnam
   RATE_LIMIT_DELAY=1.0
   ```

3. **Enable Gmail App Passwords**:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate an app password for this application

### Quick Start

1. **Prepare your email list** (`emails.csv`):

   ```csv
   email,name
   john@example.com,John Doe
   jane@example.com,Jane Smith
   ```

2. **Send emails**:

   ```bash
   python Sending_mail.py --csv emails.csv
   ```

3. **Test first** (recommended):

   ```bash
   python Sending_mail.py --csv emails.csv --dry-run
   ```

---

## 📖 Usage

### Basic Usage

```bash
# Send emails using default template
python Sending_mail.py --csv emails.csv

# Use custom subject and body
python Sending_mail.py --csv emails.csv --subject "Hello!" --body "Custom message"

# Use a template file
python Sending_mail.py --csv emails.csv --template vietnam_template.txt
```

### Advanced Features

```bash
# Send HTML emails with attachments
python Sending_mail.py --csv emails.csv \
  --template vietnam_template.txt \
  --html-template vietnam_template.html \
  --attachments brochure.pdf map.jpg

# Dry run to test configuration
python Sending_mail.py --csv emails.csv --dry-run

# Create sample files
python Sending_mail.py --create-samples
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--csv` | CSV file with email addresses | `--csv emails.csv` |
| `--subject` | Email subject (overrides template) | `--subject "Hello World"` |
| `--body` | Email body (overrides template) | `--body "Custom message"` |
| `--template` | Text template file | `--template vietnam_template.txt` |
| `--html-template` | HTML template file | `--html-template vietnam_template.html` |
| `--attachments` | Files to attach | `--attachments file1.pdf file2.jpg` |
| `--dry-run` | Test without sending | `--dry-run` |
| `--create-samples` | Create sample files | `--create-samples` |

---

## 📁 File Formats

### CSV Format

Your CSV file can have headers or be a simple list:

**With headers:**

```csv
email,name
john@example.com,John Doe
jane@example.com,Jane Smith
```

**Without headers:**

```csv
john@example.com,John Doe
jane@example.com,Jane Smith
```

**Simple email list:**

```csv
john@example.com
jane@example.com
```

### Template Format

Templates use `{name}` for personalization and `---` to separate subject from body:

```text
Subject Line with {name}
---
Dear {name},

Your email content here...

Best regards,
Your Team
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_ADDRESS` | Your Gmail address | Required |
| `EMAIL_PASSWORD` | Gmail app password | Required |
| `SMTP_SERVER` | SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |
| `DEFAULT_SUBJECT` | Default email subject | `Explore Vietnam` |
| `RATE_LIMIT_DELAY` | Delay between emails (seconds) | `1.0` |

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security
   - 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. **Use the app password** (not your regular password) in the `.env` file

---

## 🧪 Testing

Always test your configuration before sending bulk emails:

```bash
# Test with dry run
python Sending_mail.py --csv emails.csv --dry-run

# Test with a small list first
python Sending_mail.py --csv test_emails.csv

# Check logs for any issues
tail -f logs/email_sender.log
```

---

## 📊 Examples

### Example 1: Simple Text Email

```bash
python Sending_mail.py \
  --csv contacts.csv \
  --subject "Welcome to Vietnam!" \
  --body "Thank you for your interest in Vietnam tourism."
```

### Example 2: Template with Attachments

```bash
python Sending_mail.py \
  --csv vip_contacts.csv \
  --template welcome_template.txt \
  --attachments brochure.pdf vietnam_guide.pdf
```

### Example 3: HTML Email Campaign

```bash
python Sending_mail.py \
  --csv newsletter_list.csv \
  --template newsletter.txt \
  --html-template newsletter.html \
  --attachments latest_offers.pdf
```

---

## 🔒 Security

- ✅ **Never commit** `.env` files to version control
- ✅ **Use app passwords** instead of regular Gmail passwords
- ✅ **Rotate credentials** regularly
- ✅ **Monitor logs** for suspicious activity
- ✅ **Test with small batches** first
- ✅ **Respect rate limits** to avoid being blocked

---

## 🐛 Troubleshooting

### Common Issues

**Authentication Error:**

```text
SMTPAuthenticationError: Username and Password not accepted
```

- Ensure 2FA is enabled on Gmail
- Use app password, not regular password
- Check EMAIL_ADDRESS and EMAIL_PASSWORD in .env

**Connection Error:**

```text
SMTPConnectError: Connection refused
```

- Check internet connection
- Verify SMTP_SERVER and SMTP_PORT settings
- Check firewall settings

**Rate Limiting:**

```text
Too many emails sent
```

- Increase RATE_LIMIT_DELAY in .env
- Send smaller batches
- Wait before retrying

### Getting Help

1. **Check logs**: `logs/email_sender.log`
2. **Run dry-run**: `--dry-run` flag
3. **Test with one email** first
4. **Verify Gmail settings**

---

## 📝 License

This project is open source. Feel free to use and modify as needed.

---

## 👨‍💻 Author

**Quang-Ng-Duong** - Enhanced with modern Python practices and enterprise features

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## Happy emailing! 📧✨
