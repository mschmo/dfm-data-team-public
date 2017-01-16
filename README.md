### Local Environement Configuration
Run `vagrant up` to launch the vagrant box and provision PostreSQL.
Local command access to the database via psql:
`PGUSER=digitalfirst PGPASSWORD=localpass psql -h localhost -p 15432 digitalfirst`