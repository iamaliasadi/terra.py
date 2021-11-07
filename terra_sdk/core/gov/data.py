"""Gov module data types."""

from __future__ import annotations

import copy
from typing import Union, List

import attr
from dateutil import parser
from terra_proto.cosmos.gov.v1beta1 import Proposal as Proposal_pb
from terra_proto.cosmos.gov.v1beta1 import TallyResult as TallyResult_pb

from terra_sdk.core import Coins, AccAddress
from terra_sdk.core.distribution import CommunityPoolSpendProposal
from terra_sdk.core.params import ParameterChangeProposal
from terra_sdk.core.upgrade import (
    CancelSoftwareUpgradeProposal,
    SoftwareUpgradeProposal,
)
from terra_sdk.util.json import JSONSerializable, dict_to_data
from terra_proto.cosmos.gov.v1beta1 import (
    VoteOption,
    WeightedVoteOption as WeightedVoteOption_pb,
    Vote as Vote_pb
)

from .proposals import TextProposal

__all__ = ["Proposal", "Content", "VoteOption", "WeightedVoteOption"]


Content = Union[
    TextProposal,
    CommunityPoolSpendProposal,
    ParameterChangeProposal,
    SoftwareUpgradeProposal,
    CancelSoftwareUpgradeProposal,
]


@attr.s
class TallyResult(JSONSerializable):
    yes: str = attr.ib()
    abstain: str = attr.ib()
    no: str = attr.ib()
    no_with_veto: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TallyResult:
        return cls(
            yes=data["yes"],
            abstain=data["abstain"],
            no=data["no"],
            no_with_veto=data["no_with_veto"],
        )

    def to_proto(self) -> TallyResult_pb:
        return TallyResult_pb(
            yes=self.yes,
            abstain=self.abstain,
            no=self.no,
            no_with_veto=self.no_with_veto,
        )


@attr.s
class Proposal(JSONSerializable):
    """Contains information about a submitted proposal on the blockchain."""

    proposal_id: int = attr.ib(converter=int)
    """Proposal's ID."""

    content: Content = attr.ib()
    """Proposal contents."""

    status: str = attr.ib()
    """Status of proposal."""

    final_tally_result: TallyResult = attr.ib()
    """Final tallied result of the proposal (after vote)."""

    submit_time: str = attr.ib()
    """Timestamp at which proposal was submitted."""

    deposit_end_time: str = attr.ib()
    """Time at which the deposit period ended, or will end."""

    total_deposit: Coins = attr.ib(converter=Coins)
    """Total amount deposited for proposal"""

    voting_start_time: str = attr.ib()
    """Time at which voting period started, or will start."""

    voting_end_time: str = attr.ib()
    """Time at which voting period ended, or will end."""

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["id"] = str(d["id"])
        return dict_to_data(d)

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        return cls(
            proposal_id=data["proposal_id"],
            content=Content.from_data(data["content"]),
            status=data["status"],
            final_tally_result=data["final_tally_result"],
            submit_time=data["submit_time"],
            deposit_end_time=data["deposit_end_time"],
            total_deposit=Coins.from_data(data["total_deposit"]),
            voting_start_time=data["voting_start_time"],
            voting_end_time=data["voting_end_time"],
        )

    def to_proto(self) -> Proposal_pb:
        return Proposal_pb(
            proposal_id=self.proposal_id,
            content=self.content.pack_any(),
            status=self.status,
            final_tally_result=self.final_tally_result.to_proto(),
            submit_time=parser.parse(self.submit_time),
            deposit_end_time=parser.parse(self.deposit_end_time),
            total_deposit=self.total_deposit.to_proto(),
            voting_start_time=parser.parse(self.voting_start_time),
            voting_end_time=parser.parse(self.voting_end_time),
        )


@attr.s
class WeightedVoteOption(JSONSerializable):
    weight: str = attr.ib()
    option: VoteOption = attr.ib(converter=int)

    @classmethod
    def from_data(cls, data: dict) -> WeightedVoteOption:
        return cls(option=data["option"], weight=data["weight"])

    def to_proto(self) -> WeightedVoteOption_pb:
        return WeightedVoteOption_pb(
            option=self.option,
            weight=self.weight
        )


@attr.s
class Vote(JSONSerializable):
    proposal_id: int = attr.ib(converter=int)
    voter: AccAddress = attr.ib()
    options: List[WeightedVoteOption] = attr.ib(converter=list)

    @classmethod
    def from_data(cls, data: dict) -> Vote:
        return cls(
            proposal_id=data["proposal_id"],
            voter=data["voter"],
            options=data["options"]
        )

    def to_proto(self) -> Vote_pb:
        return Vote_pb(
            proposal_id=self.proposal_id,
            voter=self.voter,
            options=self.options
        )
