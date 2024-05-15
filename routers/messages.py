from uuid import UUID

from fastapi import APIRouter, Path, Body, Security, Depends
from fastapi import status

from dependencies import common_api_errors, oauth2_scheme, message_tag
from models import ErrorResponse, Message, MessageListResponse, MessageListParams, MessageListResponseSimple, \
    MessageIds, CancelOfferRequest, AcceptOfferRequest

router = APIRouter()


@router.post("/api/v3/chats/{id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED,
             tags=[message_tag], description="Send a new chat Message",
             responses={**common_api_errors,
                        status.HTTP_200_OK: {"model": Message},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def send_message(id: UUID = Path(..., description="Chat Id"),
                       message: Message = Body(..., description="Message to send"),
                       token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/{message_id}/delivered", response_model=Message, tags=[message_tag],
             deprecated=True,
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat/Message not found"}})
async def message_delivered(id: UUID = Path(..., description="Chat Id"),
                            message_id: UUID = Path(..., description="Message Id"),
                            token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/{message_id}/read", response_model=Message, tags=[message_tag],
             deprecated=True,
             responses={**common_api_errors,
                 status.HTTP_200_OK: {"content": {"application/json": {"example": {
                     "external_request_id": "bb638f26-7064-4285-94b3-ce5d48f29b9b",
                     "message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                     "author_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                     "status": "READ",
                     "type": "MESSAGE",
                     "create_time": "2021-04-01T10:34:15Z",
                     "text": "Hello!",
                     "prev_message_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                 }}}},
                 status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat/Message not found"}})
async def message_read(id: UUID = Path(..., description="Chat Id"),
                       message_id: UUID = Path(..., description="Message Id"),
                       token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/delivered", response_model=MessageListResponseSimple, tags=[message_tag],
             description="Marks one or more messages as delivered and return the content of these messages.",
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat/Message not found"}})
async def messages_delivered(id: UUID = Path(..., description="Chat Id"),
                             body: MessageIds = Body(..., description="Array of Message ids"),
                             token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return MessageListResponseSimple


@router.post("/api/v3/chats/{id}/messages/read", response_model=MessageListResponseSimple, tags=[message_tag],
             description="Marks one or more messages as read and return the content of these messages.",
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat/Message not found"}})
async def messages_read(id: UUID = Path(..., description="Chat Id"),
                        body: MessageIds = Body(..., description="Array of Message ids"),
                        token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return MessageListResponseSimple


@router.get("/api/v3/chats/{id}/messages", response_model=MessageListResponse, tags=[message_tag],
            description="List messages, sorted by message creation timestamp (create_time asc) by default",
            responses={**common_api_errors})
async def list_messages(id: UUID = Path(..., description="Chat Id"),
                        list_params: MessageListParams = Depends(MessageListParams),
                        token: str = Security(oauth2_scheme, scopes=["chats:read"])):
    return MessageListResponse


@router.get("/api/v3/chats/{id}/messages/{message_id}", response_model=Message, tags=[message_tag],
            responses={**common_api_errors,
                       status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat/Message not found"}})
async def get_message(id: UUID = Path(..., description="Chat Id"),
                      message_id: UUID = Path(..., description="Message Id"),
                      token: str = Security(oauth2_scheme, scopes=["chats:read"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/cancel-offer", response_model=Message, tags=[message_tag],
             description="Cancel the special offer. The offer can be cancelled by offer-owner ONLY!",
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def cancel_offer(id: UUID = Path(..., description="Chat Id"),
                       body: CancelOfferRequest = Body(..., description="Cancel Offer Request"),
                       token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/accept-offer", response_model=Message, tags=[message_tag],
             description="Accept the special offer and start a trade. The offer can NOT be accepted by offer-owner!",
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def accept_offer(id: UUID = Path(..., description="Chat Id"),
                       body: AcceptOfferRequest = Body(..., description="Accept Offer Request"),
                       token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return Message


@router.post("/api/v3/chats/{id}/messages/read-all", response_model=MessageListResponseSimple, tags=[message_tag],
             description="This method marks all chat messages as read and returns the last message",
             responses={**common_api_errors,
                        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Chat not found"},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def read_all(id: UUID = Path(..., description="Chat Id"),
                   token: str = Security(oauth2_scheme, scopes=["chats:write"])):
    return MessageListResponseSimple
