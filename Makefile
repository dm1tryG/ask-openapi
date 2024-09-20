.PHONY: sync
sync:
	@if [ -z "$(url)" ]; then \
		echo "Error: url is not set. Please provide a valid URL."; \
		exit 1; \
	fi
	docker-compose exec ask_openapi python sync.py sync '$(url)'
url := $(word 2, $(MAKECMDGOALS))
%:
	@:



.PHONY: chat
chat:
	docker-compose up --build

.PHONY: clean
clean:
	rm -rf data/*
	data
