import hashlib
import json
from datetime import datetime
import os

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.ledger_file = 'data/ledger.json'
        self._load_chain()

    def _load_chain(self):
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, 'r') as f:
                chain_data = json.load(f)
                self.chain = [Block(
                    index=block['index'],
                    timestamp=datetime.fromisoformat(block['timestamp']),
                    data=block['data'],
                    previous_hash=block['previous_hash']
                ) for block in chain_data]
        else:
            # Create genesis block
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, datetime.now(), "Genesis Block", "0")
        self.chain.append(genesis_block)
        self._save_chain()

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        self._save_chain()
        return new_block

    def _save_chain(self):
        chain_data = [{
            "index": block.index,
            "timestamp": block.timestamp.isoformat(),
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        } for block in self.chain]

        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        with open(self.ledger_file, 'w') as f:
            json.dump(chain_data, f, indent=4)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def log_shipment_update(self, shipment_id, update_type, details):
        log_entry = {
            "shipment_id": shipment_id,
            "update_type": update_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.add_block(log_entry)
        return log_entry 