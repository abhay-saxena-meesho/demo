import hashlib
import json
from time import time
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")
    def get_latest_block(self):
        return self.chain[-1]
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
def run_blockchain_demo():
    print("--- SIMPLE BLOCKCHAIN DEMO ---")
    my_coin = Blockchain()
    print("1. Mining block 1 with data: {amount: 4}...")
    my_coin.add_block(Block(1, time(), {"amount": 4}, ""))
    print("2. Mining block 2 with data: {amount: 10}...")
    my_coin.add_block(Block(2, time(), {"amount": 10}, ""))
    print(f"3. Chain validity check: {my_coin.is_chain_valid()}")
    print("4. Tampering with Block 1 data...")
    my_coin.chain[1].data = {"amount": 1000}
    print(f"5. Chain validity after tamper: {my_coin.is_chain_valid()}")
    print("\n--- FINAL CHAIN DATA ---")
    for block in my_coin.chain:
        print(f"Index: {block.index} | Hash: {block.hash[:10]}... | Data: {block.data}")
if __name__ == "__main__":
    run_blockchain_demo()
