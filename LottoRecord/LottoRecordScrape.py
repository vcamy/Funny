import requests
import json
import mysql.connector
from datetime import datetime
from datetime import date
from datetime import timedelta

def main():
    url = "https://apigw.mylotto.co.nz/api/results/v1/results/lotto/{}"
    drawInfo = getLastDrawInfo()
    if len(drawInfo) < 2:
        print("get latest draw info wrong")
    count = calcLatestCount(drawInfo[1])
    lastDraw = drawInfo[0]
    while count > 0:
        lastDraw = lastDraw + 1
        response = fetchResult(url.format(lastDraw))
        if response is not None:
            result = parseResult(response)
            saveData(result)
        else:
            print("Fail to fetch data")
        count -= 1 


def calcLatestCount(drawDate):
    today = date.today()
    last_day = date.fromisoformat(drawDate)
    num = 0
    today = today - timedelta(days=1)
    while today > last_day:
        if today.weekday() == 2 or today.weekday() == 5:
            num = num+1         
        today = today - timedelta(days=1)
    return num


def fetchResult(url):
    try:
        response = requests.get(url)
    except (HTTP):
        print('Failed to fetch data from %\nURL: %s',url)
        return 
    else:
        return response.json()
    

def parseResult(data):
    result = []
##    result["id"] = data["lotto"]["drawNumber"]
##    result["date"] = data["lotto"]["drawDate"]
##    result["num1"] = data["lotto"]["lottoWinningNumbers"]["numbers"][0]
##    result["num2"] = data["lotto"]["lottoWinningNumbers"]["numbers"][1]
##    result["num3"] = data["lotto"]["lottoWinningNumbers"]["numbers"][2]
##    result["num4"] = data["lotto"]["lottoWinningNumbers"]["numbers"][3]
##    result["num5"] = data["lotto"]["lottoWinningNumbers"]["numbers"][4]
##    result["num6"] = data["lotto"]["lottoWinningNumbers"]["numbers"][5]
##    result["bonus"] = data["lotto"]["lottoWinningNumbers"]["bonusBalls"]
##    result["powerBall"] = data["powerBall"]["powerballWinningNumber"]

    result.append(data["lotto"]["drawNumber"])
    result.append(data["lotto"]["drawDate"])
    result.append(data["lotto"]["lottoWinningNumbers"]["numbers"][0])
    result.append(data["lotto"]["lottoWinningNumbers"]["numbers"][1])
    result.append(data["lotto"]["lottoWinningNumbers"]["numbers"][2])
    result.append(data["lotto"]["lottoWinningNumbers"]["numbers"][3])
    result.append(data["lotto"]["lottoWinningNumbers"]["numbers"][4])
    result.append(data["lotto"]["lottoWinningNumbers"]["numbers"][5])
    result.append(data["lotto"]["lottoWinningNumbers"]["bonusBalls"])
    result.append(data["powerBall"]["powerballWinningNumber"])
    return result


def saveData(item):
    print(item)
##    connection_string = getConnectionString()
##    cnxn = pyodbc.connect(connection_string)
    myDB = connect_db()
    cursor = myDB.cursor()
    insert_query = "INSERT INTO lotto_results(DrawID, DrawDate, NumOne, NumTwo, NumThree, NumFour,NumFive,NumSix,Bonus,Powerball) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, item)
    myDB.commit()
    myDB.close()
    return

def getConnectionString():
    server = 'tcp:mylottoserver.database.windows.net,1433'
    database = 'lottodb'
    username = 'root'
    password = 'Admin!@#123'
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server + ';DATABASE='+database+';UID='+username+';PWD='+password
    return connection_string


def connect_db():
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin!@#123",
        database="lottodb"
        )
    return myDB

def getLastDrawInfo():
##    connection_string = getConnectionString()
##    print(connection_string)
##    cnxn = pyodbc.connect(connection_string)
##    cursor = cnxn.cursor()
##    cursor.execute("SELECT TOP 1 DrawID, DrawDate FROM [dbo].[LottoDraws] ORDER BY DrawID DESC")
##    last_draw = cursor.fetchone()
##    cursor.close()
    myDB = connect_db()
    print(myDB)
    mycursor = myDB.cursor()
    mycursor.execute("SELECT DrawID, DrawDate FROM lotto_results ORDER BY DrawID DESC Limit 1")
    last_draw = mycursor.fetchone()
    mycursor.close()
    print(last_draw)
    return last_draw

def initialDB():
    url = "https://apigw.mylotto.co.nz/api/results/v1/results/lotto/1867"
    response = fetchResult(url)
    if response is not None:
            result = parseResult(response)
            saveData(result)
    
    else:
        print("Fail to initial database")

main()
