
.PHONY: run
run:
	- docker network create insurance
	- docker-compose -f docker-compose.yaml up -d
	- cd db && make build && make run && cd .. && \
	cd migrations && make build && make run && cd .. && \
	cd api && make build && make run && cd ..
