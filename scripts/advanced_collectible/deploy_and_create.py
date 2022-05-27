from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from brownie import AdvancedCollectible, network, config
from web3 import Web3


def deploy_and_create():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        advanced_collectible = AdvancedCollectible.deploy(
            get_contract("vrf_coordinator"),
            get_contract("link_token"),
            config["networks"][network.show_active()]["key_hash"],
            config["networks"][network.show_active()]["fee"],
            {"from": account},
        )
    else:
        advanced_collectible = AdvancedCollectible.deploy(
            config["networks"][network.show_active()]["vrf_coordinator"],
            config["networks"][network.show_active()]["link_token"],
            config["networks"][network.show_active()]["key_hash"],
            config["networks"][network.show_active()]["fee"],
            {"from": account},
            publish_source=True,
        )
    fund_with_link(advanced_collectible.address)
    tx = advanced_collectible.CreateCollectible({"from": account})
    tx.wait(1)
    print("New token has been created!")
    return advanced_collectible, tx


def main():
    deploy_and_create()
