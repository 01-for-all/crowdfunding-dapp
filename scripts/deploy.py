from brownie import FundMe,MockV3Aggregator,network,config 
from scripts.helpful_scripts import (
    deploy_mocks, 
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

def deploy_fund_me():
    account = get_account() 
    # pass the price feed address to our fundme contract
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # live chain 
        price_feed_address = config["network"][network.show_active()]["eth_usd_price_feed"]
    else:
        # development chain
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me() 