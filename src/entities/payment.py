from typing import List, Optional, Union
from pydantic import BaseModel, Field
from entities.amount import Amount
from entities.recurring import Recurring
from entities.discount import Discount
from entities.person import Person
from entities.item import Item
from entities.instrument import Instrument
from entities.payment_modifier import PaymentModifier
from mixins.fields_mixin import FieldsMixin


class Payment(BaseModel, FieldsMixin):
    reference: str = Field(..., description="Payment reference")
    description: str = Field(
        default="", description="Description of the payment")
    amount: Optional[Amount] = Field(
        default=None, description="Amount information")
    allowPartial: bool = Field(
        default=False, description="Allow partial payments")
    shipping: Optional[Person] = Field(
        default=None, description="Shipping details")
    items: List[Item] = Field(default_factory=list,
                              description="List of items")
    recurring: Optional[Recurring] = Field(
        default=None, description="Recurring payment details"
    )
    payment: Optional[Instrument] = Field(
        default=None, description="Instrument payment details"
    )
    discount: Optional[Discount] = Field(
        default=None, description="Discount information"
    )
    subscribe: bool = Field(default=False, description="Subscribe flag")
    agreement: Optional[int] = Field(default=None, description="Agreement ID")
    agreementType: str = Field(default="", description="Type of agreement")
    modifiers: List[PaymentModifier] = Field(
        default_factory=list, description="List of payment modifiers"
    )

    def set_items(self, items: Union[List[dict], List[Item]]) -> None:
        """
        Set the items for the payment.
        """
        self.items = [
            Item(**item) if isinstance(item, dict) else item for item in items
        ]

    def items_to_array(self) -> List[dict]:
        """
        Convert the items list to an array of dictionaries.
        """
        return [item.model_dump() for item in self.items]

    def set_modifiers(
        self, modifiers: Union[List[dict], List[PaymentModifier]]
    ) -> None:
        """
        Set the payment modifiers.
        """
        self.modifiers = [
            PaymentModifier(**mod) if isinstance(mod, dict) else mod
            for mod in modifiers
        ]

    def modifiers_to_array(self) -> List[dict]:
        """
        Convert the modifiers list to an array of dictionaries.
        """
        return [modifier.model_dump() for modifier in self.modifiers]

    def to_dict(self) -> dict:
        """
        Convert the Payment object to a dictionary, including nested objects.
        """
        return {
            "reference": self.reference,
            "description": self.description,
            "amount": self.amount.model_dump() if self.amount else None,
            "allowPartial": self.allowPartial,
            "shipping": self.shipping.model_dump() if self.shipping else None,
            "items": self.items_to_array(),
            "recurring": self.recurring.model_dump() if self.recurring else None,
            "discount": self.discount.model_dump() if self.discount else None,
            "subscribe": self.subscribe,
            "agreement": self.agreement,
            "agreementType": self.agreementType,
            "modifiers": self.modifiers_to_array(),
            "fields": self.fields_to_array(),
        }
