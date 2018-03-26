import sys
from miner import Miner
from blockChain import BlockChain
from core import *
from flask import Flask, jsonify, request
import requests
from block import Block
class NetworkNode:
	
	def __init__(self,id,address,max_len,neighbours=[]):
		self.id = id
		self.address = address
		self.max_len = max_len
		self.miner = Miner(BlockChain(100),max_len,self)
		self.nodes = set()
		self.nodes.add(self.address)
		self.nodes.update(neighbours)

	@property
	def chain(self):
		return self.miner.chain

	def new_neighbour(self,node):
		print("new node registered:%s" % node.id)
		self.nodes.add(node)

	def notify_neighbours(self):
		for address in self.nodes:
			if address is self.address:
				continue
			data = json.dumps({"proof":self.chain.last_block.proof,"length":self.chain.length})
			requests.post("%s/notify" % address,data = data,headers= {'Content-Type': 'application/json', 'Accept': 'application/json'})

	#todo:try to sync the latest block chain from other node
	def sync(self):
		pass	 

	def empty_chain(self):
		return BlockChain(0)
		
	@property
	def all_nodes(self):
		return map(lambda n: n, self.nodes)

	@property
	def chain(self):
		return self.miner.chain

	def join_cluster(self,seed):
		if seed is not None:
			url = "%s/nodes" % seed
			nodes_address = requests.get(url).json()
			self.nodes.update(nodes_address)

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def start():
	return node.chain.status()

@app.route("/nodes",methods=['GET'])
def nodes():
	return json.dumps(node.all_nodes)

@app.route("/notify",methods=['POST'])
def notify():
	json = request.json
	proof = json['proof']
	length = json['length']
	if length < node.chain.length:
		print("invalid length")
	elif length > node.chain.length + 1:
		node.sync()
	else: 
		if valid_proof(node.chain.last_proof,proof):
			node.chain.new_block(Block(node.chain.last_proof,proof))
			node.sync()
	return ""

@app.route("/mine",methods=['GET'])
def mine():
	node.miner.mine()
	return node.chain.status()

if __name__ == "__main__":
	id = sys.argv[1]
	max_len = 10
	address = sys.argv[2]
	port = int(sys.argv[3])
	seed = None
	nodes_address = []
	if len(sys.argv) > 4:
		seed = sys.argv[4]
	node = NetworkNode(id,"%s:%s" % (address,port),max_len,nodes_address)
	node.join_cluster(seed)
	#node.miner.start()
	app.run(host='0.0.0.0', port=port)

    