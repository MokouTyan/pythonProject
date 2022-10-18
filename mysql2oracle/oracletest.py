import cx_Oracle
import datetime
oracle_connection = cx_Oracle.connect("blues", "blues", "192.168.141.13:1521/itfdatapool.itfdatapool", encoding="UTF-8")
oracle_cursor = oracle_connection.cursor()


# sql = '''INSERT INTO SQ_DAILYRANK_NOFUTURE ("DATE", "INSTRUMENTID", "ALL_", "ALL_CHANGE", "BUY", "BUY_CHANGE", "SELL", "SELL_CHANGE") VALUES(:1, :2, :3, :4, :5, :6, :7, :8)'''
#
# oracle_cursor.execute(sql,(datetime.datetime(2022, 7, 26, 23, 2, 34), "cuall",610236, -45905, 414820,15421, 416882, 14507))
sql = '''INSERT INTO SQ_DAILYRANK_NOFUTURE ("DATE", "INSTRUMENTID", "ALL_", "ALL_CHANGE", "BUY", "BUY_CHANGE", "SELL", "SELL_CHANGE") VALUES(:1, :2, :3, :4, :5, :6, :7, :8)'''

oracle_cursor.execute(sql,(datetime.datetime(2022, 7, 26, 23, 2, 34), "cuall",610236, -45905, 414820,15421, 416882, 14507))
oracle_connection.commit()
oracle_cursor.close()
oracle_connection.close()
