from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery ,network, config
import time

# ______________________===== 8:20:10

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from":account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("deployed Lottery!")
    return lottery

def start_lottery():
    account =get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from":account})
    starting_tx.wait(1)
    #Brownie sometimes get's a little confused if you don't wait for the last transaction to go through
    print("The lottery has officialy begun!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx= lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!!")

def end_lottery():
    account = get_account()
    lottery= Lottery[-1]
    #fund contract with Link
    tx= fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from":account})
    ending_transaction.wait(1)
    time.sleep(60)
    #waiting for the chainlink node to respond with the fulfillRandomness function, typically within a few blocks(we will wait 60 secs)
    print(f"{lottery.recentWinner()}is the new winner!")


   


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()