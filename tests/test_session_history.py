import unittest
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from agents.session_history import get_session_history, store


class TestSessionHistory(unittest.TestCase):

    def setUp(self):
        """Set up the store for each test."""
        # Clear the store before each test to avoid cross-test interference
        store.clear()

    def test_get_session_history_creates_new_history(self):
        """Test that a new chat history is created if the session_id does not exist."""
        session_id = "test_session"
        self.assertNotIn(session_id, store)  # Ensure session_id is not in store

        # Call the function
        history = get_session_history(session_id)

        # Assertions
        self.assertIn(session_id, store)  # Now it should be in the store
        self.assertIsInstance(history, InMemoryChatMessageHistory)
        self.assertEqual(store[session_id], history)

    def test_get_session_history_returns_existing_history(self):
        """Test that an existing chat history is returned if the session_id exists."""
        session_id = "test_session"
        existing_history = InMemoryChatMessageHistory()
        store[session_id] = existing_history  # Pre-populate store with existing history

        # Call the function
        history = get_session_history(session_id)

        # Assertions
        self.assertIn(session_id, store)  # Confirm it is in the store
        self.assertEqual(history, existing_history)  # Should return the existing history


if __name__ == '__main__':
    unittest.main()
