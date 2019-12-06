import pandas as pd
import numpy as np
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

if __name__=='__main__':
    df_data=pd.read_csv('books.csv')
    df_except=pd.DataFrame(columns=df_data.columns)
    # print(df_data)

    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    for indx,row in df_data.iterrows():
        print(f'Row: {indx}')
        isbn=row['isbn']
        title=row['title']
        author=row['author']
        year=int(row['year'])
        try:
            db.execute("INSERT INTO books (isbn,author,year,title) VALUES (:isbn,:author,:year,:title)",{"isbn":isbn,"author":author,"year":year,"title":title})
        except Exception as e:
            print(f'error in row {indx}.Error: {e}')
            df_except=df_except.append({'isbn':isbn,'title':title,'author':author,'year':year},ignore_index=True)
    db.commit()
    df_except.to_csv('exceptions.csv',index=False)

