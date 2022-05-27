from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network, config
import pytest
import time


def test_can_create_advanced_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing!")
    # Act
    advanced_collectible, tx = deploy_and_create()
    time.sleep(360)
    # Assert
    # test if the account holder is the owner of the collectible
    assert advanced_collectible.ownerOf(0) == get_account()
    # test if the tokenCounter has been increased from 0 to 1
    assert advanced_collectible.tokenCounter() == 1
