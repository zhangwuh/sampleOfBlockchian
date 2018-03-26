import hashlib
import time
import json

COMPLEXITY = 4

def hash(text):
	return hashlib.sha256(text).hexdigest()

def hash_block(block):
	asText = json.dumps(block.__dict__,sort_keys=True).encode("utf-8")
	return hash(asText)

def proof_of_work(last_proof,timeout):
	proof = 0
	start_at = time.time()
	while valid_proof(last_proof,proof) is False:
		if time.time() - start_at > timeout:
			raise Exception("timeout")		
		proof += 1
	return proof

def valid_proof(last_proof,proof):
	guess = "%s%s" % (last_proof,proof)
	return hash(guess)[:4] == COMPLEXITY * "0"

def register_node(node):
	nodes.add(node)

def valid(chain):
	last_block = chain.blocks[0]
	index = 1

	while index < chain.length:
		block = chain.blocks[index]
		if block.prevProof != last_block.proof:
			return False
		if not valid_proof(last_block.proof,block.proof):
			return False

		last_block = block
		index += 1

	return True

def broadcast():
	longest_chain = resolve_longest_chain()
	if longest_chain is not None:
		for node in nodes:
			node.chain = longest_chain  
			print("update chain at %s" % node.id)
			