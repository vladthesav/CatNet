import mysql.connector

rds_host = "terraform-20230526210527221800000001.cglcexcu1hkr.us-east-2.rds.amazonaws.com"

mydb = mysql.connector.connect(
  host=rds_host,
  user="foo",
  password="foobarbaz",
  database="reddit_cat_pics"
)

print(mydb)

#make reddit cat pic db
with open("reddit_catpic_db_setup.sql","r") as f: reddit_db_create_script =f.read()
print(reddit_db_create_script)


mycursor = mydb.cursor()

#create table for reddit cat pics
mycursor.execute(reddit_db_create_script)
