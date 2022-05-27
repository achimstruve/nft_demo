from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    OPENSEA_URL,
)
from brownie import SimpleCollectible, network

sampe_token_uri = "https://ipfs.io/ipfs/QmYdD4NWtd8cYRbos82HhKJFnuJEEdLGuQNELt41HxQsxT?filename=1-PUG.json"


def deploy_and_create():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        simple_collectable = SimpleCollectible.deploy({"from": account})
    else:
        simple_collectable = SimpleCollectible.deploy(
            {"from": account}, publish_source=True
        )

    tx = simple_collectable.createCollectible(sampe_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"NFT minted! You can see it on {OPENSEA_URL.format(simple_collectable.address, simple_collectable.tokenCounter()-1)}"
    )
    print("Please wait up to 20 minutes and hit the refresh metadata button.")
    return simple_collectable


def main():
    deploy_and_create()
