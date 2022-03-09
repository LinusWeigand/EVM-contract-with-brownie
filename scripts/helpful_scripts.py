from brownie import network, config, accounts, MockV3Aggregator


def get_account():
    if network.show_active():
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

