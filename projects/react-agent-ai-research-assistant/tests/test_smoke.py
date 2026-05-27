from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import ReferenceAgent


def test_agent_initializes_state():
    state = ReferenceAgent().initialize("test task")
    assert state.task == "test task"
    assert "ReAct Agent" == ReferenceAgent.pattern


def test_agent_has_local_tool_by_default():
    agent = ReferenceAgent()
    assert "local_knowledge_search" in agent.tools
    assert "web_search" in agent.tools


def test_agent_can_disable_web_tool():
    agent = ReferenceAgent(web_search_mode="off")
    assert "local_knowledge_search" in agent.tools
    assert "web_search" not in agent.tools
