# Import necessary modules and classes
import joblib
from config import DefaultConfig
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load app configuration
CONFIG = DefaultConfig()

# Extract OpenAI API key from the configuration
OPENAI_API_KEY = CONFIG.OPENAI_API_KEY
# Raise an exception if the OpenAI API key is not set
if OPENAI_API_KEY is None:
    raise Exception('OPENAI_API_KEY environment variable not set')

# Load the FAISS vector database from a specified path
docsearch = joblib.load(CONFIG.VECTOR_DATABASE_JOBLIB_PATH)
# Create a retriever from the vector database
vectorstore_retriever = docsearch.as_retriever()

# Create an instance of ChatOpenAI with specified model and temperature
llm = ChatOpenAI(model=CONFIG.OPENAI_MODEL, temperature=0.3, openai_api_key=OPENAI_API_KEY)

# Define a template for the chat prompts
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Answer as detailed as possible.
Say "Thanks for asking!" at the end of the answer if the prompt is question.
{context}
Question: {question}
Helpful Answer:"""

# Create a ChatPromptTemplate from the defined template
prompt = ChatPromptTemplate.from_template(template)

# Define a chain of operations to be performed on the input query
chain = (
    {
        "context": vectorstore_retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Define a function to ask the bot a question
def ask_polar_cape_bot(query):
    # Invoke the chain of operations on the input query and return the result
    return chain.invoke(query).strip()

# Example usage
if __name__ == "__main__":
    question = "What is the capital of France?"
    answer = ask_polar_cape_bot(question)
    print(answer)
