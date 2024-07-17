from datetime import datetime
import hashlib
from flask import Flask , jsonify
import json

class Blockchain:

    

    def __init__(self):
        self.chain = []
        self.create_block(proof=1,previous_hash=0)

    def create_block(self,proof,previous_hash):
        block = {'index':len(self.chain)+1,"time":datetime.now().isoformat(),
                'proof':proof,
                'previous_hash':previous_hash}
        self.chain.append(block)
        return block

    def get_previous_hash(self):
        return self.chain[-1]
        
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof = False
        while check_proof!=True:
            hash_operatoion = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operatoion[0:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            if self.hash(previous_block) != chain[block_index]['previous_block']:
                return False
            previous_proof = previous_block['proof']
            proof = chain[block_index]['proof']
            hash_operatoion = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
                
            block_index += 1
            previous_block = chain[block_index]
            
        return True

app = Flask(__name__)

blockchain = Blockchain()



@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_hash()
    prevoius_work = previous_block['proof']
    proof = blockchain.proof_of_work(prevoius_work)
    block = blockchain.create_block(proof,blockchain.hash(previous_block))
    response = {'message':'Congragulations your block got created.'
                ,'index':block['index'],"time":block['time'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response) , 200 


@app.route('/Get_chain', methods = ['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response) , 200

app.run(host= '0.0.0.0',port= 5000)

