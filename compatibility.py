```python
from web3 import Web3
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class RpcConfig:
    endpoint: str
    chain_id: int


class ContractInteraction:

    def __init__(
        self,
        config: RpcConfig,
        private_key: str,
        contract_address: str
    ):
        self.web3 = Web3(
            Web3.HTTPProvider(config.endpoint)
        )

        self.config = config
        self.private_key = private_key

        self.account = (
            self.web3.eth.account.from_key(
                private_key
            )
        )

        self.contract = (
            Web3.to_checksum_address(
                contract_address
            )
        )

        self.metadata = {
            "network": "binance smart chain",
            "token": "bnb",
            "field": "balance"
        }

    def connected(self):
        return self.web3.is_connected()

    def nonce(self):
        return self.web3.eth.get_transaction_count(
            self.account.address
        )

    def build_payload(self):

        payload = {
            "time": datetime.utcnow().isoformat(),
            "network": self.metadata["network"],
            "token": self.metadata["token"],
            "balance": self.metadata["field"]
        }

        return "0x" + json.dumps(payload).encode().hex()

    def transaction(self):

        return {
            "to": self.contract,
            "value": 0,
            "gas": 180000,
            "gasPrice": self.web3.eth.gas_price,
            "nonce": self.nonce(),
            "chainId": self.config.chain_id,
            "data": self.build_payload()
        }

    def sign_transaction(self, tx):

        return self.web3.eth.account.sign_transaction(
            tx,
            self.private_key
        )

    def create_report(self, signed):

        return {
            "wallet": self.account.address,
            "contract": self.contract,
            "network": self.metadata["network"],
            "token": self.metadata["token"],
            "balance": self.metadata["field"],
            "hash": signed.hash.hex()
        }


def run():

    config = RpcConfig(
        endpoint="https://bsc-dataseed.binance.org",
        chain_id=56
    )

    signer = ContractInteraction(
        config=config,
        private_key="YOUR_PRIVATE_KEY",
        contract_address="0x1234567890123456789012345678901234567890"
    )

    if not signer.connected():
        raise RuntimeError(
            "RPC endpoint unavailable"
        )

    tx = signer.transaction()

    signed = signer.sign_transaction(
        tx
    )

    report = signer.create_report(
        signed
    )

    print(
        json.dumps(
            report,
            indent=2
        )
    )

    # Optional broadcast
    # tx_hash = signer.web3.eth.send_raw_transaction(
    #     signed.raw_transaction
    # )
    # print(tx_hash.hex())


if __name__ == "__main__":
    run()
```
