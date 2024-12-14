start-server:
	@uv run src/server.py

start-client:
	@uv run src/client.py

run-tests:
	@uv run pytest -s tests/