from typing import List
from uuid import UUID

from fastapi import APIRouter, Path, Body, Security, Depends
from fastapi import status

from dependencies import common_api_errors, oauth2_scheme, chat_tag
from models import Chat, ErrorResponse, ChatListResponse, ChatListParams, NewChat, ChatDetails, ProfileBaseListResponse, \
    CustomerIds, Message, SystemMessage

router = APIRouter()


@router.post("/api/v3/chats", response_model=ChatDetails, status_code=status.HTTP_201_CREATED,
             tags=[chat_tag], description="Create a new Chat with the given customer",
             responses={**common_api_errors,
                        status.HTTP_200_OK: {"model": ChatDetails},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse},
                        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse}})
async def start_chat(chat: NewChat = Body(..., description="Chat to start"),
                     token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return ChatDetails


@router.get("/api/v3/chats/{id}", response_model=ChatDetails, tags=[chat_tag],
            responses={**common_api_errors,
                       status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                       status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def get_chat(id: UUID = Path(..., description="Chat Id"),
                   token: str = Security(oauth2_scheme, scopes=["chats:read"])):
    return ChatDetails


@router.get("/api/v3/chats", response_model=ChatListResponse, tags=[chat_tag],
            description="List chats, sort by last activity timestamp (last message added OR chat room creation if "
                        "there are no messages) (DESC)",
            responses={**common_api_errors})
async def list_chats(list_params: ChatListParams = Depends(ChatListParams),
                     token: str = Security(oauth2_scheme, scopes=["chats:read"])):
    return ChatListResponse


@router.post("/api/v3/chats/{id}/block", response_model=ChatDetails, tags=[chat_tag],
             description="Block a given Chat and the corresponding customer",
             responses={**common_api_errors,
                 status.HTTP_200_OK: {"content": {"application/json": {"example": {
                     "chat_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                     "partner": {
                         "customer_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "username": "RichJason",
                         "avatar_url": "https://example.com/avatar/RichJason.png",
                         "display_name": "Rich Jason",
                         "status": "ONLINE",
                         "country": "RU"
                     },
                     "last_message": {
                         "message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "author_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "status": "DELIVERED",
                         "type": "MESSAGE",
                         "create_time": "2021-04-01T10:34:15Z",
                         "text": "Hello!",
                         "attachments": [
                             {
                                 "filename": "image.png",
                                 "uri": "https://google.com/image.png",
                                 "thumbnail_uri": "https://google.com/small_image.png"
                             }
                         ],
                         "parameters": {
                             "additionalProp1": "string",
                             "additionalProp2": "string",
                             "additionalProp3": "string"
                         },
                         "prev_message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "update_time": "2021-04-02T11:34:15Z"
                     },
                     "context": {
                         "chat_name": "Chat with John",
                         "delivered_message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "read_message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "status": "BLOCKED",
                         "unread_count": 0,
                         "update_time": "2021-04-01T10:34:15Z"
                     },
                     "moderator": {
                         "customer_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "username": "RichJason",
                         "avatar_url": "https://example.com/avatar/RichJason.png",
                         "display_name": "Rich Jason",
                         "status": "ONLINE",
                         "country": "RU"
                     },
                     "me": {
                         "customer_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                         "username": "RichJason",
                         "avatar_url": "https://example.com/avatar/RichJason.png",
                         "display_name": "Rich Jason",
                         "status": "ONLINE",
                         "country": "RU"
                     }
                 }}}},
                 status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                 status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def block_chat(id: UUID = Path(..., description="Chat Id"),
                     token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return ChatDetails


@router.post("/api/v3/chats/{id}/unblock", response_model=ChatDetails, tags=[chat_tag],
             description="Unlock a given Chat and the customer",
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def unblock_chat(id: UUID = Path(..., description="Chat Id"),
                       token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return ChatDetails


@router.post("/api/v3/chats/check-responders", response_model=ProfileBaseListResponse, status_code=status.HTTP_200_OK,
             tags=[chat_tag], description="This API method could be used to check presence of the "
                                          "requested customers, etc.",
             responses={**common_api_errors,
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse}})
async def check_responders(body: CustomerIds = Body(..., description="Array of Customer ids"),
                           token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return ProfileBaseListResponse

