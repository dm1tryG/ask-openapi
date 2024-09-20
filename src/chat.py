from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from settings import settings

def chat_with_model(user_input: str):
    embeddings = OpenAIEmbeddings(model=settings.OPENAI_API_EMBEDDINGS_MODEL)
    llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model=settings.OPEN_API_MODEL)
    chroma_db = Chroma(
        persist_directory="data",
        embedding_function=embeddings,
        collection_name="spec",
    )
    retriever = chroma_db.as_retriever()

    prompt = PromptTemplate.from_template(
        """
        System: You are an assistant that converts OpenAPI JSON specs into neatly structured, human-readable text with summary, description, tags, produces, responses, parameters, method, and curl examples.

        Example of OpenAPI spec chunk:
        ***GET /dogs***
        {{"responses": {{"200": {{"description": "Success"}}, "400": {{"description": "Bad Request"}}, "404": {{"description": "Not Found"}}, "500": {{"description": "Internal Server Error"}}}}, 
        "parameters": [
            {{"in": "query", "name": "breed", "required": false, "type": "string", "description": "<b>Filter</b>. Filter the list of dogs by breed."}}, 
            {{"in": "query", "name": "age", "required": false, "type": "integer", "description": "<b>Filter</b>. Filter the list of dogs by age."}}, 
            {{"in": "query", "name": "size", "required": false, "type": "string", "enum": ["small", "medium", "large"], "description": "<b>Filter</b>. Filter dogs by size."}},
            {{"in": "header", "name": "authorization", "required": true, "type": "string", "description": "Bearer token for authorization."}}
        ], 
        "tags": ["Dogs"], 
        "summary": "Retrieve a list of dogs", 
        "description": "Get a filtered list of dogs based on query parameters such as breed, age, or size", 
        "produces": ["application/json"], 
        "method": "get", 
        "path": "/api/v1/dogs"}}

        Result:
        ### GET /dogs

        **Summary**: Retrieve a list of dogs

        **Description**: Get a filtered list of dogs based on query parameters such as breed, age, or size.

        **Tags**: Dogs

        **Produces**: application/json

        **Responses**:
        - **200**: Success
        - **400**: Bad Request
        - **404**: Not Found
        - **500**: Internal Server Error

        **Parameters**:
        - **Query**:
        - `breed` (string, optional): Filter by dog breed.
        - `age` (integer, optional): Filter by dog age.
        - `size` (string, optional): Filter by dog size (small, medium, large).
        - **Header**:
        - `authorization` (string, required): Bearer token for authorization

        **Method**: GET

        **Curl Example**:
        ```sh
        curl -X GET "https://api.example.com/dogs?breed=labrador&size=medium" -H "Authorization: Bearer <your_token>"
        ```

        Now, format the following OpenAPI spec:

        {context}

        Curl Example:

        {question}
        """
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(user_input)