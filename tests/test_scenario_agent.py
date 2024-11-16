import unittest
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from agents.scenario_agent import ScenarioAgent


class TestScenarioAgent(unittest.TestCase):
    @patch('agents.scenario_agent.ScenarioAgent.load_intro')
    @patch('agents.scenario_agent.ScenarioAgent.load_prompt')
    def setUp(self, mock_load_prompt, mock_load_intro):
        """Set up a ScenarioAgent instance for each test."""
        mock_load_prompt.return_value = 'Mocked prompt response'
        mock_load_intro.return_value = ["Mocked intro message"]
        self.agent = ScenarioAgent(scenario_name="test_scenario")

    @patch('agents.scenario_agent.get_session_history')
    @patch('agents.scenario_agent.random.choice')
    def test_start_new_session_no_history(self, mock_random_choice, mock_get_session_history):
        """Test start_new_session when there is no existing session history."""

        # Setup mocks
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_session_history.return_value = mock_history

        mock_random_choice.return_value = "Hello, I am an AI assistant."  # Mocked initial AI message

        # Call start_new_session
        initial_message = self.agent.start_new_session()

        # Assertions
        self.assertEqual(initial_message, "Hello, I am an AI assistant.")
        mock_random_choice.assert_called_once_with(self.agent.intro_messages)
        mock_history.add_message.assert_called_once_with(AIMessage(content="Hello, I am an AI assistant."))

    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_with_existing_history(self, mock_get_session_history):
        """Test start_new_session when there is existing session history."""

        # Setup mocks
        mock_history = MagicMock()
        mock_history.messages = [AIMessage(content="Existing message")]  # Existing history
        mock_get_session_history.return_value = mock_history

        # Call start_new_session
        last_message = self.agent.start_new_session()

        # Assertions
        self.assertEqual(last_message, "Existing message")
        mock_get_session_history.assert_called_once_with(self.agent.session_id)
        mock_history.add_message.assert_not_called()  # No new message should be added


if __name__ == '__main__':
    unittest.main()