# Ask OpenAPI

RAG based application to read large OpenAPI Specs

## Overview
Ask OpenAPI is a web application that allows users to interact with OpenAPI specifications and convert them into human-readable formats.

## Requirements
- Docker
- Docker Compose

## Installation
1. Create a `.env` file based on the `example.env`:
   - Copy `example.env` to `.env`:
     ```bash
     cp example.env .env
     ```
   - Edit the `.env` file to set your OpenAI API key:
     ```plaintext
     OPENAI_API_KEY=<your_openai_api_key>
     OPENAI_API_EMBEDDINGS_MODEL=text-embedding-ada-002
     OPEN_API_MODEL=gpt-4o
     ```

2. Build and start the application:
   ```bash
   make chat
   ```

## Commands
- `make sync url=<your_openapi_url>`: Sync OpenAPI specifications from a URL.
- `make chat`: Start the chat interface.
- `make clean`: Clean up generated data.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.