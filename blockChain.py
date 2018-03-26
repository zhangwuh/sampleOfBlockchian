import json
from block import Block
from core import *

class BlockChain(object):

	def __init__(self,genesis):
		self.blocks = []
		self.blocks.append(Block(prevProof=0,proof=genesis))

	def new_block(self,block):
		if valid_proof(self.last_proof,block.proof):
			self.blocks.append(block)
		else:
			raise Exception("Don't lie to me!")

	def new_transaction(self):
		pass

	def is_empty(self):
		return self.blocks[0].proof == 0

	@property
	def last_proof(self):
		return self.last_block.proof

	@property
	def last_block(self):
		return self.blocks[-1]

	@property
	def length(self):
		return len(self.blocks)

	def status(self):
		return json.dumps([obj.__dict__ for obj in self.blocks])


