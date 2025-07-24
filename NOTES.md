# NOTES.md

## AI Usage
-Tool Used: ChatGPT 
- Purpose: Assisted with environment setup, debugging, endpoint implementation, test writing, and code explanations.
- AI-generated code:
  -Helped me in designing and implement the /api/shorten, redirect, and analytics endpoints, including adding clear error handling for each.
  - Guidance on fixing import and port issues.
  - Suggestions for testing with curl and Postman.
  - Test suite for all core and edge cases.
- Modifications:
  - All AI-generated code was reviewed and tested before use.
  - Minor adjustments made for environment compatibility and error handling.

## Implementation Notes
- Endpoints implemented:
  - `POST /api/shorten` for URL shortening
  - `GET /<short_code>` for redirection
  - `GET /api/stats/<short_code>` for analytics
-In-memory storage is used for URL mappings and analytics.
- Testing:
  - Used curl and Postman for manual endpoint testing.
  - pytest used for automated test validation.
  - To run tests:From the project root, use `PYTHONPATH=. pytest`
  - All 6 tests pass, covering health, shorten, redirect, analytics, invalid input, and not found cases.
-Common issues encountered:
  - Port 5000 conflict with AirPlay/Control Center
  - Python import errors when running scripts directly
  - Solution: Always use `python -m flask --app app.main run --port 5050` from project root, and `PYTHONPATH=. pytest` for tests

## What remains
- (Optional) Refactor for code clarity or add more edge case tests
- make the short code generation more robust
- add a /api/health endpoint that returns more detailed status (memory usage, number of URLs, etc.)
-Add a /api/shorten GET endpoint that lists all current short codes.
