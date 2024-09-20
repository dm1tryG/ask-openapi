import json
import requests
from langchain.docstore.document import Document


def get_openapi_spec(url: str):
    """
    Fetches the OpenAPI specification from the given URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_openapi_spec_paths(specification: dict):
    paths = []

    for p in specification["paths"]:
        for m in specification["paths"][p]:
            path = specification["paths"][p][m]
            path["method"] = m
            path["path"] = p
            path["components"] = []
            paths.append(path)

    # 2.0 OpenAPI doesnt have components
    if "components" in specification:
        for s in specification["components"]["schemas"]:
            for pi in range(len(paths)):
                if s in json.dumps(paths[pi]):
                    schema = specification["components"]["schemas"][s]
                    schema["id"] = s
                    paths[pi]["components"].append(schema)

    return paths


def dump_openapi_spec_to_chroma_docs(paths):
    dumped_paths = []
    for p in paths:
        dumped_paths.append(
            Document(page_content=json.dumps(p), metadata={"source": "local"})
        )
    return dumped_paths
