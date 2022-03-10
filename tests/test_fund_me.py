from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENT,
)
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and network.show_active() not in FORKED_LOCAL_ENVIRONMENT
    ):
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad = accounts.add()
    good = get_account()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad})
