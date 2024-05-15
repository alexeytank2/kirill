from enum import Enum

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union, Dict, Any, Type
from uuid import UUID


class ContactTypeEnum(str, Enum):
    TRUSTED = "TRUSTED"
    BLOCKED = "BLOCKED"


class CustomerStatusEnum(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class ChatContextStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    SYSTEM = "SYSTEM"
    BLOCKED = "BLOCKED"
    HIDDEN = "HIDDEN"
    MARKETING = "MARKETING"


class Customer(BaseModel):
    customer_id: UUID = Field(description="Customer Id")
    username: str = Field(description="Username", example="RichJason", readOnly=True)
    avatar_url: str = Field(readOnly=True, example="https://example.com/avatar/RichJason.png")
    display_name: str = Field(description="Display name", example="Rich Jason", readOnly=True)
    status: CustomerStatusEnum = Field(readOnly=True, example=CustomerStatusEnum.ONLINE)
    country: Optional[str] = Field(description="Country ISO2 code from profile", example="RU", readOnly=True)


class NewContact(BaseModel):
    customer_id: UUID = Field(description="Contact id (customer id of contact)")
    display_name: str = Field(description="Display name", example="Rich Jason")
    type: Optional[ContactTypeEnum] = Field(description="Contact type", example=ContactTypeEnum.TRUSTED)


class Contact(BaseModel):
    customer_id: UUID = Field(description="Contact id (customer id of contact)", readOnly=True)
    username: str = Field(description="Username", example="RichJason", readOnly=True)
    display_name: str = Field(description="Display name", example="Rich Jason")
    email_verified: bool = Field(readOnly=True)
    phone_verified: bool = Field(readOnly=True)
    bio: str = Field(description="Bio", readOnly=True, example="Some words about RichJason")
    avatar_url: str = Field(readOnly=True, example="https://example.com/avatar/RichJason.png")
    location: str = Field(description="Location", readOnly=True, example="US")
    create_time: datetime = Field(description="User's registration time", readOnly=True, example="2021-04-01T10:34:15Z")
    type: ContactTypeEnum = Field(description="Contact type", example=ContactTypeEnum.TRUSTED)


class Token(BaseModel):
    token: str
    expire_time: str = Field(description="Token expiration time", readOnly=True)
    remaining_seconds: int = Field(description="Remaining seconds till token expiration or 0 is token was already"
                                               " expired", readOnly=True, example=10000)
    inbox_channel: str = Field(description="Personal inbox channel name", readOnly=True)
    subscribe_key: str = Field(description="key for subscription", readOnly=True)


class AcceptChatMessagesEnum(str, Enum):
    YES = "YES"
    NO = "NO"
    TRUSTED_ONLY = "TRUSTED_ONLY"
    TRUSTED_AND_TRADE_PARTNERS = "TRUSTED_AND_TRADE_PARTNERS"


class FeatureFlags(BaseModel):
    messenger_enabled_for_user: bool = Field(readOnly=True)
    adabot_global: bool = Field(readOnly=True)


class Profile(Customer):
    token: Token = Field()
    accept_chat_messages: AcceptChatMessagesEnum = Field(readOnly=True)
    chats_unread_count: int = Field(readOnly=True)
    trades_unread_count: int = Field(readOnly=True)
    system_unread_count: int = Field(readOnly=True)
    marketing_unread_count: int = Field(readOnly=True)
    feature_flags: FeatureFlags = Field(readOnly=True)
    email: str = Field(readOnly=True)


class ProfileUpdate(BaseModel):
    accept_chat_messages: AcceptChatMessagesEnum = Field(deprecated=True)


class ReadAllMessagesReq(BaseModel):
    status: str = Field(description="A comma-separated array of chat statuses. The method will reset"
                                    " chats with requested context statuses.",
                        example=ChatContextStatusEnum.ACTIVE)


class ProfileBase(BaseModel):
    customer_id: UUID = Field(description="Customer Id")
    status: CustomerStatusEnum = Field(readOnly=True, example=CustomerStatusEnum.ONLINE)
    accept_chat_messages: AcceptChatMessagesEnum = Field(readOnly=True)


class ProfileBaseWithChatId(ProfileBase):
    chat_id: Optional[UUID] = Field(description="Chat id with that customer", readOnly=True, deprecated=True)


class MessageStatusEnum(str, Enum):
    NEW = "NEW"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
    UPDATED = "UPDATED"
    HIDDEN = "HIDDEN"


class MarketingMessageStatusEnum(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class MessageTypeEnum(str, Enum):
    MESSAGE = "MESSAGE"
    FILE = "FILE"
    SPECIAL_TRADE = "SPECIAL_TRADE"
    SPECIAL_OFFER = "SPECIAL_OFFER"
    SYSTEM = "SYSTEM"
    INTERNAL_TRANSFER = "INTERNAL_TRANSFER"


class MessageAttachment(BaseModel):
    filename: str = Field(description="File name", example="image.png")
    uri: str = Field(description="Attachment uri", example="https://google.com/image.png")
    thumbnail_uri: str = Field(description="Attachment thumbnail uri", example="https://google.com/small_image.png",
                               readOnly=True)


class FileContent(BaseModel):
    filename: str = Field(description="File name", example="image.png")
    file: str = Field(description="File to upload. Supported formats are jpeg, png, jpg. Files up to 10mb are only "
                                  "allowed.")


class OfferTypeEnum(str, Enum):
    sell = "sell"
    buy = "buy"


class TradeStatusEnum(str, Enum):
    not_funded = "Not funded"
    funds_processing = "Funds processing"
    funds_processed = "Funds processed"
    active_funded = "Active funded"
    paid = "Paid"
    cancelled_system = "Cancelled system"
    cancelled_buyer = "Cancelled buyer"
    cancelled_seller = "Cancelled seller"
    released = "Released"
    dispute_open = "Dispute open"
    dispute_wins_seller = "Dispute wins seller"
    dispute_wins_buyer = "Dispute wins buyer"


class CheckChatCreationResultEnum(str, Enum):
    COULD_NOT_START = "COULD_NOT_START"
    ALREADY_STARTED = "ALREADY_STARTED"
    COULD_START = "COULD_START"


class CheckChatCreationErrorCodeEnum(str, Enum):
    user_banned = "user_banned"
    chat_blocked = "chat_blocked"
    privacy_settings = "privacy_settings"
    could_not_start = "could_not_start"


class SystemMessagePlaceholders(BaseModel):
    hash: Optional[str] = Field(example="F8Mc6Jejy9G", title="Trade hash")


class SystemMessageParameters(BaseModel):
    type: Optional[str] = Field(example="referrer_message", title="Message type")
    link: Optional[str] = Field(example="/user/superman", title="Optional link")
    link_text: Optional[str] = Field(example="Go to chat room", title="Optional link text")
    message: Optional[str] = Field(example="John joined by your invite link",
                                   title="Optional message, the same as text")
    title: Optional[str] = Field(example="Daily Life of NoOnes Guys",
                                 title="Optional title for message")
    chat_id: Optional[UUID] = Field(title="Optional chat_id, applicable to referrer_message and referral_message")
    message_placeholders: Optional[SystemMessagePlaceholders] = Field(title="Optional structure")


class SpecialOfferParameters(BaseModel):
    offer_type: OfferTypeEnum = Field(example=OfferTypeEnum.sell)
    crypto_currency: str = Field(example="BTC", title="Crypto currency code")
    fiat_currency: str = Field(example="USD", title="Fiat currency code")
    fiat_price_per_crypto: str = Field(example="19900", format="decimal")
    crypto_amount: str = Field(example="0.005",
                               title="Amount of crypto currency, includes the eighth decimal place for BTC (1 SATS)",
                               format="decimal")
    fee_percentage: str = Field(example="2", format="decimal")
    fiat_amount: str = Field(example="100",
                             title="Amount of fiat currency, usually includes the second decimal place (1 cent)",
                             format="decimal")
    payment_method_name: str = Field(example="Amazon Gift Card")
    payment_method_slug: str = Field(example="amazon-gift-card")
    margin: str = Field(example="19900", format="decimal")

    crypto_to_fiat_amount: str = Field(example="99.5", format="decimal")
    fee_crypto_amount: str = Field(example="0.0001", format="decimal")
    fee_crypto_to_fiat_amount: str = Field(example="2.5", format="decimal")
    crypto_amount_total: str = Field(example="0.0051", format="decimal")
    crypto_to_fiat_amount_total: str = Field(example="100.5", format="decimal")

    active: bool = Field(example=True)
    offer_owner_id: UUID = Field(description="Customer who makes the offer")
    offer_accepted: bool = Field(example=False)
    offer_terms: str = Field(example="offer terms", deprecated=True)


class SpecialTradeParameters(BaseModel):
    offer_type: OfferTypeEnum = Field(example=OfferTypeEnum.sell)
    crypto_currency: str = Field(example="BTC", title="Crypto currency code")
    fiat_currency: str = Field(example="USD", title="Fiat currency code")
    fiat_price_per_crypto: str = Field(example="19900", format="decimal")
    crypto_amount_requested: str = Field(example="0.005",
                                         title="Amount of crypto currency, includes the eighth decimal place for BTC (1 SATS)",
                                         format="decimal")
    crypto_amount_total: str = Field(example="0.0051", format="decimal")
    fee_percentage: str = Field(example="2", format="decimal")
    fee_crypto_amount: str = Field(example="0.0001", format="decimal")
    fiat_amount_requested: str = Field(example="100",
                                       title="Amount of fiat currency, usually includes the second decimal place (1 cent)",
                                       format="decimal")
    payment_method_name: str = Field(example="Amazon Gift Card")
    payment_method_slug: str = Field(example="amazon-gift-card")
    margin: str = Field(example="19900", format="decimal")

    crypto_to_fiat_amount: str = Field(example="99.5", format="decimal")
    fee_crypto_to_fiat_amount: str = Field(example="2.5", format="decimal")
    crypto_to_fiat_amount_total: str = Field(example="100.5", format="decimal")

    offer_terms: str = Field(example="offer terms", deprecated=True)
    trade_status: TradeStatusEnum = Field(example=TradeStatusEnum.active_funded)
    offer_owner_id: UUID = Field(description="Customer who makes the offer")


class InternalTransferParameters(BaseModel):
    id: str = Field(example="1f3d24a1-3fb0-44f7-9a88-cf2f31d0d2cc", title="Operation id at Operation History")
    status: str = Field(example="success")
    crypto_currency: str = Field(example="BTC", title="Crypto currency code")
    fiat_currency: str = Field(example="USD", title="Fiat currency code")
    crypto_amount: str = Field(example="0.005",
                               title="Amount of crypto currency, includes the eighth decimal place for BTC (1 SATS)",
                               format="decimal")
    fiat_amount: str = Field(example="100",
                             title="Amount of fiat currency, usually includes the second decimal place (1 cent)",
                             format="decimal")
    sender_customer_id: UUID = Field(description="Customer who sends the crypto")

    crypto_total_amount: Optional[str] = Field(example="0.0051", format="decimal")
    crypto_fee: Optional[str] = Field(example="0.0001", format="decimal")
    fiat_total_amount: Optional[str] = Field(example="100.2", format="decimal")
    fiat_fee: Optional[str] = Field(example="0.2", format="decimal")


class MessageSimple(BaseModel):
    external_request_id: Optional[str] = Field(example="bb638f26-7064-4285-94b3-ce5d48f29b9b", max_length=40,
                                               title="Idempotence key, provided by the caller")
    message_id: UUID = Field(description="Message id", readOnly=True)
    create_time: datetime = Field(description="Message creation time", readOnly=True,
                                  example="2021-04-01T10:34:15Z")
    text: Optional[str] = Field(description="Message text, up to 1024 symbols",
                                example="Hello!", max_length=1024)
    author_id: UUID = Field(description="Id of Customer who wrote the message", readOnly=True)
    is_mine: bool = Field(description="Is this message written by me?", readOnly=True)
    status: MessageStatusEnum = Field(description="Message delivery status", readOnly=True,
                                      example=MessageStatusEnum.DELIVERED)
    type: MessageTypeEnum = Field(description="Message type", readOnly=True,
                                  example=MessageTypeEnum.MESSAGE)
    parameters: Optional[Union[SpecialTradeParameters, SpecialOfferParameters, InternalTransferParameters,
    SystemMessageParameters]] = \
        Field(description="Optional list of key-value parameters, mostly used with specific message types",
              readOnly=True)
    update_time: Optional[datetime] = Field(description="Message update time", readOnly=True,
                                            example="2021-04-02T11:34:15Z")
    offer_hash: Optional[str] = Field(example="MJkEzVgCaMT", max_length=40,
                                      description="Optional Offer Hash, applicable to SPECIAL_OFFER and SPECIAL_TRADE")
    trade_hash: Optional[str] = Field(example="lJkgEzVgCaT", max_length=40,
                                      description="Optional Trade Hash, applicable to SPECIAL_TRADE type")


class Message(MessageSimple):
    attachments: Optional[List[MessageAttachment]] = Field(readOnly=True)
    prev_message_id: Optional[UUID] = Field(description="Previous message id", readOnly=True)


class MessageIds(BaseModel):
    message_ids: List[str] = Field(description="Message Ids")


class CancelOfferRequest(BaseModel):
    offer_hash: str = Field(example="MJkEzVgCaMT", max_length=40, description="Offer Hash")


class AcceptOfferRequest(BaseModel):
    offer_hash: str = Field(example="MJkEzVgCaMT", max_length=40, description="Offer Hash")


class CustomerIds(BaseModel):
    customer_ids: List[str] = Field(description="Customer Ids")
    return_chat_id: Optional[bool] = Field(description="Return chat_id for the requested customers if it was "
                                                       "created previously", default=False, deprecated=True)


class CheckRespondersInternalRequest(BaseModel):
    customer_id: UUID = Field(description="Id of Customer from whose perspective the request is sent")
    responder_ids: List[str] = Field(description="Partner (responder) Ids")
    return_chat_id: Optional[bool] = Field(description="Return chat_id for the requested partners if it was "
                                                       "created previously", default=False)


class CheckChatCreationInternalRequest(BaseModel):
    customer_id: UUID = Field(description="Id of Customer from whose perspective the request is sent")
    partner_id: UUID = Field(description="Partner (responder) Id")


class SystemMessage(BaseModel):
    customer_id: UUID = Field(description="Id of Customer who receives the system notification")
    text: str = Field(description="Message text, up to 1024 symbols",
                      example="New trade 68rvszsmCot for Gift Card", max_length=1024)
    parameters: Optional[Dict[str, str]] = Field(
        description="Optional list of key-value parameters, mostly used with "
                    "specific message types", example={"type": "trade_started_receiver",
                                                       "link": "https://noones.com/p2p/trade/68rvszsmCot",
                                                       "link_text": "view trade"})


class ChatContext(BaseModel):
    chat_name: str = Field(description="Optional chat name, could be named automatically", example="Chat with John")
    delivered_message_id: Optional[UUID] = Field(description="Last delivered message id to current user",
                                                 readOnly=True, deprecated=True)
    read_message_id: Optional[UUID] = Field(description="Last read message id by current user", readOnly=True)
    status: Optional[ChatContextStatusEnum] = Field(default=ChatContextStatusEnum.ACTIVE, readOnly=True)
    unread_count: int = Field(readOnly=True)
    update_time: datetime = Field(description="Last chat update time", readOnly=True,
                                  example="2021-04-01T10:34:15Z")
    activity_time: datetime = Field(description="Last chat activity time (chat creation or message creation)",
                                    readOnly=True,
                                    example="2021-04-01T10:34:15Z")
    blocked_by_me: bool = Field(description="Is this chat blocked by me (and can be unblocked)", readOnly=True)


class Chat(BaseModel):
    chat_id: UUID = Field(description="Chat id", readOnly=True)
    partner: Customer = Field(description="Other party of chat, could be chat responder or originator", readOnly=True)
    last_message: Optional[MessageSimple] = Field(description="Last message")
    context: ChatContext = Field(description="Customer specific chat context")


class ChatDetails(Chat):
    moderator: Optional[Customer] = Field(description="Moderator", readOnly=True)
    me: Customer = Field(description="Current user profile", readOnly=True)
    is_started_by_me: bool = Field(description="Is this chat was started/created by me", readOnly=True)


class ChatReadiness(BaseModel):
    partner: Customer = Field(description="Other party of chat, could be chat responder", readOnly=True)


class FiatCurrency(BaseModel):
    currency_code: str = Field(example="USD", title="Fiat currency code")
    amount: str = Field(example="10.12",
                        title="Amount of fiat currency, usually includes the second decimal place (1 cent)",
                        format="decimal")


class CryptoCurrency(BaseModel):
    currency_code: str = Field(example="BTC", title="Crypto currency code")
    amount: str = Field(example="0.00017614",
                        title="Amount of crypto currency, includes the eighth decimal place for BTC (1 SATS)",
                        format="decimal")


class TradeContext(BaseModel):
    trade_name: str = Field(description="User-centric trade name, could be named automatically",
                            example="Trade with John")
    unread_count: int = Field(readOnly=True)
    update_time: datetime = Field(description="Last trade activity/update time", readOnly=True,
                                  example="2021-04-01T10:34:15Z")


class OfferInfo(BaseModel):
    offer_type: OfferTypeEnum = Field(example="sell", readOnly=True,
                                      description="Offer Type from Offer-Maker's perspective. It will be "
                                                  "'sell' if the User is to buying crypto and vice versa.")
    offer_owner_id: UUID = Field(readOnly=True)
    offer_margin: str = Field(example="5.0", readOnly=True,
                              description="A percent that determines differences between market price and the price of "
                                          "the offer.")
    payment_method_slug: Optional[str] = Field(example="bank-transfer",
                                               description="Payment method slug. For a list of payment method slugs "
                                                           "please refer to payment-method/list endpoint at "
                                                           "developers.noones.com")
    payment_method_name: Optional[str] = Field(example="bank-transfer",
                                               description="Payment method name")


class Trade(BaseModel):
    trade_hash: str = Field(example="MJkEzVgCaMT", readOnly=True, max_length=40, description="Trade Hash")
    crypto: Optional[CryptoCurrency] = Field(description="Amount and code of buying/selling crypto", deprecated=True)
    fiat: Optional[FiatCurrency] = Field(description="Amount and code of fiat to pay/get", deprecated=True)
    crypto_currency: str = Field(example="BTC", title="Crypto currency code")
    fiat_currency: str = Field(example="USD", title="Fiat currency code")
    crypto_amount_requested: str = Field(example="0.005",
                                         title="Amount of crypto currency, includes the eighth decimal place for BTC "
                                               "(1 SATS)",
                                         format="decimal")
    fiat_amount_requested: str = Field(example="100",
                                       title="Amount of fiat currency, usually includes the second decimal place "
                                             "(1 cent)",
                                       format="decimal")
    crypto_to_fiat_amount: str = Field(example="99.5", format="decimal")
    create_time: datetime = Field(description="Trade creation time", readOnly=True)
    status: TradeStatusEnum = Field(example=TradeStatusEnum.active_funded, readOnly=True,
                                    title="Simplified status of Trade")
    offer: OfferInfo = Field(description="Trade Offer info", readOnly=True)
    partner: Customer = Field(description="Other party of trade, could be offer-maker or offer-taker", readOnly=True)
    context: TradeContext = Field(description="Customer specific trade context")


class TradeDetails(Trade):
    me: Customer = Field(description="Current user profile", readOnly=True)


class NewChat(BaseModel):
    partner: Customer = Field(description="Other party of chat")
    context: Optional[ChatContext] = Field(description="Customer specific chat context")
    message: Optional[Message] = Field(description="Optional initial message")


class CheckChatCreationInternalResponse(BaseModel):
    result: CheckChatCreationResultEnum = Field(example=CheckChatCreationResultEnum.COULD_NOT_START, readOnly=True,
                                                title="Ability to start chat with the given partner/responder")
    error_code: Optional[CheckChatCreationErrorCodeEnum] = Field(
        example=CheckChatCreationErrorCodeEnum.privacy_settings,
        readOnly=True,
        title="Additional Error code for result=COULD_NOT_START")
    chat_id: Optional[UUID] = Field(description="Existent chat id with that partner/responder, if "
                                                "result=ALREADY_STARTED", readOnly=True)


class MarketingMessage(BaseModel):
    external_request_id: Optional[str] = Field(example="bb638f26-7064-4285-94b3-ce5d48f29b9b", max_length=40,
                                               title="Idempotence key, provided by the caller")
    marketing_id: UUID = Field(description="Marketing Message id", readOnly=True)
    text: str = Field(description="Message text",
                      example="Hello bro! We've got a new cool feature - BSC network support")
    title: Optional[str] = Field(description="Message title, actually, not used", example="")
    status: MarketingMessageStatusEnum = Field(description="Message status, PENDING - when message is created but "
                                                           "should not be visible to the users until start_time",
                                               readOnly=True,
                                               example=MarketingMessageStatusEnum.PENDING)
    link: Optional[str] = Field(example="https://noones.com/wallet")
    link_text: Optional[str] = Field(example="Go To Wallet")
    create_time: datetime = Field(description="Message creation time", readOnly=True,
                                  example="2021-04-01T10:34:15Z")
    update_time: Optional[datetime] = Field(description="Message update time", readOnly=True,
                                            example="2021-04-02T11:34:15Z")
    start_time: Optional[datetime] = Field(description="Time when message should be delivered to the user",
                                           example="2021-04-02T11:34:15Z")
    author: str = Field(description="Email of marketing message creator", example="superman@noones.team")


class MarketingMessageUpdateReq(BaseModel):
    text: str = Field(description="Message text",
                      example="Hello bro! We've got a new cool feature - BSC network support")
    title: Optional[str] = Field(description="Message title, actually, not used", example="")
    link: Optional[str] = Field(example="https://noones.com/wallet")
    link_text: Optional[str] = Field(example="Go To Wallet")
    start_time: Optional[datetime] = Field(description="Time when message should be delivered to the user",
                                           example="2021-04-02T11:34:15Z")
    status: Optional[MarketingMessageStatusEnum] = Field(description="Message status",
                                                         example=MarketingMessageStatusEnum.DELETED)


class ListParams:
    def __init__(self, page_token: Optional[str] = Query(None,
                                                         description="The next page key. Should be a resource identifier",
                                                         example="5498da1bf83a61f58ef6c6d4"),
                 limit: Optional[int] = Query(20, description="Max records to return in a List response. If not set, "
                                                              "a default value will be used")):
        self.page_token = page_token
        self.limit = limit


class ChatListParams:
    def __init__(self, list_params: ListParams = Depends(ListParams),
                 q: Optional[str] = Query(None, description="Optional search query. Will be applied as searchable "
                                                            "substring for following chat attributes: "
                                                            "context.chat_name", ),
                 statuses: Optional[str] = Query(None,
                                                 description="An optional comma-separated array of chat statuses. If "
                                                             "specified, the method will return chats with "
                                                             "requested context statuses. Otherwise, it will return "
                                                             "all chats.",
                                                 example=ChatContextStatusEnum.ACTIVE)):
        self.basic_params = list_params
        self.q = q
        self.statuses = statuses


class TradeListParams:
    def __init__(self,
                 limit: Optional[int] = Query(10, description="Max records to return in a List response. If not set, "
                                                              "a default value will be used"),
                 statuses: Optional[str] = Query(None,
                                                 description="An optional comma-separated array of trade statuses. If "
                                                             "specified, the method will return chats with "
                                                             "requested statuses.",
                                                 example=TradeStatusEnum.active_funded)):
        self.limit = limit
        self.statuses = statuses


class MessageListParams:
    def __init__(self, list_params: ListParams = Depends(ListParams),
                 last_message_id: UUID = Query(None, description="Optional filter: from last message id"),
                 order_by: str = Query(None, description="Optional sorting order. Only 'create_time desc' supported",
                                       example="create_time desc")):
        self.basic_params = list_params
        self.order_by = order_by
        self.last_message_id = last_message_id


class MarketingMessageListParams:
    def __init__(self, list_params: ListParams = Depends(ListParams),
                 statuses: Optional[str] = Query(None,
                                                 description="An optional comma-separated array of marketing message "
                                                             "statuses. If specified, the method will return messages "
                                                             "with requested statuses. Otherwise, it will return all "
                                                             "messages.",
                                                 example=MarketingMessageStatusEnum.ACTIVE)):
        self.basic_params = list_params
        self.statuses = statuses


class ContactListParams:
    def __init__(self, list_params: ListParams = Depends(ListParams),
                 q: Optional[str] = Query(None, description="Optional search query. Will be applied as searchable "
                                                            "substring for following contact attributes: username "
                                                            "or display_name",
                                          example="Rich"),
                 types: Optional[str] = Query(None,
                                              description="An optional comma-separated array of operation contact "
                                                          "types. If specified, the method will return contacts with "
                                                          "requested types. Otherwise, it will return all contacts.",
                                              example=ContactTypeEnum.TRUSTED)):
        self.basic_params = list_params
        self.q = q
        self.types = types


class ListResponse(BaseModel):
    limit: int = Field(default=20,
                       description="The effective value of the 'limit' parameter used to process this request. If the"
                                   " 'limit' parameter was not specified in the request, the default limit is returned.")
    next_page_token: Optional[str] = Field(example="5498da1bf83a61f58ef6c6d4",
                                           description="The next page token for use in the 'page_token' argument of a subsequent "
                                                       "paged request. The value must be URL-friendly, either in "
                                                       "percent-encoding or Base64url. It will be null for the last page.")
    prev_page_token: Optional[str] = Field(example="5498da1bf83a61f58ef6c6d4",
                                           description="The previous page token for use in the page_token parameter in a "
                                                       "subsequent paged request. The value must be URL-friendly, either in "
                                                       "percent-encoding or Base64url.")


class ChatListResponse(ListResponse):
    items: List[Chat] = Field(description="An array of arbitrary Chat objects")


class TradeListResponse(BaseModel):
    items: List[Trade] = Field(description="An array of arbitrary Trade objects")


class MessageListResponse(ListResponse):
    items: List[Message] = Field(description="An array of arbitrary Message objects")


class MessageListResponseSimple(BaseModel):
    items: List[Message] = Field(description="An array of arbitrary Message objects")


class ContactListResponse(ListResponse):
    items: List[Contact] = Field(description="An array of arbitrary Contact objects")


class ProfileBaseListResponse(BaseModel):
    items: List[ProfileBaseWithChatId] = Field(description="An array of arbitrary Profile objects")


class MarketingMessageListResponse(ListResponse):
    items: List[MarketingMessage] = Field(description="An array of arbitrary MarketingMessage objects")


class ErrorResponse(BaseModel):
    code: str = Field(readOnly=True)
    message: str = Field(readOnly=True)


class ValidationError(BaseModel):
    loc: List[str] = Field(title="Location", readOnly=True)
    msg: str = Field(title="Location", readOnly=True)
    type: str = Field(title="Error Type", readOnly=True)


class ValidationErrorResponse(ErrorResponse):
    details: Optional[List[ValidationError]] = Field(None, description="Optional error details", readOnly=True)
