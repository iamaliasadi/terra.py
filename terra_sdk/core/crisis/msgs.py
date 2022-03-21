"""Crisis module message types."""

from __future__ import annotations

from typing import Any

from terra_proto.cosmos.crisis.v1beta1 import MsgVerifyInvariant as MsgVerifyInvariant_pb

from terra_sdk.core import AccAddress
from terra_sdk.core.msg import Msg

__all__ = ["MsgVerifyInvariant"]

import attr


@attr.s
class MsgVerifyInvariant(Msg):
    """ MsgVerifyInvariant represents a message to verify a particular invariance.

    Args:
        sender: address of the sender
        invariant_module_name: module name to verify invariant
        invariant_route: route to veriryf
    """

    type_amino = "crisis/MsgVerifyInvariant"
    """"""
    type_url = "/cosmos.crisis.v1beta1.MsgVerifyInvariant"
    """"""

    sender: AccAddress = attr.ib()
    invariant_module_name: str = attr.ib()
    invariant_route: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "invariant_module_name": self.invariant_module_name,
                "invariant_route": self.invariant_route
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgVerifyInvariant:
        return cls(
            sender=data["sender"],
            invariant_module_name=data["invariant_module_name"],
            invariant_route=data["invariant_route"]
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "sender": self.sender,
            "invariant_module_name": self.invariant_module_name,
            "invariant_route": self.invariant_route
        }

    @classmethod
    def from_proto(cls, proto: MsgVerifyInvariant_pb) -> MsgVerifyInvariant:
        return cls(
            sender=proto.sender,
            invariant_module_name=proto.invariant_module_name,
            invariant_route=proto.invariant_route
        )

    def to_proto(self) -> MsgVerifyInvariant_pb:
        return MsgVerifyInvariant_pb(
            sender=self.sender,
            invariant_module_name=self.invariant_module_name,
            invariant_route=self.invariant_route
        )

    @classmethod
    def unpack_any(cls, any: Any) -> MsgVerifyInvariant:
        return MsgVerifyInvariant.from_proto(any)
