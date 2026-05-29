from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import ReferenceAgent
from src.memory import SQLiteResearchMemory


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


def test_memory_persists_runs_and_memories():
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = SQLiteResearchMemory(Path(tmpdir) / "research.sqlite3")
        run_id = memory.create_run("test task", {"pattern": "ReAct Agent"})
        memory.save_step(
            run_id=run_id,
            step_number=1,
            thought="need evidence",
            action="local_knowledge_search",
            action_input="local-first agents",
            observation="Ollama supports local-first inference.",
            sources=["docs/ollama-local-models.md"],
        )
        memory.save_final_answer(run_id, "Local-first agents can use Ollama.")
        memory.remember("research_summary", "local-first-agents", "Ollama local inference")

        assert memory.recent_runs()[0]["task"] == "test task"
        assert memory.search_memories("Ollama agents")[0].key == "local-first-agents"
