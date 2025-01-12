from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.core.cache import cache

class MessagingAppTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(username="sender", password="password")
        self.receiver = User.objects.create_user(username="receiver", password="password")

    def test_message_creation(self):
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message."
        )

        # Check if the message is saved correctly
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Hello, this is a test message.")

    def test_notification_creation(self):
        # Create a message, which should trigger the notification signal
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is another test message."
        )

        # Check if a notification is created for the receiver
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)

        notification = notifications.first()
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)  # Default value should be False

    def test_no_notification_for_sender(self):
        # Create a message
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Yet another test message."
        )

        # Check that the sender has no notifications
        notifications = Notification.objects.filter(user=self.sender)
        self.assertEqual(notifications.count(), 0)

class MessageEditLoggingTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(username="sender", password="password")
        self.receiver = User.objects.create_user(username="receiver", password="password")
        # Create an initial message
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message content"
        )

    def test_message_edit_logs_history(self):
        # Update the message content
        self.message.content = "Updated message content"
        self.message.save()

        # Check if a history record is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)

        # Verify the history record contains the old content
        history_record = history.first()
        self.assertEqual(history_record.old_content, "Original message content")

    def test_multiple_edits_log_multiple_histories(self):
        # First edit
        self.message.content = "First edit"
        self.message.save()

        # Second edit
        self.message.content = "Second edit"
        self.message.save()

        # Check if two history records are created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 2)

        # Verify the history records
        self.assertEqual(history[0].old_content, "Original message content")
        self.assertEqual(history[1].old_content, "First edit")

    def test_edited_flag_set_on_edit(self):
        # Update the message content
        self.message.content = "Edited content"
        self.message.save()

        # Reload the message and check the edited flag
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)

    def test_no_history_on_no_content_change(self):
        # Save the message without changing the content
        self.message.save()

        # Check that no history record is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 0)

class UserDeletionTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        
        # Create messages between users
        self.message1 = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Hello from user1"
        )
        self.message2 = Message.objects.create(
            sender=self.user2, receiver=self.user1, content="Hello from user2"
        )
        
        # Create notifications for messages
        Notification.objects.create(user=self.user2, message=self.message1)
        Notification.objects.create(user=self.user1, message=self.message2)
        
        # Log a message edit
        MessageHistory.objects.create(
            message=self.message1,
            old_content="Original content",
            edited_by=self.user1
        )

    def test_user_deletion_cleans_related_data(self):
        # Delete user1
        self.user1.delete()

        # Verify that messages sent by or received by user1 are deleted
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 0)
        self.assertEqual(Message.objects.filter(receiver=self.user1).count(), 0)

        # Verify that notifications for user1 are deleted
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)

        # Verify that message histories edited by user1 are deleted
        self.assertEqual(MessageHistory.objects.filter(edited_by=self.user1).count(), 0)

    def test_related_user_data_persistence_for_others(self):
        # Delete user1
        self.user1.delete()

        # Verify that user2's data is still intact
        self.assertEqual(User.objects.filter(username="user2").count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.user2).count(), 1)
        self.assertEqual(Message.objects.filter(sender=self.user2).count(), 1)
        self.assertEqual(Message.objects.filter(receiver=self.user2).count(), 0)

class ThreadedConversationTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        
        # Create a root message
        self.root_message = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Root message"
        )
        
        # Create replies
        self.reply1 = Message.objects.create(
            sender=self.user2, receiver=self.user1, content="First reply", parent_message=self.root_message
        )
        self.reply2 = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Second reply", parent_message=self.reply1
        )
        self.reply3 = Message.objects.create(
            sender=self.user2, receiver=self.user1, content="Third reply", parent_message=self.reply1
        )

    def test_thread_structure(self):
        # Fetch the thread for the root message
        replies = self.root_message.replies.all()

        # Check that the root message has the correct direct replies
        self.assertEqual(replies.count(), 1)
        self.assertEqual(replies.first(), self.reply1)

        # Check that the first reply has the correct nested replies
        nested_replies = self.reply1.replies.all()
        self.assertEqual(nested_replies.count(), 2)
        self.assertIn(self.reply2, nested_replies)
        self.assertIn(self.reply3, nested_replies)

    def test_recursive_thread_view(self):
        # Use the test client to call the view
        response = self.client.get(f'/conversation/{self.root_message.id}/')
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON
        data = response.json()

        # Check root message details
        self.assertEqual(data['id'], self.root_message.id)
        self.assertEqual(data['content'], "Root message")
        self.assertEqual(len(data['replies']), 1)

        # Check the nested replies
        first_reply = data['replies'][0]
        self.assertEqual(first_reply['id'], self.reply1.id)
        self.assertEqual(len(first_reply['replies']), 2)

        second_reply = first_reply['replies'][0]
        self.assertEqual(second_reply['id'], self.reply2.id)

        third_reply = first_reply['replies'][1]
        self.assertEqual(third_reply['id'], self.reply3.id)


class UnreadMessagesManagerTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        # Create messages
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Unread message 1")
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Unread message 2", read=True)
        Message.objects.create(sender=self.user2, receiver=self.user1, content="Unread message 3")

    def test_unread_messages_for_user(self):
        # Fetch unread messages for user2
        unread_messages = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread_messages.count(), 1)
        self.assertEqual(unread_messages.first().content, "Unread message 1")

        # Fetch unread messages for user1
        unread_messages = Message.unread.unread_for_user(self.user1)
        self.assertEqual(unread_messages.count(), 1)
        self.assertEqual(unread_messages.first().content, "Unread message 3")


class CachedViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user1", password="password")
        self.client.login(username="user1", password="password")

        # Create unread messages
        Message.objects.create(sender=self.user, receiver=self.user, content="Message 1")
        Message.objects.create(sender=self.user, receiver=self.user, content="Message 2", read=True)

    def test_unread_messages_cache(self):
        # Fetch unread messages
        response1 = self.client.get('/unread_messages/')
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json()
        self.assertEqual(len(data1), 1)

        # Add a new unread message
        Message.objects.create(sender=self.user, receiver=self.user, content="Message 3")

        # Fetch again before cache expiry (should return same result as before)
        response2 = self.client.get('/unread_messages/')
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        self.assertEqual(len(data2), 1)  # Cache still active

        # Clear cache and fetch again (should return updated result)
        cache.clear()
        response3 = self.client.get('/unread_messages/')
        self.assertEqual(response3.status_code, 200)
        data3 = response3.json()
        self.assertEqual(len(data3), 2)  # Cache cleared, updated data