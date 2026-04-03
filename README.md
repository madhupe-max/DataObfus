# DataObfus

Simple Python API for PII and MNPI-style data obfuscation.

## Features

- `POST /obfuscate` endpoint to mask common sensitive values
- Detects and obfuscates:
	- Email addresses
	- Phone numbers
	- SSNs
	- Credit card-like numbers
- `GET /health` endpoint for basic service checks

## Quick Start

1. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn app:app --reload
```

4. Open interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Example

Request:

```bash
curl -X POST "http://127.0.0.1:8000/obfuscate" \
	-H "Content-Type: application/json" \
	-d '{"text":"Jane Doe email jane@example.com and card 4111 1111 1111 1111"}'
```

Response (example):

```json
{
	"obfuscated_text": "Jane Doe email [EMAIL] and card [CREDIT_CARD]",
	"replacements": {
		"email": 1,
		"phone": 0,
		"ssn": 0,
		"credit_card": 1
	}
}
```
