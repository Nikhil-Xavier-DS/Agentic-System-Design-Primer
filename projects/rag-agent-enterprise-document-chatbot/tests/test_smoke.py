from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import ReferenceAgent


def test_agent_initializes_state():
    state = ReferenceAgent().initialize("test task")
    assert state.task == "test task"
    assert "RAG Agent" == ReferenceAgent.pattern
