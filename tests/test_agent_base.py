import unittest
import os
import sys
from unittest.mock import patch, MagicMock, mock_open
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from agents.agent_base import AgentBase


class TestAgentBaseComplete(unittest.TestCase):
    class ConcreteAgent(AgentBase):
        """A concrete class to instantiate AgentBase for testing purposes."""
        def create_chatbot(self):
            self.chatbot = MagicMock()  # Mocking chatbot creation for test purposes.

    def setUp(self):
        """Set up test environment."""
        self.prompt_file = 'test_prompt.txt'
        self.intro_file = 'test_intro.json'
        with open(self.prompt_file, 'w') as f:
            f.write('Test prompt content.')
        with open(self.intro_file, 'w') as f:
            f.write('["intro message 1", "intro message 2"]')
        self.agent = self.ConcreteAgent(name='TestAgent', prompt_file=self.prompt_file, intro_file=self.intro_file)

    def tearDown(self):
        """Clean up test files."""
        import os
        if os.path.exists(self.prompt_file):
            os.remove(self.prompt_file)
        if os.path.exists(self.intro_file):
            os.remove(self.intro_file)

    def test_load_prompt(self):
        """Test if prompt is loaded correctly."""
        self.assertEqual(self.agent.prompt, 'Test prompt content.')

    def test_load_intro(self):
        """Test if intro messages are loaded correctly."""
        self.assertEqual(self.agent.intro_messages, ["intro message 1", "intro message 2"])

    def test_missing_prompt_file(self):
        """Test behavior when prompt file is missing."""
        with self.assertRaises(FileNotFoundError):
            self.ConcreteAgent(name='TestAgent', prompt_file='missing_prompt.txt')

    @patch('agents.agent_base.AgentBase.load_prompt')
    def test_mock_load_prompt_method(self, mock_load_prompt):
        """Test behavior when load_prompt is mocked."""
        mock_load_prompt.return_value = 'Mocked prompt response'
        agent = self.ConcreteAgent(name='TestAgent', prompt_file='mocked_prompt.txt')
        self.assertEqual(agent.prompt, 'Mocked prompt response')
        mock_load_prompt.assert_called_once()

    @patch('agents.agent_base.AgentBase.load_intro')
    @patch('agents.agent_base.AgentBase.load_prompt')
    def test_mock_load_intro_method(self, mock_load_prompt, mock_load_intro):
        """Test behavior when load_intro is mocked."""
        mock_load_intro.return_value = ["Mocked intro message"]
        agent = self.ConcreteAgent(name='TestAgent', prompt_file='mocked_prompt.txt', intro_file='mocked_intro.json')
        self.assertEqual(agent.intro_messages, ["Mocked intro message"])
        mock_load_intro.assert_called_once()

    # @patch('src.agents.agent_base.AgentBase.create_chatbot')
    # @patch('agents.agent_base.AgentBase.load_prompt')
    # def test_create_chatbot(self, mock_load_prompt, mock_create_chatbot):
    #     """Test that create_chatbot is called during initialization."""
    #     agent = self.ConcreteAgent(name='TestAgent', prompt_file='mocked_prompt.txt')
    #     mock_create_chatbot.assert_called_once()

    def test_chat_with_history(self):
        """Test chat_with_history using a mocked chatbot instance."""
        self.agent.create_chatbot()  # This sets up the mocked chatbot

        # Simulating chat responses
        mock_response = "Mock response to user input"
        self.agent.chatbot.chat_with_history = MagicMock(return_value=mock_response)

        user_input = "Hello, chatbot!"
        response = self.agent.chatbot.chat_with_history(user_input)

        self.agent.chatbot.chat_with_history.assert_called_once_with(user_input)
        self.assertEqual(response, mock_response)


if __name__ == '__main__':
    unittest.main()
