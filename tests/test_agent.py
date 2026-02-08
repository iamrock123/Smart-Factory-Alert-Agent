import pytest
from unittest.mock import mock_open, patch
from agent import AnomalyAlertAgent

class TestAgent:
    def test_load_knowledge_base_success(self):
        mock_content = "# Mock KB content"
        with patch("builtins.open", mock_open(read_data=mock_content)):
            # We also need to mock AnomalyDetector inside Agent init to avoid FS calls
            with patch("agent.AnomalyDetector"):
                agent = AnomalyAlertAgent(model_name="test")
                # Creating agent calls _load_knowledge_base immediately
                assert agent.knowledge_base == mock_content

    def test_load_knowledge_base_missing(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
             with patch("agent.AnomalyDetector"):
                agent = AnomalyAlertAgent(model_name="test")
                assert "No Standard Operating Procedure available" in agent.knowledge_base
