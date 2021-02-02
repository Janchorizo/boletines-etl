# boeDashboard

How to use the notebooks:

1. Make sure Docker is installed and your user has permissions

2. Create the database container by running `make create_mariadb`
    - You can enter the MySQL shell by running `make enter_mariadb`

3. Install the Python virtual environment by running `make install`
    - If you want to use other executable than _python3_ set it as an environment 
    argument: `make install -e PYTHON=python3.8`

4. Start the notebook server by running `make nb`