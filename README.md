About this APP: 

Comprehensive Search Capabilities:
    The application provides users with robust search functionality, allowing them to explore historical data by entering a query-to-question answer dataset having around 10K entries. This powerful feature facilitates efficient data retrieval, enabling users to pinpoint relevant information swiftly.

Keyword, Semantic, and Hybrid Search:
    Users can harness the power of keyword, semantic, and hybrid searches to refine their queries. This multi-faceted search approach ensures a nuanced exploration of the machine failures data, enhancing the precision of results.

Intuitive Presentation in a Tabular Format:
    Upon successful matching of the user's query with the data stored in the database, the application presents the results in a table format. The results are ordered by the highest similarity, providing users with a clear and organized overview of relevant information.

State-of-the-Art SBERT Model:
    To accomplish advanced text embeddings, we have implemented the cutting-edge Sentence-BERT (SBERT) model. This state-of-the-art model enables the conversion of textual data into a structured format, facilitating efficient comparison and analysis.

Open Source Vector Database:
    We have adopted an open-source vector database to store the embedded data securely. This ensures scalability, flexibility, and accessibility of the stored information.

Python-Powered Front-End Application:
    Our front-end application is developed using Python, harnessing the language's versatility and ease of use. The user-friendly interface ensures a seamless experience, allowing users to interact with the application effortlessly. ''')

How to Install:
Prerequisites:
- Install docker desktop (to install the weaviate vector database later in your local machine)

Installation:
1. clone the repo:
   https://github.com/rickystanley76/weaviate-multilingual-hybrid-search.git and then change to directory by using
   cd weaviate-multilingual-hybrid-search
2. Install required libraries:
   pip install -r requirements.txt
3. Run docker compose to install the weaviate in local macihine:
   docker compose up -d
4. Importing the CSV data to the weaviate database:
   python import.py (it may take longer time as the CSV has 10k records, embedding those may take time, if needed you can delete some records and test)

  
