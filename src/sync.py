import typer
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from openapi_helpers import (
    dump_openapi_spec_to_chroma_docs,
    get_openapi_spec_paths,
    get_openapi_spec,
)

app = typer.Typer()

@app.command()
def help():
    print("Welcome to Ask OpenAPI")

@app.command()
def sync(url: str):
    specification = get_openapi_spec(url)
    paths = get_openapi_spec_paths(specification)
    dumped_paths = dump_openapi_spec_to_chroma_docs(paths)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002"
    )
    Chroma.from_documents(
        documents=dumped_paths,
        embedding=embeddings,
        persist_directory="data",
        collection_name="lc_chroma_demo",
    )


if __name__ == "__main__":
    app()
