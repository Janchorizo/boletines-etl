# boeDashboard

## How to use the notebooks:

1. Make sure Docker is installed and your user has permissions

2. Create the database container by running `make create_mariadb`
    - You can enter the MySQL shell by running `make enter_mariadb`

3. Install the Python virtual environment by running `make install`
    - If you want to use other executable than _python3_ set it as an environment 
    argument: `make install -e PYTHON=python3.8`

4. Start the notebook server by running `make nb`

## How to run a local pipeline (without indexing)
It is possible to run the pipelines for a specific date or for a range of dates from a start to current time. With the requirements installed and from
within the `/src` folder you can run either of these commands.

For a range of dates:
```bash
PYTHONPATH=. luigi \
    --module pipelines.local_no_indexing_boe_pipeline \
    --RangeDaily --of Pipeline \
    --start 2021-01-20 \
    --local-scheduler \
    --workers 3 \
    --GlobalParams-base-dir ./temp \
    --DBParams-host localhost \
    --DBParams-user root \
    --DBParams-password pass \
    --DBParams-database boe
```

For a single date:
```bash
PYTHONPATH=. luigi \
    --module pipelines.local_no_indexing_boe_pipeline \
    Pipeline \
    --local-scheduler \
    --workers 3 \
    --GlobalParams-base-dir ./temp \
    --DBParams-host localhost \
    --DBParams-user root \
    --DBParams-password pass \
    --DBParams-database boe \
    --date 2021-01-26
```
