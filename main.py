from datetime import datetime
import json
import unittest


class Observer:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, event_type, user):
        for observer in self.observers:
            observer.update(event_type, user)


class DataStore:
    @staticmethod
    def load_data(archive):
        try:
            with open(archive, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_data(data, archive):
        with open(archive, 'w') as file:
            json.dump(data, file)


class EventManager(Observer):
    def __init__(self, data_store):
        super().__init__()
        self.data_store = data_store

    def register_event(self, event_type, user):
        events = self.data_store.load_data('events.json')
        if not isinstance(events, list):
            events = []
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        new_event = {
            'type': event_type,
            'user': user,
            'timestamp': timestamp
        }
        events.append(new_event)
        self.data_store.save_data(events, 'events.json')
        self.notify_observers(event_type, user)

    def get_user_with_most_events(self):
        events = self.data_store.load_data('events.json')
        user_counts = {}
        for event in events:
            user = event['user']
            if user in user_counts:
                user_counts[user] += 1
            else:
                user_counts[user] = 1
        if user_counts:
            user_with_most_events = max(user_counts, key=user_counts.get)
            return user_with_most_events
        return None

    def get_most_commented_tweet(self):
        messages = self.data_store.load_data('messages.json')
        if not isinstance(messages, list):
            return None
        most_commented_tweet = max(messages, key=lambda x: len(x['replies']))
        return most_commented_tweet

    def get_unique_users_opened_app(self):
        events = self.data_store.load_data('events.json')
        unique_users = set(event['user'] for event in events)
        return len(unique_users)


class UserEventManager(EventManager):
    def __init__(self, data_store):
        super().__init__(data_store)

    def register_user_event(self, event_type, user):
        self.register_event(event_type, user)


class MessageEventManager(EventManager):
    def __init__(self, data_store):
        super().__init__(data_store)

    def register_message_event(self, event_type, user):
        self.register_event(event_type, user)


class MessageManager:
    def __init__(self, data_store, event_manager):
        self.data_store = data_store
        self.event_manager = event_manager

    def post_message(self, username):
        author = username
        message = input('Enter your message (max. 300 characters): ')
        if len(message) > 300:
            print('Message exceeds the maximum character limit.')
            return
        messages = self.data_store.load_data('messages.json')
        if not isinstance(messages, list):
            messages = []
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        message_id = len(messages) + 1
        new_message = {
            'id': message_id,
            'author': author,
            'timestamp': timestamp,
            'message': message,
            'replies': []
        }
        messages.append(new_message)
        self.data_store.save_data(messages, 'messages.json')
        print('Message posted successfully!')
        self.event_manager.register_message_event('create tweet', author)

    def post_reply(self, message_id, user):
        author = user
        reply = input('Enter your reply (max. 300 characters): ')
        if len(reply) > 300:
            print('Reply exceeds the maximum character limit.')
            return
        messages = self.data_store.load_data('messages.json')
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        for message in messages:
            if message['id'] == message_id:
                new_reply = {
                    'author': author,
                    'timestamp': timestamp,
                    'reply': reply
                }
                message['replies'].append(new_reply)
                self.data_store.save_data(messages, 'messages.json')
                print('Reply posted successfully!')
                self.event_manager.register_message_event('reply tweet', author)
                return
        print('Invalid message ID.')

    def get_messages(self):
        messages = self.data_store.load_data('messages.json')
        if not messages:
            print('No messages available.')
            return

        last_10_messages = messages[-10:]
        for message in last_10_messages:
            print(f"[ID: {message['id']}] {message['author']} - {message['timestamp']}: {message['message']}")
            replies = message['replies']
            if replies:
                print("Replies:")
                for reply in replies:
                    print(f"\t{reply['author']} - {reply['timestamp']}: {reply['reply']}")
            print()


class UserManager:
    def __init__(self, data_store):
        self.data_store = data_store

    def register(self):
        username = input('Enter a username: ')
        password = input('Enter a password: ')
        users = self.data_store.load_data('users.json')
        if username in users:
            print('Username already exists. Please choose a different username.')
        else:
            users[username] = password
            self.data_store.save_data(users, 'users.json')
            print('Registration successful!')

    def login(self):
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        users = self.data_store.load_data('users.json')
        if username not in users or users[username] != password:
            print('Invalid username or password. Please try again.')
            return False
        else:
            print('Login successful!')
            print('Welcome, ' + username + "!")
            return [username, password]


class DataStoreFactory:
    @staticmethod
    def create_data_store():
        return DataStore()


class App:
    def __init__(self, message_manager, user_manager, event_manager):
        self.message_manager = message_manager
        self.user_manager = user_manager
        self.event_manager = event_manager

    def user_session(self, user):
        while True:
            print('''        1. Post a message
        2. Post a reply
        3. Dashboard 
        4. Logout''')
            choice = input('Enter your choice (1-4): ')
            if choice == '1':
                self.message_manager.post_message(user)
            elif choice == '2':
                message_id = input('Enter the ID of the message you want to reply to: ')
                self.message_manager.post_reply(int(message_id), user)
            elif choice == '3':
                self.message_manager.get_messages()
            elif choice == '4':
                break
            else:
                print('Invalid choice. Please try again.')

    def main_menu(self):
        print('''Welcome to Twitter Reloaded!
        This app was developed by Alex Bracho!''')
        while True:
            print('''You need to register or login to use the app!
        1. Register
        2. Login
        3. Exit''')
            choice = input('Enter your choice (1-4): ')
            if choice == '1':
                self.user_manager.register()
            elif choice == '2':
                users_credentials = self.user_manager.login()
                if users_credentials:
                    self.user_session(users_credentials[0])
            elif choice == '3':
                break
            else:
                print('Invalid choice. Please try again.')


class EventManagerTests(unittest.TestCase):
    def setUp(self):
        self.data_store = DataStore()
        self.event_manager = EventManager(self.data_store)

    def test_get_user_with_most_events(self):
        # Create test events
        events = [
            {'type': 'event1', 'user': 'user1'},
            {'type': 'event2', 'user': 'user2'},
            {'type': 'event1', 'user': 'user2'},
            {'type': 'event2', 'user': 'user2'},
            {'type': 'event1', 'user': 'user1'},
            {'type': 'event1', 'user': 'user3'}
        ]
        self.data_store.save_data(events, 'events.json')

        # Test the method
        user_with_most_events = self.event_manager.get_user_with_most_events()
        self.assertEqual(user_with_most_events, 'user2')

    def test_get_most_commented_tweet(self):
        # Create test messages
        messages = [
            {'id': 1, 'author': 'user1', 'replies': []},
            {'id': 2, 'author': 'user2', 'replies': [{'author': 'user3', 'reply': 'Reply 1'}]},
            {'id': 3, 'author': 'user3', 'replies': [{'author': 'user1', 'reply': 'Reply 1'},
                                                      {'author': 'user2', 'reply': 'Reply 2'}]},
            {'id': 4, 'author': 'user4', 'replies': [{'author': 'user3', 'reply': 'Reply 1'},
                                                      {'author': 'user1', 'reply': 'Reply 2'},
                                                      {'author': 'user2', 'reply': 'Reply 3'}]},
            {'id': 5, 'author': 'user5', 'replies': [{'author': 'user4', 'reply': 'Reply 1'},
                                                      {'author': 'user3', 'reply': 'Reply 2'},
                                                      {'author': 'user2', 'reply': 'Reply 3'},
                                                      {'author': 'user1', 'reply': 'Reply 4'}]}
        ]
        self.data_store.save_data(messages, 'messages.json')

        # Test the method
        most_commented_tweet = self.event_manager.get_most_commented_tweet()
        self.assertEqual(most_commented_tweet['id'], 5)

    def test_get_unique_users_opened_app(self):
        # Create test events
        events = [
            {'type': 'event1', 'user': 'user1'},
            {'type': 'event2', 'user': 'user2'},
            {'type': 'event1', 'user': 'user2'},
            {'type': 'event2', 'user': 'user2'},
            {'type': 'event1', 'user': 'user1'},
            {'type': 'event1', 'user': 'user3'}
        ]
        self.data_store.save_data(events, 'events.json')

        # Test the method
        unique_users = self.event_manager.get_unique_users_opened_app()
        self.assertEqual(unique_users, 3)


if __name__ == '__main__':
    # Create data store
    data_store = DataStoreFactory.create_data_store()

    # Create event manager
    event_manager = EventManager(data_store)

    # Create user event manager
    user_event_manager = UserEventManager(data_store)
    event_manager.register_observer(user_event_manager)

    # Create message event manager
    message_event_manager = MessageEventManager(data_store)
    event_manager.register_observer(message_event_manager)

    # Create message manager
    message_manager = MessageManager(data_store, message_event_manager)

    # Create user manager
    user_manager = UserManager(data_store)

    # Create the app
    app = App(message_manager, user_manager, event_manager)

    # Run the main menu
    app.main_menu()

    # Run tests
    unittest.main()
