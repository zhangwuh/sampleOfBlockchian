import time

class Block:

	def __init__(self,prevProof,proof):
		self.prevProof = prevProof
		self.proof = proof
		self.timestamp = int(time.time())
		self.transactions = []
		#self.nonce = ""

	def __str__(self):
		return self.proof

