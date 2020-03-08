import player
import parser
import spinner
import recorder

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
        return self.parse.main_functionality()

    def __play_init(self):
        self.game = player.skeleton_game.format(immovable="", mover="", chaser=player.chaser_str)
        self.player = player.GameClass(actions_list=self.moves, game_desc=self.game, level_desc=self.maze)

    def __play_perform(self):
        return self.player.play()

    def __record_init(self):
        self.db = recorder.DBWrapper()

    def __record_job(self, winnable=True, outcome=True):
        self.db.submit_gameplay(self.maze, self.game, winnable, self.moves, outcome)

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

            if self.__play_perform() > 0:
                self.__record_job(outcome=True)
                return
            else:
                self.__record_job(outcome=False)



class GeneticSimClass:

    def __init__(self, simType="Elitistic", databaseLoc=":memory:", numElites=4):
        # If no database is given, in-RAM db will be used, this is not nice to have btw.
        # If no simulation type is given, an elitistic simulation will be performed.
        # If no numElites is given, it is 50. numPopulation is 2*numElites no matter what.
        self.simType = simType
        self.databaseLoc = databaseLoc
        self.numElites = numElites
        self.numPopulation = 2*self.numElites
        self.activeGeneration = []
        print(1)

    def _connect_db(self):
        self.connection = recorder.EliteSelector(databaseLoc)

    def generate_a_generation(self):

        if len(self.activeGeneration) is 0:
            while len(self.activeGeneration) < self.numPopulation:
                print(2)
                self._level_gen_no_parents()

        elif len(self.activeGeneration) is self.numElites:
            #while len(self.activeGeneration) < self.numPopulation:
            for index in enumerate(self.activeGeneration):
                self._level_gen_with_parents(self.activeGeneration[index], self.activeGeneration[49 - index])
                if len(self.activeGeneration) is self.numPopulation:
                    return

        elif len(self.activeGeneration) is self.numPopulation:
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
        return asd[0:50]


    def _check_level(self, genomeX, genomeY):
        g = spinner.GenomeSpinClass(genomeX, genomeY)
        g.generate_compile_spin()

        p = parser.ParserClass()
        avatar_moves = p.main_functionality()

        game = player.skeleton_game.format(immovable="", mover="", chaser=player.chaser_str)
        pp = player.GameClass(actions_list=avatar_moves, game_desc=game, level_desc=g.mazify())

        return len(avatar_moves) * pp.play()


    def _level_gen_no_parents(self):
        spinning = spinner.GenomeSpinClass()
        spinning.generate_compile_spin()
        self.activeGeneration.append([spinning.genomeX, spinning.genomeY, 0])

    def _level_gen_with_parents(self, parent1=None, parent2=None, mutationChance=0.2):
        ######EVOLUTIONARY ALGORITHM HERE!!!!!!!!!
        self.activeGeneration.append(parent1)
        return parent1 #TODO: REMOVE!!


if __name__ == "__main__":
    s = GeneticSimClass()
    s.generate_a_generation()
    s.generate_a_generation()
