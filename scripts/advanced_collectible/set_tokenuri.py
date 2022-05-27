from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account
from scripts.advanced_collectible.create_metadata import tokenId_to_metadata_uri


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    n_collectibles = advanced_collectible.tokenCounter()
    for token_id in range(n_collectibles):
        tokenURI = tokenId_to_metadata_uri[token_id]
        advanced_collectible.setTokenURI(token_id, tokenURI, {"from": account})
        print(f"Set tokenURI of tokenId {token_id} to {tokenURI}")
