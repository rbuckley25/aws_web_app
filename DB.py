import sqlalchemy as sql
import pandas as pd



class Database:
    
    def __init__(self):

        username = "c_admin"
        password = "jTFLjGuQTYenRojiRRSC"
        hostname = "cloudservices.czi7jpt4jrwk.eu-west-1.rds.amazonaws.com"
        port = "3306"
        database = "CloudDB"
        # Initialise engine database connection
        db_conn_string = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
        self.engine = sql.create_engine(db_conn_string)
        self.conn = self.engine.raw_connection()

        try:
            self.conn = self.engine.connect()            
            if self.conn is not None:
                print("-I- Successful database connection")
        except Exception as e:
            print(f"-W- {str(e)}")

    def write_to_db(self,df,name):
        df.to_sql(name,self.conn, if_exists = 'replace')

    def read_db(self,table):
        df = pd.read_sql(table,self.conn)
        return df

    def show_tables(self):
        df = pd.read_sql("SHOW TABLES",self.conn)
        return df

    
if __name__ == "__main__":
    db = Database()
    print(db.show_tables())
    print(db.read_db('Sunshine'))