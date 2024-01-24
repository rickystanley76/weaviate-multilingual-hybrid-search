import weaviate
from weaviate import Config
import weaviate.classes as wvc
import os
import pandas as pd
import numpy as np

# Starting up the weaviate client
client = weaviate.Client("http://localhost:8080")

# Deleting any previously existing "MachineFailures" class
print("delete previous")
client.schema.delete_class("GeneralQa")

# Creating a new class with the defined schema
#Here "vectorizer": "text2vec-transformers" it is using: the default transformer model used was `bert-base-uncased`.
#If you need to use a specific transformer model, such as `paraphrase-multilingual-mpnet-base-v2`, 
#and Weaviate's default model does not meet your requirements, you may need to vectorize your text data outside of Weaviate using the Sentence Transformers library, 
#as I described in the previous answer, and then store the resulting vectors in Weaviate manually.

# Created all the properties with 'text' so it enables with semantic and keyword search(Hybrid search)
# Creating a new class with the defined schema
try:
    client.schema.create_class(
        {
            "class": "GeneralQa",
            "description": "A class to store general QA records in swedish",
            "vectorIndexConfig": {
                "distance" : "cosine"
                },
            "vectorIndexType": "hnsw",
            "vectorizer": "text2vec-transformers",
            "properties": [
                {
                    "name": "question",
                    "dataType": ["text"],
                },
                {
                    "name": "answer",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-transformers": {
                        "skip": True  # Skip vectorization for this property
                        }
                    }
                },     
            ],

        }
    )
except weaviate.SchemaValidationException as e:
    print(f"Schema validation error: {e}")
except weaviate.UnexpectedStatusCodeException as e:
    print(f"Unexpected status code: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


# Checking is the collection is created successfully or not
print("create new")
print(client.collection.exists("GeneralQa"))

# Importing the data using pandas
data = pd.read_csv('./data/general-qa-swedish_10k.csv', index_col=0)

# Getting the collection "DiseaseSearch" that was created earlier
general_qa_data = client.collection.get("GeneralQa")


# Iterating through the dataset and storing it all in an array to be inserted later
objects_to_add = [
    {
        "question": row["question"],
        "answer": row["answer"],
    }
    for index, row in data.iterrows()
]

# Define a function to replace non-compliant float values
def replace_non_compliant_values(value):
    if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
        return None  # Replace with None or an appropriate placeholder
    return value
    
# Inserting the data into the class
for obj in objects_to_add:
    # Replace non-compliant float values in the object
    sanitized_obj = {k: replace_non_compliant_values(v) for k, v in obj.items()}
    client.data_object.create(sanitized_obj, "GeneralQa")

# Fetching any 5 objects from the class and printing the response
query_string = """
{
  Get {
    GeneralQa(limit: 5) {
      question
      answer
    }
  }
}
"""
response = client.query.raw(query_string)
print("Output")
print(response)