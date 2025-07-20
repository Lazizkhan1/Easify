from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import asyncio
from utils.call_agent import call_agent_async
from agents import root_erp_agent


async def run_team_conversation():

    session_service = InMemorySessionService()
    APP_NAME = "erp_agent"
    USER_ID = "user_007"
    SESSION_ID = "session_007"

    initial_state = {
        "user_language": "en", # uz, ru, en,
        "merchant_id": "0b575adc-df04-415e-858c-ff0426aaf168",
        "branch_id": "59e7f8b8-f414-4c57-8395-764a8ef0e8cd",
        "bearer_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJveWd1bFVzZXJzIiwiaXNzIjoiaHR0cHM6Ly9veWd1bC51eiIsInVzZXJJZCI6Ijc3ODcyMjE2LTUyMTUtNDMxNi05YjllLWIzMmRhMzhlODQ0ZCIsImxvZ2luIjoiVG9zaEd1bCIsInVzZXJUeXBlIjoiTUVSQ0hBTlQiLCJtZXJjaGFudElkIjoiMGI1NzVhZGMtZGYwNC00MTVlLTg1OGMtZmYwNDI2YWFmMTY4IiwiYnJhbmNoSWQiOiIiLCJkcml2ZXJJZCI6IiIsImV4cCI6MTc1Mjk2MDA3NH0.3jzxwWLjQFiNk_1kEMuCLg7DVN9pkKK5ZJGLP5Iv6BU"
    }

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )

    runner_agent_team = Runner(
        agent=root_erp_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    prompt = f"Introduce yourself and contunue in language: {initial_state['user_language']}"
    while True:
        await call_agent_async(
            query=prompt,
            runner=runner_agent_team,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        prompt = input(">>> ")
        if "exit" in prompt:
            break


if __name__ == "__main__":
    try:
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
