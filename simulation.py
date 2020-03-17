import player
import parser
import spinner
import recorder
import random
import sqlite3 #TODO: REMOVE DATABASE AND MOVE IT TO THE WRAPPER

def bubblesort(list):

    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx][2]>list[idx+1][2]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp
    return list


class SimClass:
    def __init__(self):
        self.__record_init()

    def __spin_job(self):
        self.spin = spinner.SpinClass()
        self.spin.generate_compile_spin()
        return self.spin.mazify()

    def __parse_job(self):
        self.parse = parser.ParserClass()
        asd = self.parse.main_functionality()
        #print(asd)
        return self.parse.main_functionality()

    def __play_init(self):
        self.game = player.skeleton_game.format(immovable="", mover="", chaser=player.chaser_str)
        self.player = player.GameClass(actions_list=self.moves, game_desc=self.game, level_desc=self.maze)

    def __play_perform(self):
        return self.player.play()

    def __record_init(self):
        self.db = recorder.DBWrapper()

    def __record_job(self, winnable=True, outcome=True):
        #self.db.submit_gameplay(self.maze, self.game, winnable, self.moves, outcome)
        pass
    def main_functionality(self): #is a chain reaction of model checking, parsing, playing and recording.
        self.maze = self.__spin_job()

        try:
            self.moves = self.__parse_job()
        except ValueError: #If we cannot win, report but continue.
            self.__record_job(winnable=False, outcome=False)
            return
            #self.simulate()

        self.__play_init()

        count = 0
        while count < 100:
            count += 1
            try:
                if self.__play_perform() > 0:
                    self.__record_job(outcome=True)
                    return
                else:
                    self.__record_job(outcome=False)
            except ValueError:
                print("asd")


class NewGeneticSimClass:
    def __init__(self, numElites=50, database=None):
        self.numElites = numElites
        self.numPopulation = 2*numElites
        self.activeGeneration = []

        if database is None: #Initialize the default database
            self.dbname = "onur.db"
            self.__init_connect_db()
        else:
            self.dbname = database
            self.__connect_db()

    def __connect_db(self):
        self.connection = recorder.EliteSelector(self.dbname)

    def __init_connect_db(self):
        pass

    def generate_a_generation(self):
        if len(self.activeGeneration) is 0:
            while len(self.activeGeneration) < self.numPopulation:
                print(len(self.activeGeneration))
                self._level_gen_no_parents()

        elif len(self.activeGeneration) is self.numElites:
            for index, _ in enumerate(self.activeGeneration):
                self._level_gen_with_parents(self.activeGeneration[index], self.activeGeneration[self.numElites - 1 - index])
                if len(self.activeGeneration) is self.numPopulation:
                    return
        elif len(self.activeGeneration) is self.numPopulation:
            self.activeGeneration = self._step_a_generation()
            self.generate_a_generation()

    def _level_gen_no_parents(self):
        s = spinner.NewGenomeBinarySpinClass()
        s.generate_compile_spin()
        self.activeGeneration.append([s.x_genome, s.y_genome, s.av_genome, s.op_genome, s.po_genome, 0])

    def _level_gen_with_parents(self, parent1, parent2, mutationChance=0.2):
        if random.random() > mutationChance: #This is not that cool of a crossing.
            self.activeGeneration.append([parent1[0], parent2[1], [parent1[2][0], parent2[2][1]], [parent1[3][0], parent2[3][1]], [parent1[4][0], parent2[4][1]], 0])
        else:
            self.activeGeneration.append(self._level_gen_with_parents_mutated(parent1, parent2))

    def _level_gen_with_parents_mutated(self, parent1, parent2):
        cromosome = random.randint(0,7)
        ret = [parent1[0], parent2[1], [parent1[2][0], parent2[2][1]], [parent1[3][0], parent2[3][1]], [parent1[4][0], parent2[4][1]], 0]

        if random.random() > 0.5:
            if ret[0][cromosome] is 1:
                ret[0][cromosome] = 0
            else:
                ret[0][cromosome] = 1
        else:
            if ret[1][cromosome] is 1:
                ret[1][cromosome] = 0
            else:
                ret[1][cromosome] = 1

        return ret

    def _step_a_generation(self):
        if len(self.activeGeneration) != self.numPopulation: # Dude let this propagate. Something is wrong here.
            raise ValueError("An early stepping occurred!")
        return self._checkLevels()

    def _checkLevels(self):
        asd = []
        for level in self.activeGeneration:
            asd.append([level[0], level[1], level[2], level[3], level[4], self._check_level(level[0], level[1], level[2], level[3], level[4])])
        asd = bubblesort(asd)
        return asd[self.numElites:]

    def _check_level(self, genome_x, genome_y, genome_av, genome_op, genome_po):
        g = spinner.NewGenomeBinarySpinClass(genome_x, genome_y, genome_av, genome_op, genome_po)
        g.generate_compile_spin()
        p = parser.ParserClass()

        try:
            avatar_moves = p.main_functionality()
        except ValueError:
            return -1000

        game = player.skeleton_game.format(immovable="", mover="", chaser=player.chaser_str)
        pp = player.GameClass(actions_list=avatar_moves, game_desc=game, level_desc=g.mazify())

        fitness = len(avatar_moves) * pp.play()

        query = "INSERT INTO gengame (genome_x, genome_y, genome_av, genome_op, genome_po, level, fitness, moves) VALUES ('{}','{}','{}','{}','{}','{}',{},'{}')".format(genome_x, genome_y, genome_av, genome_op, genome_po, g.mazify(), fitness, avatar_moves)
        print(query)
        con = sqlite3.connect(self.dbname)
        con.isolation_level = None
        cur = con.cursor()
        cur.execute(query)
        return fitness


class GeneticSimClass:

    def __init__(self, simType="Elitistic", databaseLoc=":memory:", numElites=50):
        self.simType = simType
        self.databaseLoc = databaseLoc
        self.numElites = numElites
        self.numPopulation = 2*self.numElites
        self.activeGeneration = []

    def _connect_db(self):
        self.connection = recorder.EliteSelector(databaseLoc)

    def generate_a_generation(self):

        if len(self.activeGeneration) is 0:
            while len(self.activeGeneration) < self.numPopulation:
                #print(2)
                self._level_gen_no_parents()

        elif len(self.activeGeneration) is self.numElites:
            #while len(self.activeGeneration) < self.numPopulation:
            #print(self.activeGeneration)
            for index, _ in enumerate(self.activeGeneration):
                self._level_gen_with_parents(self.activeGeneration[index], self.activeGeneration[self.numElites - 1 - index])
                if len(self.activeGeneration) is self.numPopulation:
                    return

        elif len(self.activeGeneration) is self.numPopulation:
            #print(self.activeGeneration)
            self.activeGeneration = self._step_a_generation()
            self.generate_a_generation()

    def _step_a_generation(self):
        if len(self.activeGeneration) < self.numPopulation:
            raise ValueError("Should not be at the stepping place. Population is wrong!")
        return self.checkLevels()

    def checkLevels(self):
        asd = []
        for level in self.activeGeneration:
            asd.append([level[0], level[1], self._check_level(level[0], level[1])])
        asd = bubblesort(asd)
        #print(asd)
        #print(asd[0:self.numElites])
        return asd[self.numElites:]

    def _check_level(self, genomeX, genomeY):
        g = spinner.GenomeSpinClass(genomeX, genomeY)
        g.generate_compile_spin()

        p = parser.ParserClass()
        try:
            avatar_moves = p.main_functionality()
        except ValueError:
            return -1000

        game = player.skeleton_game.format(immovable="", mover="", chaser=player.chaser_str)
        pp = player.GameClass(actions_list=avatar_moves, game_desc=game, level_desc=g.mazify())
        fitness = len(avatar_moves) * pp.play()
        query = "INSERT INTO gengame (genome_x, genome_y, level, fitness, moves) VALUES ({}, {}, '{}', {}, '{}')".format(de_serialize_gene(genomeX), de_serialize_gene(genomeY), g.mazify(), fitness, avatar_moves)
        con = sqlite3.connect("gen.db")
        con.isolation_level = None
        cur = con.cursor()
        cur.execute(query)
        return fitness  # A More realistic fitness function here

    def _level_gen_no_parents(self):
        spinning = spinner.GenomeSpinClass()
        spinning.generate_compile_spin()
        self.activeGeneration.append([spinning.genomeX, spinning.genomeY, 0])

    def _level_gen_with_parents(self, parent1=None, parent2=None, mutationChance=0.2):
        ###### A REAL GENETIC EVOLUTION ALGORITHM HERE!!!!!!!!!
        if random.random() > mutationChance:
            self.activeGeneration.append([parent1[0], parent2[1], 0])
        else:
            self.activeGeneration.append(self._level_gen_with_parents_mutated(parent1, parent2))

    def _level_gen_with_parents_mutated(self, parent1, parent2):
        cromosome = random.randint(0,7)
        ret = [parent1[0], parent2[1], 0]
        if random.random() > 0.5: #gene1
            if ret[0][cromosome] is 1:
                ret[0][cromosome] = 0
            else:
                ret[0][cromosome] = 1
        else: # gene2
            if ret[1][cromosome] is 1:
                ret[1][cromosome] = 0
            else:
                ret[1][cromosome] = 1

        return ret

def de_serialize_gene(gene):
    return (gene[7] + 2*(gene[6] + 2*(gene[5] + 2*(gene[4] + 2*(gene[3] + 2*(gene[2] + 2*(gene[1] + 2*gene[0])))))))

def printall_generation(gen):
    print("Gen_start")
    sum = 0
    for member in gen:
        print("---")
        print(de_serialize_gene(member[0]))
        print(de_serialize_gene(member[1]))
        print(member[2])
        sum += member[2]
    print(sum/len(gen))
    print("Gen_end")

if __name__ == "__main__":
#    query = """CREATE TABLE gengame (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    genome_x text NOT NULL,
#    genome_y text NOT NULL,
#    genome_av text NOT NULL,
#    genome_op text NOT NULL,
#    genome_po text NOT NULL,
#    level text NOT NULL,
#    fitness INTEGER DEFAULT 0,
#    moves text NOT NULL);"""
#    con = sqlite3.connect("onur.db")
#    cur = con.cursor()
#    cur.execute(query)
    #s = GeneticSimClass()
    #for i in range(1,100):
    #    s.generate_a_generation()
    #    printall_generation(bubblesort(s.activeGeneration))
    s = NewGeneticSimClass()
    for i in range(1,10000):

        s.generate_a_generation()
