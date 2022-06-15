
from multiprocessing.dummy import current_process
from click import command
import psycopg2
import sys, os
import numpy as np
import pandas as pd
import dbcreds as creds
import pandas.io.sql as psql
import random
def connecttodb():
    conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
    +" password="+ creds.PGPASSWORD
    conn=psycopg2.connect(conn_string)
    return conn
conn = connecttodb()
def create_tables(conn):
    cursor =conn.cursor()
    command = """
        CREATE TABLE players (
            player_name VARCHAR(255) NOT NULL,
            player_pass VARCHAR(255) NOT NULL,
            player_tries1 INT,
            player_tries2 INT,
            player_tries3 INT,
            player_tries4 INT
        )
        
        """
    command2 = """
            CREATE TABLE questions (
            question_id  INT,
            question_content VARCHAR(1000) NOT NULL,
            question_answers VARCHAR(1000) NOT NULL,
            answer INT NOT NULL
        )"""
    cursor.execute(command)
    conn.commit()
    
    cursor.execute(command2)
    conn.commit()
    

    
def fetchplayer(conn,pvs):
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM players WHERE player_name = '{}'".format(pvs[0]))
    vals = cursor.fetchall()
    return vals

playervars = ("Jane","12345678",19)
def insertplayer(conn,pvs):
    cursor =conn.cursor()
    """ insert a  player into the players table """
    sql = """INSERT INTO players (player_name,player_pass,player_tries1,player_tries2,player_tries3,player_tries4) 
    VALUES('{}','{}',{},{},{},{}) ;""".format(pvs[0],pvs[1],0,0,0,0)
    cursor.execute(sql)
    conn.commit()
def editplayer(conn,pvs):
    cursor =conn.cursor()
    updatevals = fetchplayer(conn,pvs)
    command = """UPDATE players
    SET player_tries4 = {player_tries3},player_tries3={player_tries2},player_tries2={player_tries1},player_tries1={}
    WHERE player_name = '{}';
    """.format(pvs[2],pvs[0],player_tries3 = updatevals[0][4],player_tries2 = updatevals[0][3],player_tries1 = updatevals[0][2])
    cursor.execute(command)
    conn.commit()

def manageplayer(conn,pvs):
    
    vals = fetchplayer(conn,pvs)
    if vals:
       editplayer(conn,pvs)
       conn.commit()
    else :
        insertplayer(conn,pvs)
        conn.commit()

#explicit type declaration TO DO ---- DONE
#add on rest of functions for ease of use and deubbuging TO DO 
##function returns tuple including question id and question content
def takequestion(conn,exclude=[]):#:psycopg2.connection):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(question_id) from questions;")
    numofquestions = cursor.fetchone()[0]
    print(numofquestions)
    cursor.execute("SELECT * FROM questions WHERE question_id = {}".format(random.choice([i for i in range(0,numofquestions) if i not in exclude])))
    question = cursor.fetchall()
    return question 
def addqtodbfromtxt(conn):
    cursor = conn.cursor()
    id = 100000
    content = "initiation"
    answer = 47
    answers =['1','2','3','4']
    with open("questions.txt","r",encoding="utf-8")  as file:
        for line in file:
            
            if not line.strip():
                continue
            if line.startswith("Q"):
                id =line.strip()
                id = id.translate({ord(i): None for i in 'Q.'})
                print(answers)
                answtxt = "$".join([i.replace("'","''") for i in answers])
                sql = """INSERT INTO questions (question_id,question_content,question_answers,answer) 
                    
                    VALUES({},'{}','{}',{}) ;""".format(int(id)-1,content.replace("'","''"),answtxt,answer)
                cursor.execute(sql)
                conn.commit()
                content = ''
                answer = 0
                answers = []
            else:
                if line[-3:] == "***":
                    answer = int(line[0])
                    answers.append(line[2:-1].lstrip())
                if line[0].isdigit() and line[1]==".":
                    answers.append(line[2:-1].lstrip())
                   
                
                else:
                    content += line


if __name__ == "__main__":
    conn = connecttodb()
    create_tables(conn)
    print(takequestion(conn))