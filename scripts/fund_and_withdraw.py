from brownie import CrowdFunding
from scripts.helpful_scripts import get_account


def fund():
    crowd_funding = CrowdFunding[-1]
    account = get_account()
    entrance_fee = crowd_funding.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    crowd_funding.fund({"from": account, "value": entrance_fee})


def withdraw():
    crowd_funding = CrowdFunding[-1]
    account = get_account()
    crowd_funding.withdraw({"from": account})


def main():
    fund()
    withdraw()
