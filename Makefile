start:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose-test.yml down
	docker-compose -f docker-compose.yml up --build --abort-on-container-exit
test:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose-test.yml down
	docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit
db:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose-test.yml down
	docker-compose up db
