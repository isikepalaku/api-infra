"""AgentOS Demo"""

from agno.db.postgres import PostgresDb
from agno.os import AgentOS
from db.session import db_url

from agents.web_agent import get_web_agent
from agents.finance_agent import get_finance_agent
from agents.agno_assist import get_agno_assist


web_agent = get_web_agent(model_id="gpt-4o-mini")
finance_agent = get_finance_agent(model_id="gpt-4o-mini")
agno_assist = get_agno_assist(model_id="gpt-4o-mini")

# Create Postgres-backed database
db = PostgresDb(
    db_url=db_url,
)

# Add knowledge to Agno Assist agent
agno_assist.knowledge.add_content(
    name="Agno Docs",
    url="https://docs.agno.com/llms-full.txt",
)


# Create the AgentOS
agent_os = AgentOS(
    os_id="agentos-demo",
    agents=[web_agent, finance_agent, agno_assist],
    interfaces=[],
)
app = agent_os.get_app()

if __name__ == "__main__":
    # Simple run to generate and record a session
    agent_os.serve(app="main:app", reload=True)
