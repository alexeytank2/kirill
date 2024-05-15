from uuid import UUID

from fastapi import APIRouter, Path, Body, Security, File, Form
from fastapi import status

from dependencies import common_api_errors, oauth2_scheme, attachment_tag
from models import ErrorResponse, Message, MessageAttachment

router = APIRouter()


@router.post("/api/v3/chats/{id}/messages/link-file", response_model=Message, status_code=status.HTTP_200_OK,
             tags=[attachment_tag], description="Add File to Chat", deprecated=True,
             responses={**common_api_errors,
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def link_file(id: UUID = Path(..., description="Chat Id"),
                    attachment: MessageAttachment = Body(..., description="Message Attachment"),
                    token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/{message_id}/link-file", response_model=Message,
             status_code=status.HTTP_200_OK, deprecated=True,
             tags=[attachment_tag], description="Add File to the given message of Chat",
             responses={**common_api_errors,
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def link_file(id: UUID = Path(..., description="Chat Id"),
                    message_id: UUID = Path(..., description="Message Id"),
                    attachment: MessageAttachment = Body(..., description="Message Attachment"),
                    token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/upload-file", response_model=Message, status_code=status.HTTP_201_CREATED,
             tags=[attachment_tag], description="Upload File to Chat",
             responses={**common_api_errors,
                        status.HTTP_201_CREATED: {"content": {"application/json": {"example": {
                            "external_request_id": "bb638f26-7064-4285-94b3-ce5d48f29b9b",
                            "message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "create_time": "2021-04-01T10:34:15Z",
                            "author_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "is_mine": True,
                            "status": "DELIVERED",
                            "type": "FILE",
                            "attachments": [
                                {
                                    "filename": "image.png",
                                    "uri": "https://google.com/image.png",
                                    "thumbnail_uri": "https://google.com/small_image.png"
                                }
                            ],
                            "prev_message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        }}}},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def upload_file(file: bytes = File(default=None),
                      id: UUID = Path(..., description="Chat Id"),
                      external_request_id: str = Form(default=None, description="Optional idempotency key for request"),
                      token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/{message_id}/upload-file", response_model=Message,
             status_code=status.HTTP_200_OK,
             tags=[attachment_tag], description="Upload File to the given message of Chat",
             responses={**common_api_errors,
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def upload_file(file: bytes = File(default=None),
                      id: UUID = Path(..., description="Chat Id"),
                      message_id: UUID = Path(..., description="Message Id"),
                      token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message
