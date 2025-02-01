.PHONY: start stop ps logs clean purge help

BLUE=\033[0;34m
GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m
UNDERLINE=\033[4m

help:
	@echo "Available commands:"
	@echo "  make start    - Start all services"
	@echo "  make stop     - Stop all services (preserves data)"
	@echo "  make ps       - Show running containers"
	@echo "  make logs     - Show logs"
	@echo "  make clean    - Stop and remove containers (preserves volumes)"
	@echo "  make purge    - Remove everything (containers, volumes, networks)"

start:
	@echo "Starting all services..."
	@docker compose -f .devcontainer/docker-compose.yaml -f docker-compose.kestra.yaml up -d
	@echo "\nServices running at:"
	@echo "${BLUE}${UNDERLINE}http://localhost:5432${NC} - PostgreSQL (ny_taxi)"
	@echo "${BLUE}${UNDERLINE}http://localhost:8088${NC} - PgAdmin"
	@echo "${BLUE}${UNDERLINE}http://localhost:8080${NC} - Kestra UI"
	@echo "${BLUE}${UNDERLINE}http://localhost:8081${NC} - Kestra API"

stop:
	@echo "Stopping all services..."
	@docker compose -f .devcontainer/docker-compose.yaml -f docker-compose.kestra.yaml down
	@echo "${GREEN}All services stopped successfully!${NC}"

ps:
	@docker compose -f .devcontainer/docker-compose.yaml -f docker-compose.kestra.yaml ps

logs:
	@docker compose -f .devcontainer/docker-compose.yaml -f docker-compose.kestra.yaml logs -f

clean: stop
	@echo "Removing containers..."
	@docker compose -f .devcontainer/docker-compose.yaml -f docker-compose.kestra.yaml rm -f
	@echo "${GREEN}All containers removed!${NC}"

purge:
	@echo "${RED}Warning: This will remove all containers, volumes, and networks${NC}"
	@read -p "Are you sure? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker compose -f .devcontainer/docker-compose.yaml -f docker-compose.kestra.yaml down -v; \
		docker volume prune -f; \
		docker network prune -f; \
		echo "${GREEN}Everything has been removed!${NC}"; \
	else \
		echo "Operation cancelled"; \
	fi