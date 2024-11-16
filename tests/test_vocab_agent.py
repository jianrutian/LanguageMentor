import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from agents.vocab_agent import VocabAgent
from langchain_core.messages import AIMessage


class TestVocabAgent(unittest.TestCase):

    def setUp(self):
        """Set up a VocabAgent instance for each test."""
        self.agent = VocabAgent()

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session_no_session_id(self, mock_get_session_history):
        """Test restart_session when no session_id is provided."""

        # Setup mocks
        mock_history = MagicMock()
        mock_get_session_history.return_value = mock_history

        # Call restart_session
        result = self.agent.restart_session()

        # Assertions
        mock_get_session_history.assert_called_once_with(self.agent.session_id)
        mock_history.clear.assert_called_once()
        self.assertEqual(result, mock_history)

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session_with_session_id(self, mock_get_session_history):
        """Test restart_session when a session_id is provided."""

        # Setup mocks
        mock_history = MagicMock()
        mock_get_session_history.return_value = mock_history
        test_session_id = "test123"

        # Call restart_session with a custom session_id
        result = self.agent.restart_session(session_id=test_session_id)

        # Assertions
        mock_get_session_history.assert_called_once_with(test_session_id)
        mock_history.clear.assert_called_once()
        self.assertEqual(result, mock_history)


if __name__ == '__main__':
    unittest.main()
