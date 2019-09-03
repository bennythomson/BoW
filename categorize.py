#CLI to quickly add structured data to the database to be used to categorize words
import json
import sqlite3

conn = sqlite3.connect('training.db')
c = conn.cursor()


def setup_db():
    c.execute('''CREATE TABLE training_data (sentence text, sentiment bool)''')

def add(sentence, sentiment):
    t = (sentence,sentiment)

    c.execute("INSERT INTO training_data VALUES(?,?)",t)

    conn.commit()

def main():


    print("P - enter positive sentences")
    print("N - enter negative sentences")
    typ = input("?")

    if typ == "P":
        sentiment = True
        while True:
            sen = input("Enter positive sentences, X to cancel: ")
            if sen == "X":
                break
            else:
                add(sen, True)
    elif typ == "N":
        sentiment = False
        while True:
            sen = input("Enter negative sentences, X to cancel: ")
            if sen == "X":
                break
            else:
                add(sen, False)






if __name__== "__main__":
    #setup_db()
    main()
