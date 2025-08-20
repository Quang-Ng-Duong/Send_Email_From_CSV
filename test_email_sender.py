#!/usr/bin/env python3
"""
Unit tests for Enhanced Email Sender from CSV
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import csv

# Import the classes we want to test
from Sending_mail import EmailSenderConfig, EmailSender, load_template


class TestEmailSenderConfig(unittest.TestCase):
    """Test EmailSenderConfig class."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear environment variables
        env_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT']
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
    
    def test_default_config(self):
        """Test default configuration values."""
        config = EmailSenderConfig()
        self.assertEqual(config.smtp_server, 'smtp.gmail.com')
        self.assertEqual(config.smtp_port, 587)
        self.assertEqual(config.default_subject, 'Explore Vietnam')
        self.assertEqual(config.rate_limit_delay, 1.0)
    
    def test_env_var_override(self):
        """Test environment variable override."""
        os.environ['SMTP_SERVER'] = 'test.smtp.com'
        os.environ['SMTP_PORT'] = '465'
        
        config = EmailSenderConfig()
        self.assertEqual(config.smtp_server, 'test.smtp.com')
        self.assertEqual(config.smtp_port, 465)
    
    def test_email_validation(self):
        """Test email validation."""
        # Valid emails
        self.assertTrue(EmailSenderConfig._is_valid_email('test@example.com'))
        self.assertTrue(EmailSenderConfig._is_valid_email('user.name@domain.co.uk'))
        
        # Invalid emails
        self.assertFalse(EmailSenderConfig._is_valid_email('invalid-email'))
        self.assertFalse(EmailSenderConfig._is_valid_email('@domain.com'))
        self.assertFalse(EmailSenderConfig._is_valid_email('user@'))
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = EmailSenderConfig()
        
        # Invalid - no credentials
        self.assertFalse(config.validate())
        
        # Invalid - bad email format
        config.email_address = 'invalid-email'
        config.email_password = 'password'
        self.assertFalse(config.validate())
        
        # Valid
        config.email_address = 'test@example.com'
        config.email_password = 'password'
        self.assertTrue(config.validate())


class TestEmailSender(unittest.TestCase):
    """Test EmailSender class."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = EmailSenderConfig()
        self.config.email_address = 'test@example.com'
        self.config.email_password = 'password'
        self.sender = EmailSender(self.config)
    
    def test_initialization(self):
        """Test EmailSender initialization."""
        self.assertIsNotNone(self.sender.config)
        self.assertIsNotNone(self.sender.logger)
        self.assertIsNone(self.sender.smtp_connection)
    
    def test_load_email_list_valid_csv(self):
        """Test loading valid CSV file."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'name'])
            writer.writerow(['test1@example.com', 'Test User 1'])
            writer.writerow(['test2@example.com', 'Test User 2'])
            csv_file = f.name
        
        try:
            email_list = self.sender.load_email_list(csv_file)
            self.assertEqual(len(email_list), 2)
            self.assertEqual(email_list[0]['email'], 'test1@example.com')
            self.assertEqual(email_list[0]['name'], 'Test User 1')
        finally:
            os.unlink(csv_file)
    
    def test_load_email_list_no_headers(self):
        """Test loading CSV file without headers."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['test1@example.com', 'Test User 1'])
            writer.writerow(['test2@example.com', 'Test User 2'])
            csv_file = f.name
        
        try:
            email_list = self.sender.load_email_list(csv_file)
            self.assertEqual(len(email_list), 2)
            self.assertEqual(email_list[0]['email'], 'test1@example.com')
        finally:
            os.unlink(csv_file)
    
    def test_load_email_list_invalid_emails(self):
        """Test loading CSV with invalid emails."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'name'])
            writer.writerow(['valid@example.com', 'Valid User'])
            writer.writerow(['invalid-email', 'Invalid User'])
            writer.writerow(['', 'Empty Email'])
            csv_file = f.name
        
        try:
            email_list = self.sender.load_email_list(csv_file)
            self.assertEqual(len(email_list), 1)  # Only valid email
            self.assertEqual(email_list[0]['email'], 'valid@example.com')
        finally:
            os.unlink(csv_file)
    
    def test_load_email_list_nonexistent_file(self):
        """Test loading non-existent CSV file."""
        email_list = self.sender.load_email_list('nonexistent.csv')
        self.assertEqual(len(email_list), 0)
    
    def test_create_message_basic(self):
        """Test creating basic email message."""
        message = self.sender.create_message(
            subject='Test Subject',
            body='Test Body',
            recipient_email='test@example.com',
            recipient_name='Test User'
        )
        
        self.assertEqual(message['Subject'], 'Test Subject')
        self.assertEqual(message['From'], 'test@example.com')
        self.assertEqual(message['To'], 'test@example.com')
    
    def test_create_message_personalization(self):
        """Test message personalization."""
        message = self.sender.create_message(
            subject='Hello {name}!',
            body='Dear {name}, welcome!',
            recipient_email='test@example.com',
            recipient_name='John'
        )
        
        self.assertEqual(message['Subject'], 'Hello John!')
        # Check body content (implementation depends on message type)
    
    @patch('smtplib.SMTP')
    def test_connect_smtp_success(self, mock_smtp):
        """Test successful SMTP connection."""
        mock_instance = Mock()
        mock_smtp.return_value = mock_instance
        
        result = self.sender.connect_smtp()
        
        self.assertTrue(result)
        mock_instance.ehlo.assert_called()
        mock_instance.starttls.assert_called()
        mock_instance.login.assert_called_with('test@example.com', 'password')
    
    @patch('smtplib.SMTP')
    def test_connect_smtp_auth_failure(self, mock_smtp):
        """Test SMTP authentication failure."""
        mock_instance = Mock()
        mock_smtp.return_value = mock_instance
        mock_instance.login.side_effect = Exception("Auth failed")
        
        result = self.sender.connect_smtp()
        
        self.assertFalse(result)


class TestLoadTemplate(unittest.TestCase):
    """Test template loading function."""
    
    def test_load_template_with_separator(self):
        """Test loading template with subject/body separator."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Test Subject\n---\nTest Body Content')
            template_file = f.name
        
        try:
            subject, body = load_template(template_file)
            self.assertEqual(subject, 'Test Subject')
            self.assertEqual(body, 'Test Body Content')
        finally:
            os.unlink(template_file)
    
    def test_load_template_without_separator(self):
        """Test loading template without separator."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Just body content')
            template_file = f.name
        
        try:
            subject, body = load_template(template_file)
            self.assertEqual(subject, '')
            self.assertEqual(body, 'Just body content')
        finally:
            os.unlink(template_file)
    
    def test_load_template_nonexistent(self):
        """Test loading non-existent template."""
        subject, body = load_template('nonexistent.txt')
        self.assertEqual(subject, '')
        self.assertEqual(body, '')


if __name__ == '__main__':
    # Create logs directory for tests
    Path('logs').mkdir(exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2)
