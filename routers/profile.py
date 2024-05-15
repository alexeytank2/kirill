from fastapi import APIRouter, Security, Body
from fastapi import status

from dependencies import common_api_errors, oauth2_scheme, profile_tag
from models import Profile, Token, ProfileUpdate, ReadAllMessagesReq

router = APIRouter()


@router.get("/api/v3/profile", status_code=status.HTTP_200_OK,
            response_model=Profile,
            tags=[profile_tag], description="Read user profile",
            responses={**common_api_errors})
async def read_profile(token: str = Security(oauth2_scheme, scopes=["profile:read"])):
    return Profile


@router.post("/api/v3/profile/request-token", status_code=status.HTTP_200_OK,
             response_model=Token,
             tags=[profile_tag], description="Request channel token for subscription",
             responses={**common_api_errors})
async def request_token(token: str = Security(oauth2_scheme, scopes=["profile:read"])):
    return Token


@router.post("/api/v3/profile/read-all-trades", status_code=status.HTTP_200_OK,
             response_model=Profile,
             tags=[profile_tag], description="Mark all trades in a list as read and reset trades_unread_count to 0",
             responses={**common_api_errors})
async def read_all_trades(token: str = Security(oauth2_scheme, scopes=["profile:read"])):
    return Profile


@router.patch("/api/v3/profile", status_code=status.HTTP_200_OK,
              response_model=Profile,
              tags=[profile_tag], description="Update user profile",
              responses={**common_api_errors})
async def update_profile(profile: ProfileUpdate = Body(..., description="Profile to update"),
                         token: str = Security(oauth2_scheme, scopes=["profile:write"])):
    return Profile


@router.post("/api/v3/profile/read-all-messages", status_code=status.HTTP_200_OK,
             response_model=Profile,
             tags=[profile_tag], description="Mark all messages for the chats with the given status as read and reset "
                                             "chats_unread_count or/and system_unread_count to 0",
             responses={**common_api_errors})
async def read_all_messages(req: ReadAllMessagesReq = Body(..., description="Chats to update"),
                            token: str = Security(oauth2_scheme, scopes=["profile:read"])):
    return Profile
