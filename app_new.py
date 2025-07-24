from saksin_vect2 import SaksinConfig, SaksinRetriever

# Step 1: Configure your API settings
config = SaksinConfig(
    api_key="264dc103f55cd2fdb0226f75038f1831afc19602553e954f39f1b155cdfc3aaa"
    
)

# Step 2: Create the retriever with config
retriever = SaksinRetriever(config=config)

# Step 3: Query Saksin vector DB
response = retriever.query("What is Sākṣin platform?")
print(response)
