from google.adk.runners import InMemoryRunner
from dotenv import load_dotenv
from k8_expert_agent.agent import root_agent
from google.genai import types
import asyncio

load_dotenv()

runner = InMemoryRunner(
    agent=root_agent,
    app_name='my_app',
)

def create_session():
    session = asyncio.run(
        runner.session_service.create_session(
            app_name='my_app', user_id='user'
        )
    )

    return session

def run_agent(session_id: str, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', new_message)
    for event in runner.run(
        user_id='user',
        session_id=session_id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(f'** {event.author}: {event.content.parts[0].text}')
    print()

if __name__ == '__main__':
    session = create_session()
    run_agent(session.id, "Hello!")
    run_agent(session.id, "What can you do for me?")