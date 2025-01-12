from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification, Message

User = get_user_model()

class NotificationModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            email='sender@example.com',
            password='password123',
            first_name='Sender',
            last_name='User'
        )
        self.receiver = User.objects.create_user(
            email='receiver@example.com',
            password='password123',
            first_name='Receiver',
            last_name='User'
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, this is a test message.'
        )
        self.notification = Notification.objects.create(
            user=self.receiver,
            message=self.message
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.receiver)
        self.assertEqual(self.notification.message, self.message)
        self.assertIsNotNone(self.notification.timestamp)

    def test_notification_str(self):
        self.assertEqual(str(self.notification), f'Notification for {self.receiver.email} - {self.message.content}')