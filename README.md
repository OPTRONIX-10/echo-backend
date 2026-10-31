# Echo Backend

Echo Backend is a Python 3.12+ FastAPI service for home-service workflows. It
provides:

- Structured service-detail extraction through Gemini's OpenAI-compatible API.
- Nearby service-provider search through Google Places Text Search.
- Outbound agent calls and execution lookup through Bolna.
- WebSocket connections for execution-status updates.
- A webhook endpoint intended to forward Bolna execution status to connected
  WebSocket clients.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- API credentials for the integrations you plan to use

## Installation

```bash
uv sync
```

Create a `.env` file in the project root. Do not commit this file or real
credentials:

```dotenv
GOOGLE_PLACES_API_KEY=your-google-places-key
GEMINI_API_KEY=your-gemini-key
BOLNA_API_KEY=your-bolna-key
```

The application loads environment variables with `python-dotenv`. Missing
credentials are reported when the corresponding integration is called.

## Running locally

Start the development server with:

```bash
uv run fastapi dev src/echo_backend/main.py
```

The API is available at `http://127.0.0.1:8000`. FastAPI's interactive
documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API endpoints

### Health check

```http
GET /health/
```

Response:

```json
{"status": "ok"}
```

### Extract service details

```http
GET /llm/response?message=My%20kitchen%20sink%20is%20leaking
```

The response contains the extracted `service_description` and
`service_category`.

### Search nearby service providers

```http
POST /places/search?text_query=plumber&latitude=12.9716&longitude=77.5946
```

The endpoint queries Google Places with a 15 km distance bias and returns up to
five providers containing their ID, name, address, phone number, and
coordinates.

### Initiate a Bolna agent call

```http
POST /bolna_agent/call?agent_id=agent-id&recipient_phone_number=%2B15551234567
Content-Type: application/json
```

Request body:

```json
{
  "customer_name": "Asha",
  "customer_phone_number": "+15551234567",
  "service_type": "plumbing",
  "customer_location": "Bengaluru",
  "service_description": "Leaking kitchen sink",
  "provider_bussiness_name": "Example Services"
}
```

The response contains the Bolna message, status, and `execution_id`.

### Fetch a Bolna execution

```http
GET /bolna_agent/execution/{execution_id}
```

The response maps execution status, transcript, summary, extracted data, and
recording URL into the execution schema.

### Receive an execution webhook

```http
POST /webhook/
Content-Type: application/json
```

Request body:

```json
{
  "id": "execution-id",
  "status": "completed"
}
```

The endpoint validates that both `id` and `status` are present and returns:

```json
{"message": "Webhook received successfully"}
```

### Connect to execution updates

```text
ws://127.0.0.1:8000/websocket/{execution_id}
```

The server accepts the connection and keeps it open while receiving text
messages. The connection manager stores one WebSocket per execution ID.

## Project structure

```text
src/echo_backend/
├── main.py                         # FastAPI application and router setup
├── core/
│   ├── lifespan.py                 # Shared AsyncClient lifecycle
│   └── websocket.py                # WebSocket connection manager
├── routes/                         # HTTP and WebSocket endpoints
├── services/                       # External API and LLM integrations
└── schemas/                        # Pydantic request/response models
```

## Runtime behavior

The application creates one shared `httpx.AsyncClient` during FastAPI startup
with a 30-second timeout and closes it during shutdown. External HTTP calls
reuse this client. The LLM integration currently uses the synchronous
`OpenAI` client from an async route, so high-concurrency deployments should
move that call to an async client or a worker before production use.

## Current integration notes

- The Bolna service reads `BOLNA_API_KEY`, while its missing-key error message
  still refers to `BOLNA_API_TOKEN`. Use `BOLNA_API_KEY` as the configured
  variable.
- The call route currently accepts `agent_id`, `recipient_phone_number`, and
  the JSON user-data object. A `from_phone_number` parameter is not currently
  implemented.
- The Bolna `Authorization` header is currently a placeholder in the service
  implementation and must be wired to the configured credential before
  authenticated Bolna requests can work.
- The webhook and WebSocket manager are intended to deliver execution updates,
  but their current argument ordering does not match
  `ConnectionManager.broadcast(message, execution_id)`. This should be fixed
  before relying on webhook-driven live updates.
- There are currently no automated tests in the repository. Validate changes
  with the OpenAPI docs and integration requests against configured services.

## Development commands

Install or update the locked dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run fastapi dev src/echo_backend/main.py
```

The project is configured through `pyproject.toml` and `uv.lock`; keep the lock
file in sync when dependency declarations change.