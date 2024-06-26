#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# # Step 1:
# ### Create a "Record" Data Class
# 

# In[2]:


@dataclass 
class Record:
    sender :str
    receiver :str
    amount :float

# # Step 2:
# ### Modify the Existing Block Data Class to Store Record Data
# 

# In[3]:


@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0
    
    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()
    


# In[4]:


@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

# In[5]:


# Adds the cache decorator for Streamlit
# Adds the cache decorator for Streamlit
@st.cache_resource()
def setup():
    print("Initializing Chain")
    # Initialize the chain with a genesis block
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()


# # Step 3
# ###  Add Relevant User Inputs to the Streamlit Interface
# 

# In[6]:


# Delete the `input_data` variable from the Streamlit interface.

# Add an input area where you can get a value for `sender` from the user.
sender = st.text_input("Sender")

# Add an input area where you can get a value for `receiver` from the user.
receiver = st.text_input("Receiver") 

# Add an input area where you can get a value for `amount` from the user.
amount = st.number_input("Amount")   

# In[7]:


if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # @TODO
    # Update `new_block` so that `Block` consists of an attribute named `record`
    # which is set equal to a `Record` that contains the `sender`, `receiver`,
    # and `amount` values
    new_record = Record(
        sender=sender, 
        receiver=receiver, 
        amount=amount
    )
    
    new_block = Block(
        record= new_record,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

    

# In[8]:


st.markdown("## The PyChain Ledger")


pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())

# In[ ]:



