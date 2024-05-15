from fastapi import FastAPI

from routers import messages, chats, profile, attachments

description = """
Message Service API gives ability to create chats between customers, send messages, subscribe to chat notification channel 
and etc. for Messenger product

"""

app = FastAPI(title="Message Service API", description=description, version="1.1_17.04.2024")

app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(profile.router)
app.include_router(attachments.router)

