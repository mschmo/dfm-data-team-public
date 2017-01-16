### Local Environement Configuration
1. Create a virtulenv `virtualenv env`, enable with `source env/bin/activate` and install dependencies `pip install -r requirements.txt`
2. Run `vagrant up` to launch the vagrant box and provision PostreSQL.
Local command access to the database via psql:
`PGUSER=digitalfirst PGPASSWORD=localpass psql -h localhost -p 15432 digitalfirst`
3. Run `./manage.py db upgrade` to migrate the DB based on the schema in /migrations directory
4. Now you can run `./manage app runserver` and access the application at `127.0.0.1:5000` on a browser. Clicking the button on that page will load the data from example_report.csv.gz into the DB and display the results. This will also create a separate file locally of the results.