#0.017 eth
#170000000000000000 wei
from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrancefee():
    account = accounts[0]
    #lottery = Lottery.deploy("the argument here is required by the constructor", "from": account })
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"], {"from":account}
    )
    #assert lottery.getEntranceFee() > Web3.toWei(0.016,"ether")
    #assert lottery.getEntranceFee() < Web3.toWei(0.019,"ether")