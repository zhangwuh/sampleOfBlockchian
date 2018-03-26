import time
from block import Block
from core import *
import sys, traceback
import threading

class Miner(threading.Thread):
	def __init__(self,chain,max_len,node):
		super(Miner,self).__init__()
		self.node = node
		self.timeout_seconds = 100
		self.chain = chain
		self.max_len = max_len

	def run(self):
		i = 0
		while i < self.max_len:
			try:
				self.mine()
				i += 1	
			except Exception as e:
				traceback.print_exc(file=sys.stdout)
				return

	def mine(self):
		proof = proof_of_work(self.chain.last_proof,self.timeout_seconds)
		print("new proof found:%d by %s" % (proof,self.node.id))
		self.chain.new_block(Block(self.chain.last_proof,proof))
		print("new block appended,lastest full chain is:%s at node [%s],length is %d" % (self.chain.status(),self.node.id,self.chain.length))
		self.node.notify_neighbours()
		return self.chain.last_proof
		