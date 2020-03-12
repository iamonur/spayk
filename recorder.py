
import sqlite3

class DBWrapper:
    def __init__(self, dbname="asd.db"):
        self.connection = sqlite3.connect(dbname)
        self.db = self.connection.cursor()

    def __register_game(self, level, game, moves, winnable):
        query = "SELECT COUNT(*) FROM game WHERE level='{}' AND desc='{}'".format(level, game)
        self.db.execute(query)
        res = self.db.fetchall()[0][0]

        if res is 1:
            query = "SELECT id FROM game WHERE level='{}' AND desc='{}'".format(level, game)
            self.db.execute(query)
            res = self.db.fetchall()[0][0]
            return res
        elif res is 0:
            query = "INSERT INTO game (level, desc, iswinnable, spin_moves, spin_length) VALUES ('{}','{}','{}','{}',{})".format(level, game, winnable, moves, len(moves))
            self.db.execute(query)
            self.connection.commit()

            query = "SELECT id FROM game WHERE level='{}' AND desc='{}'".format(level, game)
            self.db.execute(query)
            res = self.db.fetchall()[0][0]
            return res
        else:
            raise "Important DB Accident that needs attention. Let execution stop and this exception propagate."

    def submit_gameplay(self, level, game, moves, winnable=True,  outcome=True):
        id = self.__register_game(level, game, winnable, moves)
        query = "INSERT INTO gameplay (id, result) VALUES ({},'{}')".format(id, outcome)
        self.db.execute(query)

class EliteSelector:
    def __init__(self, dbname="genetic.db"):
        self.connection = sqlite3.connect(dbname)
        self.db = self.connection.cursor()

    def get_elites(self, limit):
        query = "SELECT genome_x, genome_y, avatar, opponent, portal FROM levels ORDER BY fitness LIMIT {}".format(limit)


    def initialize_database(self):
        #Initialize levels
        query = """CREATE TABLE levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genome_x INTEGER NOT NULL,
            genome_y INTEGER NOT NULL,
            avatar text NOT NULL,
            opponent text NOT NULL,
            portal text NOT NULL,
            moves text NOT NULL,
            winnable text NOT NULL,
            wins INTEGER DEFAULT 0,
            loses INTEGER DEFAULT 0,
            fitness FLOAT);"""
        #Initialize Gameplays
        query = """CREATE TABLE gameplays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            g_id INTEGER NOT NULL,
            result text NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (g_id) REFERENCES game (id));"""
        #Initialize triggers
        #T-1: update wins-loses
        query = """CREATE TRIGGER update_w AFTER INSERT ON gameplays
        WHEN new.result == 'True'
        BEGIN
            UPDATE levels SET wins=wins+1 WHERE id=new.g_id
        END;"""
        query = """CREATE TRIGGER update_l AFTER INSERT ON gameplays
        WHEN new.result == 'False'
        BEGIN
            UPDATE levels SET loses=loses+1 WHERE id=new.g_id
        END;"""
        #T-2: update fitness (Not sure but probably.) It will be 0-infinity, not [0,1]
        query = """CREATE TRIGGER
        """

    def submit_gameplay(self, genomeX, genomeY, avatar, opponent, portal, moves, winnable, outcome):
        id = self.__register_level(genomeX, genomeY, avatar, opponent, portal, moves, winnable, outcome)
        query = "INSERT INTO gameplay (id, )"
    def __register_level(self, genomeX, genomeY, avatar, opponent, portal, moves):
        pass



class StubDBWrapper(DBWrapper): #Same class, but not query, just STDOUT.
    def __init__(self):
        print("A stub database connection!")

    def __register_game(self, level, game, winnable, moves):
        query = "INSERT INTO game BLAHBLAH"
        print(query)
        return "id"

    def submit_gameplay(self, level, game,  moves, winnable=True, outcome=True):
        id = self.__register_game(level, game, winnable, moves)
        query = "INSERT INTO gameplay (id, result) VALUES ({},{})".format(id, outcome)
        print(query)

if __name__ == "__main__":
    con = sqlite3.connect("gen.db")
    con.isolation_level = None
    cur = con.cursor()
    q = "SELECT COUNT(*) FROM gengame"
    query = "SELECT MAX(fitness) FROM gengame"
    q_max = "SELECT * FROM gengame WHERE fitness=(SELECT MAX(fitness) FROM gengame)"
#    q = "DROP TABLE IF EXISTS gengame;"
#    query = """CREATE TABLE gengame(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        genome_x INTEGER NOT NULL,
#        genome_y INTEGER NOT NULL,
#        level text NOT NULL,
#        fitness INTEGER NOT NULL,
#        moves text NOT NULL
#    );"""
    cur.execute(q)
    print("Number of guys: {}".format(cur.fetchall()))
    cur.execute(query)
    print("Maximum fitness: {}".format(cur.fetchall()))
    cur.execute(q_max)
    print("Best game:\n{}".format(cur.fetchall()))
    #print (cur.fetchall())



#    print ("Enter your SQL commands to execute in sqlite3.")
#    print ("Enter a blank line to exit.")

#    while True:
#        line = input()
#        if line == "":
#            break
#            buffer += line
#        if sqlite3.complete_statement(buffer):
#            try:
#                buffer = buffer.strip()
#                cur.execute(buffer)
#
#                if buffer.lstrip().upper().startswith("SELECT"):
#                    print (cur.fetchall())
#            except sqlite3.Error as e:
#                print ("An error occurred: {}".format(e.args[0]))
#            buffer = ""

    con.close()
#   I'M KEEPING TABLE QUERIES SINCE I MAY NEED THEM LATER
#   """CREATE TABLE game(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        level text NOT NULL,
#        desc text NOT NULL,
#        isWinnable text NOT NULL,
#        spin_moves text NOT NULL,
#        played INTEGER DEFAULT 0,
#        win INTEGER DEFAULT 0,
#        lose INTEGER DEFAULT 0,
#        spin_length INTEGER
#    );"""
#    """CREATE TABLE gengame(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        genome_x INTEGER NOT NULL,
#        genome_y INTEGER NOT NULL,
#        av_pos text NOT NULL,
#        po_pos text NOT NULL,
#        op_pos text NOT NULL,
#        fitness INTEGER NOT NULL,
#        moves text NOT NULL
#    );"""
#    """CREATE TABLE gameplay(
#        g_id INTEGER PRIMARY KEY AUTOINCREMENT,
#        id INTEGER NOT NULL,
#        result text NOT NULL,
#        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#        FOREIGN KEY (id) REFERENCES game (id)
#    );"""

    #cursor.execute(query)
