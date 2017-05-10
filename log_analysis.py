#!/bin/env python
"""internal reporting CLI"""
import psycopg2
import click

# Queries

QUERY1 = ("SELECT a.title, COUNT(*) AS Views "
          "FROM articles a, log l "
          "WHERE l.path like '%' || a.slug "
          "GROUP BY a.title "
          "ORDER BY views DESC limit 3;")


QUERY2 = ("WITH articleview AS "
          "(SELECT a.id, COUNT(*) AS views "
          "FROM articles a, log l "
          "WHERE l.path like '%' || a.slug "
          "GROUP BY a.id) "
          "SELECT auth.name, SUM(ab.views) AS views "
          "FROM authors auth, articleview ab, articles a "
          "WHERE a.author=auth.id "
          "AND ab.id = a.id "
          "GROUP BY auth.name "
          "ORDER BY views DESC;")


QUERY3 = ("WITH n_ok AS "
          "(SELECT date_trunc('day', time) AS day, COUNT(*) AS pageviews "
          "FROM log WHERE log.status='404 NOT FOUND' GROUP BY 1 ORDER BY 1), "
          "allp AS "
          "(SELECT date_trunc('day', time) AS day, COUNT(*) AS pageviews "
          "FROM log GROUP BY 1 ORDER BY 1), "
          "dayv AS "
          "(SELECT date_trunc('day', time) AS day, COUNT(*) AS pageviews "
          "FROM log GROUP BY 1 ORDER BY 1), "
          "final AS "
          "(SELECT dayv.day, "
          "round(n_ok.pageviews::numeric/allp.pageviews::numeric * 100,2) "
          "AS error "
          "FROM dayv, n_ok, allp "
          "WHERE allp.day = n_ok.day AND dayv.day = allp.day) "
          "SELECT *"
          "FROM final "
          "WHERE error > 1;")

Q_LIST = [QUERY1, QUERY2, QUERY3]


def query_db(query, db_conn):
    """creates a new cursor, executes query and
    returns a dict of query results"""

    cur = db_conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return results


def report_output(res_l):
    """generates a nicely formatted summary of query results"""

    out = "Top 3 most viewed articles:\n\n"
    for tup in res_l[0]:
        out += "\"%s\" - %d views\n" % (tup[0], tup[1])

    out += "\nMost popular article authors:\n\n"
    for tup in res_l[1]:
        out += "%s - %d views\n" % (tup[0], tup[1])

    out += "\nDays in which more than 1% of requests led to errors:\n\n"
    for tup in res_l[2]:
        str_date = tup[0].strftime("%B %d, %Y")
        out += "%s - %3.2f%% errors\n" % (str_date, tup[1])

    return out


def runner():
    """shows status of db operations
    and prints summary of query results to console"""

    click.echo("Connecting to DB...", nl=False)
    db_conn = psycopg2.connect("dbname=news user=ubuntu")
    click.echo("Done")

    results = []

    for query in Q_LIST:
        click.echo("Obtaining data from query result...", nl=False)
        results.append(query_db(query, db_conn))
        click.echo("Done")

    click.echo("Log analysis report is ready")
    click.pause()
    click.clear()
    click.echo(report_output(results))

if __name__ == "__main__":
    runner()
