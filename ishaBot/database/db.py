import psycopg2
import datetime

def connectDB():
    conn = psycopg2.connect(database="d8rmfkj9kbk4vj", user = "irmealujtizmts", password = "7f26c5abf9c325baa94eeca76e4f230c0ec89a024f85b2d63ef4a27ea45497ad", host = "ec2-50-16-217-122.compute-1.amazonaws.com", port = "5432")
    print ("Opened database successfully")
    return conn

def insertTweetsBulk(urlList):
    conn = connectDB()
    cur = conn.cursor()
    localTime = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M')
    for url in urlList:
        cur.execute("INSERT INTO tweets VALUES ('"+url+"','"+localTime+"');")
        conn.commit()
        print ("Tweet inserted successfully");
    conn.close()

def loadTweets():
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("SELECT * from tweets")
    rows = cur.fetchall()
    print ("Tweets loaded successfully");
    conn.close()
    return rows

def clearDb():
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("DELETE from tweets;")
    conn.commit()
    print("All tweets deleted");
    conn.close()

def getUpdationTime():
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("SELECT * from tweets")
    rows = cur.fetchall()
    conn.close()
    return rows[0][1]