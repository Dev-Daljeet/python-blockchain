import hashlib
import time

# Represent the block in the blockchain
class Block:

    def __init__(self, index, proof_num, prev_hash, data, timestamp=None):
        self.index = index
        self.proof_num = proof_num
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    # Calculate the cryptographic hash of a block
    @property
    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_num, self.prev_hash, self.data, self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()
    
    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_num, self.prev_hash, self.data, self.timestamp)

# Represent the blockchain which contains blocks
class BlockChain:

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()

    # Construct the intial block of the blockchain
    def construct_genesis(self):
        self.construct_block(proof_num = 0, prev_hash = 0)
    
    # Construct a new block and adds it to the chain
    def construct_block(self, proof_num, prev_hash):
        block = Block(index = len(self.chain), proof_num = proof_num, prev_hash = prev_hash, data = self.current_data)
        self.current_data = []
        self.chain.append(block)
        return block

    # Check whether the blockchain is valid
    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False

        elif prev_block.calculate_hash != block.prev_hash:
            return False
        
        elif not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False
        
        elif block.timestamp <= prev_block.timestamp:
            return False
            
        return True

     # Add a new transaction to the data of the transactions
    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    # Protect the blockchain from attack
    @staticmethod
    def proof_of_work(last_proof):
        '''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
         f is the previous f'
         f' is the new proof
        '''
        proof_num = 0
        while BlockChain.verifying_proof(proof_num, last_proof) is False:
            proof_num += 1
        
        return proof_num

    # Verify the proof: does hash(last_proof, proof) contain 4 leading zeroes?
    @staticmethod
    def verifying_proof(last_proof, proof):
         guess = f'{last_proof}{proof}'.encode()
         guess_hash = hashlib.sha256(guess).hexdigest()
         return guess_hash[:4] == "0000"

    # Return the last block in the chain
    @property
    def latest_block(self):
        return self.chain[-1]

    def block_mining(self, details_miner):
        self.new_data( sender = "0", #it implies that this node has created a new block
        recipient = details_miner,
        quantity = 1 #creating a new block (or identifying the proof number) is awarded with 1
        )

        last_block = self.latest_block

        last_proof_num = last_block.proof_num
        proof_num = self.proof_of_work(last_proof_num)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_num, last_hash)

        return vars(block)
    
    def create_node(self, address):
        self.nodes.add(address)
        return True
    
    # Obtain the block object from block data
    @staticmethod
    def obtain_block_object(block_data):
        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])

#Execution
blockchain = BlockChain()

username = input("Enter your name: ")
name_of_cryptocurrency = input("Enter the name for your cryptocurrency: ")
print("***Mining {} about to start***".format(name_of_cryptocurrency))
print(blockchain.chain)
    
last_block = blockchain.latest_block
last_proof_num = last_block.proof_num
proof_num = blockchain.proof_of_work(last_proof_num)
    
blockchain.new_data(
    sender="0",  #it implies that this node has created a new block
    recipient= username,  #let's send user some coins!
    quantity=1  #creating a new block (or identifying the proof number) is awarded with 1)
)

last_hash = last_block.calculate_hash
block = blockchain.construct_block(proof_num, last_hash)

print("***Mining {} has been successful***".format(name_of_cryptocurrency))
print(blockchain.chain)