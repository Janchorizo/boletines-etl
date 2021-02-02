PYTHON='python3'

install: uninstall
	bash -c "$(PYTHON) -m venv venv" && \
		. ./venv/bin/activate && \
		python3 -m pip install -r requirements.txt

uninstall:
	rm -fr ./venv 2>&-

activate:
	@echo "Run the following comand:"
	@echo ". ./venv/bin/activate"

deactivate:
	@echo "Run the following comand:"
	@echo "deactivate"

nb:
	. ./venv/bin/activate
	PYTHONPATH=. jupyter-notebook ./notebooks --no-browser

create_mariadb:
	docker run -p 3306:3306 --name maria -e MYSQL_ROOT_PASSWORD=pass -e MYSQL_USER=jancho -d mariadb

start_mariadb:
	docker container start mariadb

stop_mariadb:
	docker container stop mariadb

enter_mariadb:
	@echo "Use password \"pass\""
	docker exec -it maria mysql -u root -p

.PHONY: install uninstall activate nb activate deactivate create_mariadb start_mariadb stop_mariadb enter_mariadb