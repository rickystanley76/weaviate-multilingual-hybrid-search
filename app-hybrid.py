import streamlit as st
import pandas as pd
import weaviate
#from sentence_transformers import SentenceTransformer
from PIL import Image

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")



def get_hybrid_results(query,class_name, properties, limit):

    
    if len(query) == 0:
        # Perform a standard search if query is empty
        graphql_query = f"""
        {{
            Get {{
                {class_name}(
                    limit: {limit}
                ) {{
                    { ' '.join(properties) }

                }}
            }}
        }}
        """
    else:
        # Perform a hybrid search if query is provided
        graphql_query = f"""
        {{
            Get {{
                {class_name}(
                    hybrid: {{
                        query: "{query}",
                        alpha: 0.5
                    }},
                    limit: {limit}
                ) {{
                    { ' '.join(properties) }
                    _additional {{
                        score
                    }}
                }}
            }}
        }}
        """
    
    # Execute the query
    try:
        response = client.query.raw(graphql_query)
        data = response.get('data', {}).get('Get', {}).get(class_name, [])
        
        # Debug: Print the raw response
        #st.write("Raw response from Weaviate:")
        #st.write(response)
        
        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(data)
        if '_additional' in df.columns:
            # Calculate similarity only if 'certainty' is present and is a valid float
            df['Similarity'] = df['_additional'].apply(
                lambda x: round(float(x.get('score', 0)) * 10000, 2) if x.get('score') and is_valid_float(x.get('score')) else None
            )
            df.drop('_additional', axis=1, inplace=True)
        return df
    except Exception as err:
        st.error(f"An error occurred: {err}")
        return pd.DataFrame()  # Return an empty DataFrame instead of []

# Helper function to check if a string can be converted to a valid float
def is_valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False    

        
# Streamlit App
st.set_page_config(page_title="Swedish QA Hybrid Search APP- Vector database in the backend", layout="wide", page_icon=":tractor:")


img = Image.open('smartsearchai.jpg')

# Create two columns
col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

# Display the image in the first column
with col1:
    st.image(img, width=150)

# Display the title in the second column
with col2:
    st.title("Multilingual Hybrid Search APP")
    st.subheader("Hybrid = Semantic + Keyword")
with st.expander("Information"):
    st.write('''Key Features:

    Comprehensive Search Capabilities:
    The application provides users with a robust search functionality, allowing them to explore historical data by entering a 'problem description.' This powerful feature facilitates efficient data retrieval, enabling users to pinpoint relevant information swiftly.

    Keyword, Semantic, and Hybrid Search:
    Users can harness the power of keyword, semantic, and hybrid searches to refine their queries. This multi-faceted search approach ensures a nuanced exploration of the machine failures data, enhancing the precision of results.

    Intuitive Presentation in a Tabular Format:
    Upon successful matching of the user's query with the data stored in the database, the application presents the results in a table format. The results are ordered by highest similarity, providing users with a clear and organized overview of relevant information.

    State-of-the-Art SBERT Model:
    To accomplish advanced text embeddings, we have implemented the cutting-edge Sentence-BERT (SBERT) model. This state-of-the-art model enables the conversion of textual data into a structured format, facilitating efficient comparison and analysis.

    Open Source Vector Database:
    We have adopted an open-source vector database to store the embedded data securely. This ensures scalability, flexibility, and accessibility of the stored information.

    Python-Powered Front-End Application:
    Our front-end application is developed using Python, harnessing the language's versatility and ease of use. The user-friendly interface ensures a seamless experience, allowing users to interact with the application effortlessly. ''')




# User input for the query
query = st.text_input("Enter your search query")

# Specify the class name and properties you want to retrieve
class_name = 'GeneralQa'
properties = ['question', 'answer']

# Slider for selecting the number of search result
limit = st.slider("Select the number of search results", min_value=1, max_value=20, value=5)

# Perform search and display results
    
if query:
    results_df = get_hybrid_results(query, class_name, properties, limit)
    if not results_df.empty:
        st.write("Search Results:")
        st.table(results_df)
    else:
        st.write("No results found.")


##### FOOTER #######################################
st.subheader("Developed By:")

st.write("Project:")
st.image("smartsearchai.jpg", width=200)
url = "https://www.smartsearchai.se/"
st.markdown("check out this [link](%s)" % url)

