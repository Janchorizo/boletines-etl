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
	PYTHONPATH=. jupyter-notebook ./src --no-browser

.PHONY: install uninstall activate nb activate deactivate