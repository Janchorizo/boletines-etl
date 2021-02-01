activate:
	. ./venv/bin/activate

deactivate:
	deactivate

nb:
	. ./venv/bin/activate
	PYTHONPATH=. jupyter-notebook ./src --no-browser

.PHONY: nb activate deactivate