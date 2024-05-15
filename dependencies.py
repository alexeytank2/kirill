from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import status

from models import ValidationErrorResponse, ErrorResponse


profile_tag = "Profile API"
chat_tag = "Chat API"
contact_tag = "Contact API"
trade_tag = "Trade List API"
message_tag = "Chat Message API"
attachment_tag = "Chat Attachment API"
internal_tag = "Internal API"


oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="url", tokenUrl="url",
                                              scopes={"chats:write": "Chats",
                                                      "chats:read": "Chats",
                                                      # "contacts:write": "Contacts",
                                                      # "contacts:read": "Contacts",
                                                      "profile:read": "Profile",
                                                      "profile:write": "Profile"})

common_api_errors = {
    status.HTTP_401_UNAUTHORIZED: {},
    status.HTTP_403_FORBIDDEN: {},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}
}

common_internal_api_errors = {
    status.HTTP_403_FORBIDDEN: {},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}
}