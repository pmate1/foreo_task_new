import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import json


# import users info from .json file to gain access to postgresql database
f = open('E:/Documents/settings.json')
data = json.load(f)
u_name = data['username']
pw = data['password']


# create table in postgresql database
def create_table():

    command = (
        """
        CREATE TABLE last_week(
            store_no varchar(10) primary key,
            store varchar(40) not null,
            ty_units bigint,
            ly_units bigint,
            tw_sales float8,
            lw_sales float8,
            lw_var float8,
            ly_sales float8,
            ly_var float8,
            ytd_sales float8,
            lytd_sales float8,
            lytd_var float8
        );
        """)

    # establish the connection
    conn = psycopg2.connect(database="task", user=u_name, password=pw, host="localhost", port="5432")
    cur = conn.cursor()

    # check if the table already exist
    cur.execute("select exists(select * from information_schema.tables where table_name='last_week')")
    if not bool(cur.fetchone()[0]):
        # creates a table and close the connection
        cur.execute(command)
        conn.commit()
        cur.close()
        conn.close()
    else:
        cur.close()
        conn.close()
        return


# read the data from excel file
def read_data():

    data_frame = pd.read_excel('E:/Documents/SpaceNK_2.0.xlsx', header=5,
                               usecols=['Store No', 'Store', 'TY Units', 'LY Units', 'TW Sales', 'LW Sales',
                                        'LW Var %', 'LY Sales', 'LY Var %', 'YTD Sales', 'LYTD Sales', 'LYTD Var %'],
                               sheet_name='Last Week Report by Store', skipfooter=1)

    # rename the dataframe columns to match those of the table in postgresql database
    data_frame.rename(columns={'Store No': 'store_no',
                               'Store': 'store',
                               'TY Units': 'ty_units',
                               'LY Units': 'ly_units',
                               'TW Sales': 'tw_sales',
                               'LW Sales': 'lw_sales',
                               'LW Var %': 'lw_var',
                               'LY Sales': 'ly_sales',
                               'LY Var %': 'ly_var',
                               'YTD Sales': 'ytd_sales',
                               'LYTD Sales': 'lytd_sales',
                               'LYTD Var %': 'lytd_var'}, inplace=True)

    return data_frame


# insert the data from dataframe to postgresql table
def insert_data(d_frame):

    # establish the connection
    url = "postgresql://" + u_name + ":" + pw + "@localhost:5432/task"
    engine = create_engine(url)
    conn = engine.connect()

    # replace the data for the "new" last week and close the connection
    conn.execute(text("TRUNCATE TABLE last_week;"))
    d_frame.to_sql('last_week', con=conn, if_exists='append', index=False)
    conn.commit()
    conn.close()


if __name__ == '__main__':

    create_table()
    df = read_data()
    insert_data(df)
