import hashlib
import json
from datetime import datetime
import os

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        if isinstance(data, str):
            self.data = {
                'shipment_id': '0',
                'update_type': 'unknown',
                'details': {'message': data}
            }
        elif isinstance(data, dict) and 'data' in data:
            # Handle case where data is nested in a 'data' field
            self.data = data['data']
        else:
            # Ensure data has the required structure
            self.data = {
                'shipment_id': str(data.get('shipment_id', '0')),
                'update_type': str(data.get('update_type', 'unknown')),
                'details': data.get('details', {'message': 'No details provided'})
            }
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
        try:
            if os.path.exists(self.ledger_file):
                with open(self.ledger_file, 'r') as f:
                    chain_data = json.load(f)
                    self.chain = []
                    for block in chain_data:
                        new_block = Block(
                            index=block['index'],
                            timestamp=datetime.fromisoformat(block['timestamp']),
                            data=block['data'],
                            previous_hash=block['previous_hash']
                        )
                        self.chain.append(new_block)
            else:
                self.create_genesis_block()
        except Exception as e:
            print(f"Error loading chain: {e}")
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_data = {
            'shipment_id': '0',
            'update_type': 'genesis',
            'details': {'message': 'Genesis Block'}
        }
        genesis_block = Block(0, datetime.now(), genesis_data, "0")
        self.chain = [genesis_block]
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
        try:
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
        except Exception as e:
            print(f"Error saving chain: {e}")

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
            "shipment_id": str(shipment_id),
            "update_type": str(update_type),
            "details": details
        }
        return self.add_block(log_entry) 