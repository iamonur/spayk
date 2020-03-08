import os


class ParserClass:

    def __init__(self):

        self.output_file = "tempfile.txt"

    def __get_trail_out(self, executable, trail):

        os.system("{} -r -S {} > {} ".format(executable, trail, self.output_file))

    def __parse_trail_out(self):

        file = open(self.output_file)
        lines = file.readlines()
        file.close()

        li = []
        last = ""

        for line in lines:

            spl = line.split()

            if spl[0] == "pan:1:" and spl[1] == "assertion" and spl[2] == "violated": #end of trail file
                elem = ["WIN", spl[-1][:-1]]
                li.append(elem)
                return li

            elif spl[1] == "-":

                if spl[0] == last: # Need a skip before

                    if spl[0] == "Opponent":
                        add = ["Avatar", "Skip"]

                    else:
                        add = ["Opponent", "Skip"]

                    li.append(add)

                elem = [spl[0], spl[-1]]
                last = spl[0]
                li.append(elem)

            elif spl[0] == "MSC:":
                continue

            else:
                elem = ["LOSE", "-1"]
                return li

        #os.system("rm {}".format())

    def __parse_moves(self, moves):

        if len(moves) == 0:
            return None, None

        if moves[-1][0] is "LOSE":
            return None, None

        avatar = []
        opponent = []

        for move in moves:

            if move[0] == "Avatar":
                avatar.append(move[1])

            elif move[0] == "Opponent":
                opponent.append(move[1])

            else:
                return avatar, opponent

        return avatar, opponent



    def main_functionality(self):
        self.__get_trail_out("./temp.out", "temp.pml.trail")
        av, op = self.__parse_moves(self.__parse_trail_out())
        if av is None:
            raise ValueError("Avatar cannot win the game!")
        return av


if __name__ == "__main__":
    p = ParserClass()
    print (p.main_functionality())
