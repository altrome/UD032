'''
Performs a query to the Map Mongo db and plots the results into a line plot
'''
import pandas as pd
from pymongo import MongoClient
from ggplot import *

def get_db(db_name):

    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    pipeline = [{ "$project": {
                                "year": { "$substr": [ "$created.timestamp", 0, 4 ] },
                                "month": { "$substr": [ "$created.timestamp", 5, 2 ] }
                            }
                }, 
                { "$group":   {   
                                "_id": { "year" : "$year" , "month" : "$month" }, 
                                "entries": { "$sum" : 1 } 
                            }
                }, 
                { "$sort":    { "_id" : 1 }}]
    return pipeline

def aggregate(db, pipeline):
    result = db.barcelona.aggregate(pipeline)
    return result

if __name__ == '__main__':
    # Query DB
    db = get_db('map')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    # Building output List
    output = []
    for doc in result:
        output.append([ doc["_id"]["year"], doc["_id"]["month"], int(doc["entries"])])  
    # Dataframe Costruction
    entriesDF = pd.DataFrame(output)
    # Identifying columns
    year = entriesDF[0]
    month = entriesDF[1]
    entries = entriesDF[2]
    # Ploting 
    gg = ggplot(entriesDF, aes('month', 'entries', color='year'))  + geom_line() + ggtitle('Total entries by month/Year')
    print gg



