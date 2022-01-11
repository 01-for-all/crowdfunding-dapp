from brownie import CrowdFunding,MockV3Aggregator,network,config 
from scripts.helpful_scripts import (
    deploy_mocks, 
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

def deploy_crowd_funding():
    account = get_account() 
    # pass the price feed address to our fundme contract
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # live chain 
        price_feed_address = config["network"][network.show_active()]["eth_usd_price_feed"]
    else:
        # development chain
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        

    crowd_funding = CrowdFunding.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {crowd_funding.address}")


def main():
    deploy_crowd_funding() 
