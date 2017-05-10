# Log Analysis Project

An internal reporting CLI to obtain data from a database and to generate an informative summary for a newspaper website. The database contains newspaper articles, as well as the web server log for the site. It uses Psycopg2 as PostgreSQL adapter and Click to do some magic on the command-line.

# Installation 

* Install Postgres on your machine

Required dependencies can be installed via pip:
```bash
$ pip install -r requirements.txt
``` 
create a Postgres database `news`:
```bash
$ createdb news
```
Finally import the dump file `newsdata.sql` into the database:
```bash
$ psql news < newsdata.sql
```

# Usage 
   ```bash
    $ python log_analysis.py
   ```
