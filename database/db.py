######################################################################
# Database Connection
#
# Provides the database connection used by the Patchip API.
#
# Database: MariaDB
# Database name: patchip
#
# SonarTech IoT
######################################################################

import pymysql
from config import Config

def get_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
