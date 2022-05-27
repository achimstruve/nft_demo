from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network, config
import pytest


def test_can_create_advanced_collectible():
    random_number = 777
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    # Act
    advanced_collectible, tx = deploy_and_create()
    requestId = tx.events["requestCollectible"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    # test if the account holder is the owner of the collectible
    assert advanced_collectible.ownerOf(0) == get_account()
    # test if the tokenCounter has been increased from 0 to 1
    assert advanced_collectible.tokenCounter() == 1
    # test if the breed is 0, since 777 % 3 = 0
    assert (
        advanced_collectible.tokenIdToBreed(advanced_collectible.tokenCounter() - 1)
        == random_number % 3
    )
