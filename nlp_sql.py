## Key with paid service

import openai
import panel as pn
openai.api_key="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"



def continue_conversation(messages, temperature=0):
    
    response = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature, 
    )

    return response.choices[0].message["content"]

# def continue_conversation(natural_language_query):
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=f"Translate the following natural language query into SQL: {natural_language_query}",
#         max_tokens=50,  # You can adjust this as needed
#         stop=None,  # You can add a stop word if needed
#         temperature=0.7  # You can adjust this to control the randomness of the output
#     )
#     return response.choices[0].text

context = [{'role':'system', 'content':"""
you are a bot to assist in create SQL commands, all your answers should start with \
this is your SQL, and after that an SQL that can do what the user request. \
Your Database is composed by a SQL database with some tables. \
Try to Maintain the SQL order simple.
Put the SQL command in white letters with a black background, and just after \
a simple and concise text explaining how it works. 
If the user ask for something that can not be solved with an SQL Order \
just answer something nice and simple and ask him for something that \
can be solved with SQL. 
"""}]

context.append( {'role':'system', 'content':"""
first table: 
{
  "tableName": "employees",
  "fields": [
    {
      "nombre": "ID_usr",
      "tipo": "int"
    },
    {
      "nombre": "name",
      "tipo": "string"
    }
  ]
}
"""
})

context.append( {'role':'system', 'content':"""
second table: 
{
  "tableName": "salary",
  "fields": [
    {
      "nombre": "ID_usr",
      "type": "int"
    },
    {
      "yt": "year",
      "type": "date"
    },
    {
      "sal": "salary",
      "type": "float"
    }
  ]
}
"""
})

context.append( {'role':'system', 'content':"""
third table: 
{
  "tablename": "studies",
  "fields": [
    {
      "name": "ID",
      "type": "int"
    },
    {
      "ee": "ID_usr",
      "type": "int"
    },
    {
      "edu": "educational level",
      "type": "int"
    },
    {
      "name": "Institution",
      "type": "string"
    },
    {
      "yr": "Years",
      "type": "date"
    }
    {
      "spl": "Speciality",
      "type": "string"
    }
  ]
}

"""
})

# msg="select empyoyees whoses education level is Masters"
msg="select empyoyees nombre whose sal is 30000 and ans have studied in the yr 2003"
# ww=continue_conversation(msg)

# print("YOUR SQL QUERY : ",ww)

#give me the employee graduates in 2017

context.append({'role':'user', 'content':f"{msg}"})
context.append({'role':'system', 'content':f"Remember your instructions as SQL Assistant."})
response = continue_conversation(context)
context.append({'role':'assistant', 'content':f"{response}"})

print()
#%%
context=[{'role':'system', 'content':"""
first table: 
{
  "tableName": "State",
  "fields": [
    {
      "St_ID": "State_ID",
      "tipo": "int"
    },
    {
      "Ste": "State",
      "tipo": "string"
    }
  ]
}
"""
}]

context.append({'role':'system', 'content':"""
Second table: 
{
  "tableName": "District",
  "fields": [
    {
      "Dis_ID": "District_ID",
      "tipo": "int"
    },
    {
      "Dist": "District",
      "tipo": "string"
    }
  ]
}
"""
})
    

context.append({'role':'system', 'content':"""
Thrid table: 
{
  "tableName": "City",
  "fields": [
    {
      "Cty_ID": "City_ID",
      "tipo": "int"
    },
    {
      "Cty": "City",
      "tipo": "string"
    },
    {
      "VillgTwn": "Village Town",
      "tipo": "int"
    },
    {
      "Lat": "Latitude",
      "tipo": "float"
    },
    {
      "Lon": "Longitude",
      "tipo": "float"
    },
    {
      "SubD": "SubRD Code",
      "tipo": "int"
    }
  ]
}
"""
})
    
#%%


import os
os.environ['OPENAI_API_KEY'] = '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'
# import sqlite3

# def read_sql_query(sql, db):
    
#     conn = sqlite3.connect(db)
#     print(conn)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)
#     conn.close()
    
# read_sql_query('SELECT * FROM fashion_products LIMIT 10;',
#                "fashion_db.sqlite")


#%%
import mysql.connector


mydb = mysql.connector.connect(
    host = "192.168.10.49",
    user = "sort",
    password = "sort",
    database="test4"
)
 
# cursor = mydb.cursor()
 
    
# cursor.execute("SHOW TABLES")

# for i in cursor:
#     print(i)

sql_select_Query = "select * from 91_village_master"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()

#%%

import numpy as np
import pandas as pd
import sqlite3

df = pd.read_excel(r"C:\Users\Sort\Desktop\SubD_Cluster_For_TSI_30Aug20233.xlsx") 


conn = sqlite3.connect('fashion_db.sqlite')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS fashion_products (user_id int, product_id int, product_name text, brand text, category text, price int, rating float, color text, size text)')
conn.commit()

df.to_sql('fashion_products', conn, if_exists='replace', index = False)

c.execute('''
SELECT product_name FROM fashion_products LIMIT 100
          ''')

for row in c.fetchall():
    print (row)

#%%


from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# input_db = SQLDatabase.from_uri('sqlite:///fashion_db.sqlite')


input_db=records

#%%


llm_1 = OpenAI(temperature=0)


db_agent = SQLDatabaseChain(llm = llm_1,
                            database = input_db,
                            verbose=True)

db_agent.run("how many rows are there?")

db_agent.run("how many entries of Adidas are present?")

db_agent.run("how many XL products of Nike are there that have a rating of more than 4?")

db_agent.run("Give all the details of Adidas which have a size of L and have a rating of more than 4.2")


#%%

import mysql.connector


mydb = mysql.connector.connect(
    host = "192.168.10.49",
    user = "sort",
    password = "sort",
    database="test4"
)
 
# cursor = mydb.cursor()
 
# cursor.execute("SHOW TABLES")

# for i in cursor:
#     print(i)

sql_select_Query = "select * from 91_village_master"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()


#%%

import os
import openai

openai.api_key = os.getenv('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')

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "Given the following SQL tables, your job is to write queries given a user’s request.\n\nCREATE TABLE Orders (\n  OrderID int,\n  CustomerID int,\n  OrderDate datetime,\n  OrderTime varchar(8),\n  PRIMARY KEY (OrderID)\n);\n\nCREATE TABLE OrderDetails (\n  OrderDetailID int,\n  OrderID int,\n  ProductID int,\n  Quantity int,\n  PRIMARY KEY (OrderDetailID)\n);\n\nCREATE TABLE Products (\n  ProductID int,\n  ProductName varchar(50),\n  Category varchar(50),\n  UnitPrice decimal(10, 2),\n  Stock int,\n  PRIMARY KEY (ProductID)\n);\n\nCREATE TABLE Customers (\n  CustomerID int,\n  FirstName varchar(50),\n  LastName varchar(50),\n  Email varchar(100),\n  Phone varchar(20),\n  PRIMARY KEY (CustomerID)\n);"
    },
    {
      "role": "user",
      "content": "Write a SQL query which computes the average total order value for all orders on 2023-04-01."
    }
  ],
  temperature=0,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


#%%%
import GeoDistanceLinear

print(GeoDistanceLinear.geo_dist([16.01205963,78.66843376],[15.87607985,78.58298811]))


#%%
import requests

def scrap(df2,id1):
    url='https://route.api.here.com/routing/7.2/calculateroute.json?alternatives=2&app_code=LJXqQ8ErW71UsRUK3R33Ow&app_id=VgTVFr1a0ft1qGcLCVJ6&departure=2021-10-25T09:50:17&jsonAttributes=41&language=en_US&legattributes=all&linkattributes=none,sh,ds,rn,ro,nl,pt,ns,le,fl&maneuverattributes=all&metricSystem=metric&mode=fastest;car;traffic:enabled;&routeattributes=none,sh,wp,sm,bb,lg,no,li,tx,la&transportMode=car&walkSpeed=1.4&waypoint0=street!'+str(df2[0])+','+str(df2[1])+'!'+str(df2[0])+','+str(df2[1])+'&waypoint1=street!'+str(id1[0])+','+str(id1[1])+'!'+str(id1[0])+','+str(id1[1])
    data = requests.get(url).json()
    distance=round(data['response']['route'][0]['summary']['distance']/1000,1)
    time=round(data['response']['route'][0]['summary']['baseTime']/60,1)
    return distance,time

print(scrap([16.01205963,78.66843376],[15.87607985,78.58298811]))

#%%

# # DISTRICTS MASTER TABLE

# CREATE TABLE `district_master` (
#   `refid` bigint(20) NOT NULL AUTO_INCREMENT,
#   `country_id` bigint(20) DEFAULT NULL,
#   `state_id` bigint(20) DEFAULT NULL,
#   `scr_id` mediumint(9) NOT NULL,
#   `location_name` varchar(50) NOT NULL,
#   `map_id` varchar(50) NOT NULL,
#   `nxt_mp_level` bigint(20) NOT NULL,
#   `loc_id` bigint(20) NOT NULL,
#   `creatd_period` varchar(5) NOT NULL,
#   `2001_census` varchar(15) NOT NULL,
#   `2011_census` varchar(15) NOT NULL,
#   `latitude` varchar(50) NOT NULL,
#   `longitude` varchar(50) NOT NULL,
#   `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `stat` char(1) NOT NULL DEFAULT 'A',
#   PRIMARY KEY (`refid`),
#   KEY `refid` (`refid`,`stat`),
#   KEY `state_id` (`state_id`,`creatd_period`,`stat`),
#   KEY `state_id_2` (`state_id`,`2001_census`),
#   KEY `location_name` (`location_name`),
#   KEY `2001_census` (`2001_census`),
#   KEY `scr_id` (`scr_id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=4757 DEFAULT CHARSET=latin1


# %%

# # STATE MASTER TABLE


# CREATE TABLE `state_master` (
#   `refid` bigint(20) NOT NULL AUTO_INCREMENT,
#   `country_id` bigint(20) DEFAULT NULL,
#   `location_name` varchar(50) NOT NULL,
#   `zone_id` int(11) NOT NULL COMMENT 'zone_master',
#   `zone_name` varchar(100) NOT NULL COMMENT 'zone_master',
#   `map_id` varchar(50) NOT NULL,
#   `nxt_mp_level` bigint(20) NOT NULL,
#   `loc_id` bigint(20) NOT NULL,
#   `creatd_period` varchar(4) NOT NULL,
#   `2001_census` varchar(15) NOT NULL,
#   `2011_census` varchar(15) NOT NULL,
#   `latitude` varchar(50) NOT NULL,
#   `longitude` varchar(50) NOT NULL,
#   `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `stat` char(1) NOT NULL DEFAULT 'A',
#   PRIMARY KEY (`refid`),
#   KEY `refid` (`refid`,`stat`),
#   KEY `country_id` (`country_id`,`creatd_period`,`stat`),
#   KEY `2001_census` (`2001_census`,`stat`),
#   KEY `location_name` (`location_name`)
# ) ENGINE=MyISAM AUTO_INCREMENT=211 DEFAULT CHARSET=latin1



# %%



# # Taluk MASTER TABLE



# CREATE TABLE `taluk_master` (
#   `refid` bigint(20) NOT NULL AUTO_INCREMENT,
#   `country_id` bigint(20) DEFAULT NULL,
#   `state_id` bigint(20) DEFAULT NULL,
#   `district_id` bigint(20) DEFAULT NULL,
#   `scr_id` smallint(6) NOT NULL,
#   `location_name` varchar(50) NOT NULL,
#   `map_id` varchar(50) NOT NULL,
#   `nxt_mp_level` bigint(20) NOT NULL,
#   `loc_id` bigint(20) NOT NULL,
#   `creatd_period` varchar(5) NOT NULL,
#   `2001_census` varchar(15) NOT NULL,
#   `2011_census` varchar(15) NOT NULL,
#   `latitude` varchar(50) NOT NULL,
#   `longitude` varchar(50) NOT NULL,
#   `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `stat` char(1) NOT NULL DEFAULT 'A',
#   PRIMARY KEY (`refid`),
#   KEY `refid` (`refid`,`stat`),
#   KEY `district_id` (`district_id`,`creatd_period`,`stat`),
#   KEY `state_id` (`state_id`,`creatd_period`,`stat`)
# ) ENGINE=MyISAM AUTO_INCREMENT=14013 DEFAULT CHARSET=latin1


# %%

# Village MASTER TABLE


# CREATE TABLE `village_master` (
#   `refid` int(11) NOT NULL AUTO_INCREMENT,
#   `world_id` int(11) NOT NULL DEFAULT '1',
#   `country_id` tinyint(3) NOT NULL,
#   `state_id` smallint(6) NOT NULL,
#   `district_id` mediumint(9) NOT NULL,
#   `scr_id` int(11) NOT NULL COMMENT 'loc8( bid_application_master.district_master)',
#   `taluk_id` mediumint(9) NOT NULL,
#   `pincode_id` int(11) NOT NULL,
#   `ua_id` int(11) NOT NULL,
#   `ua_id_bkp` mediumint(9) NOT NULL,
#   `location_name` varchar(100) NOT NULL,
#   `location_name_org` varchar(50) NOT NULL,
#   `map_id_old` varchar(50) NOT NULL,
#   `map_id_20Aug15_bkp` varchar(100) NOT NULL COMMENT 'b4 up corrections',
#   `map_id_04Mar16_bkp` varchar(50) NOT NULL COMMENT 'B4 Update MP Uninhbtd Villg Crtn',
#   `map_id` varchar(100) NOT NULL COMMENT '"After UP crtn 18Aug14"',
#   `nxt_mp_level` tinyint(3) NOT NULL,
#   `loc_id` int(11) NOT NULL,
#   `creatd_period` varchar(5) NOT NULL,
#   `road` char(1) NOT NULL COMMENT '"H - Highway"',
#   `highways_2016` tinyint(4) NOT NULL COMMENT '1 - Avlbl, 0 - Not Avlbl',
#   `mandi` int(11) NOT NULL COMMENT '1 - Yes,0 - No',
#   `2001_census` varchar(15) NOT NULL,
#   `2011_census` varchar(15) NOT NULL,
#   `tot_pop_2001` int(50) NOT NULL,
#   `tot_pop_2011_old` int(50) NOT NULL,
#   `tot_pop_2011` int(50) NOT NULL,
#   `growth_2012` varchar(100) NOT NULL DEFAULT '0',
#   `growth_2013` varchar(100) NOT NULL DEFAULT '0',
#   `growth_2014` varchar(100) NOT NULL DEFAULT '0',
#   `growth_2015` varchar(100) NOT NULL DEFAULT '0',
#   `growth_2016` varchar(100) NOT NULL DEFAULT '0',
#   `growth_2017` double NOT NULL,
#   `tot_pop_2012_bkup` int(100) NOT NULL,
#   `tot_pop_2013_bkup` int(100) NOT NULL,
#   `tot_pop_2014_bkup` int(100) NOT NULL,
#   `tot_pop_2012` int(11) NOT NULL,
#   `tot_pop_2013` int(11) NOT NULL,
#   `tot_pop_2014` int(11) NOT NULL,
#   `tot_pop_2015` int(11) NOT NULL,
#   `tot_pop_2016` int(11) NOT NULL,
#   `tot_pop_2017` int(11) NOT NULL,
#   `tot_pop_2018` double NOT NULL,
#   `tot_pop_2019` double NOT NULL,
#   `tot_pop_2020` double NOT NULL,
#   `tot_pop_2021` double NOT NULL,
#   `spec_2001` tinyint(4) NOT NULL,
#   `spec_2011_old` tinyint(4) NOT NULL,
#   `spec_2011` int(50) NOT NULL,
#   `spec_2012_bkup` int(100) NOT NULL,
#   `spec_2013_bkup` int(100) NOT NULL,
#   `spec_2014_bkup` int(100) NOT NULL,
#   `spec_2012` int(11) NOT NULL,
#   `spec_2013` int(11) NOT NULL,
#   `spec_2014` int(11) NOT NULL,
#   `spec_2015` int(11) NOT NULL,
#   `spec_2016` int(11) NOT NULL,
#   `spec_2017` int(11) NOT NULL,
#   `spec_2018` int(11) NOT NULL COMMENT 'same as 2017',
#   `spec_2019` double NOT NULL,
#   `spec_2020` smallint(6) NOT NULL,
#   `spec_2021` smallint(6) NOT NULL,
#   `spec_2022` int(11) NOT NULL,
#   `latitude` varchar(50) NOT NULL,
#   `longitude` varchar(50) NOT NULL,
#   `latitude_mar2023` double NOT NULL,
#   `longitude_mar2023` double NOT NULL,
#   `latitude_bkp` double NOT NULL,
#   `longitude_bkp` double NOT NULL,
#   `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `remarks` varchar(150) NOT NULL,
#   `stat` char(1) NOT NULL DEFAULT 'A' COMMENT 'C - Gr Noida Clubbed',
#   PRIMARY KEY (`refid`),
#   KEY `latitude` (`latitude`,`longitude`),
#   KEY `spec_2022` (`spec_2022`),
#   KEY `state_id` (`state_id`),
#   KEY `2011_census` (`2011_census`),
#   KEY `2001_census` (`2001_census`),
#   KEY `map_id` (`map_id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=1262847 DEFAULT CHARSET=latin1


# %%


# Progressive INDEX OF VILLAGE


# CREATE TABLE `progressive index` (
#   `refid` int(11) NOT NULL AUTO_INCREMENT,
#   `loc5` int(11) NOT NULL DEFAULT '1' COMMENT 'country id',
#   `loc7` int(11) NOT NULL COMMENT 'state_id',
#   `loc9` int(11) NOT NULL COMMENT 'district_id',
#   `loc8` int(11) NOT NULL COMMENT 'scr_id(bid_application_master.district_master)',
#   `loc10` int(11) NOT NULL COMMENT 'taluk_id',
#   `loc11` int(11) NOT NULL,
#   `loc12` int(11) NOT NULL,
#   `loc13` varchar(100) DEFAULT NULL COMMENT 'village_id',
#   `loc14` varchar(100) NOT NULL COMMENT 'city/villg_id',
#   `loc22` int(11) NOT NULL,
#   `loc23` int(11) NOT NULL,
#   `loc25` int(11) NOT NULL,
#   `area` int(11) NOT NULL,
#   `hhs` varchar(100) DEFAULT NULL,
#   `pop` varchar(100) DEFAULT NULL,
#   `fld_master_id` int(11) NOT NULL,
#   `cluster_id` int(50) NOT NULL,
#   `cluster_old` varchar(100) DEFAULT NULL COMMENT 'village_cluster_ranking',
#   `cluster` varchar(100) NOT NULL,
#   `taluk_cluster_ranking` varchar(100) DEFAULT NULL,
#   `index_score` double NOT NULL,
#   `rpi_score` double NOT NULL,
#   `mdlz_biscuit` int(11) NOT NULL,
#   `mdlz_chocolate` int(11) NOT NULL,
#   `mdlz_snacks` int(11) NOT NULL,
#   `mdlz_whlslr` varchar(100) NOT NULL COMMENT 'given by sales team',
#   `jj_whlslr` int(11) NOT NULL COMMENT 'given by sales team',
#   `mdlz_sub_distbtr` text NOT NULL COMMENT 'given by sales team',
#   `national_highway` int(11) NOT NULL COMMENT 'vlg_amnts',
#   `state_highway` int(11) NOT NULL COMMENT 'vlg_amnts',
#   `bank_avlblty` varchar(100) NOT NULL,
#   `atm_avlblty` varchar(100) NOT NULL COMMENT '1-avlbl,2-not avlbl',
#   `schl_avlblty` varchar(100) NOT NULL,
#   `clgs_avlblty` varchar(100) NOT NULL,
#   `bus_avlblty` varchar(100) NOT NULL,
#   `mandi_avlblty` varchar(100) NOT NULL,
#   `rlway_stn_avlblty` varchar(100) NOT NULL,
#   `rank` varchar(100) DEFAULT NULL,
#   `feeder_id` int(8) NOT NULL,
#   `feeder_loc` varchar(150) NOT NULL,
#   `distance_feeder_id` int(11) NOT NULL,
#   `Distance_to_nearest_feeder` varchar(100) NOT NULL,
#   `impact_score` int(11) NOT NULL,
#   `impact_score_id` int(11) NOT NULL,
#   `descptn` varchar(100) NOT NULL COMMENT 'for meeting 14may7',
#   `descrptn_2020` varchar(100) NOT NULL,
#   `descrptn_whlslr` varchar(100) NOT NULL,
#   `descrptn_sub_rd` varchar(100) NOT NULL,
#   `stat` char(1) NOT NULL DEFAULT 'A',
#   PRIMARY KEY (`refid`),
#   KEY `loc13` (`loc13`),
#   KEY `loc7` (`loc7`,`loc14`),
#   KEY `loc7_2` (`loc7`,`impact_score`),
#   KEY `loc7_3` (`loc7`,`loc14`,`area`,`stat`),
#   KEY `loc7_4` (`loc7`,`loc14`,`stat`),
#   KEY `loc7_5` (`loc7`,`cluster_id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=616161 DEFAULT CHARSET=latin1

# %%


# Village



