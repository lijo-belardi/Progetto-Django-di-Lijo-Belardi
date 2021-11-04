from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/8ab786d530c34a56a947f5fd90a2e99a'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address: {address}\nYour key: {privateKey}")