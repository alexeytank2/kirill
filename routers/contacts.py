from uuid import UUID

from fastapi import APIRouter, Path, Body, Security, Depends
from fastapi import status

from dependencies import common_api_errors, oauth2_scheme, contact_tag
from models import Chat, ErrorResponse, Contact, \
    ContactListParams, ContactListResponse, NewContact

router = APIRouter()


@router.post("/api/v3/contacts", response_model=Contact, status_code=status.HTTP_201_CREATED,
             tags=[contact_tag], description="Create a new contact", deprecated=True,
             responses={**common_api_errors,
                        status.HTTP_200_OK: {"model": Contact},
                        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
                        status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def add_contact(contact: NewContact = Body(..., description="Contact to add"),
                      token: str = Security(oauth2_scheme, scopes=["contacts:write"])):
    return Contact


@router.get("/api/v3/contacts/{id}", response_model=Contact, tags=[contact_tag], deprecated=True,
            responses={**common_api_errors,
                       status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Contact not found"},
                       status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def get_contact(id: UUID = Path(..., description="Contact Id"),
                      token: str = Security(oauth2_scheme, scopes=["contacts:read"])):
    return Contact


@router.put("/api/v3/contacts/{id}", response_model=Chat, tags=[contact_tag], deprecated=True,
            responses={**common_api_errors,
                       status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Contact not found"},
                       status.HTTP_424_FAILED_DEPENDENCY: {"model": ErrorResponse}})
async def update_contact(id: UUID = Path(..., description="Contact Id"),
                         contact: Contact = Body(..., description="Contact to update"),
                         token: str = Security(oauth2_scheme, scopes=["contacts:write"])):
    return Contact


@router.get("/api/v3/contacts", response_model=ContactListResponse, tags=[contact_tag], deprecated=True,
            responses={**common_api_errors})
async def list_contacts(list_params: ContactListParams = Depends(ContactListParams),
                        token: str = Security(oauth2_scheme, scopes=["contacts:read"])):
    return ContactListResponse
