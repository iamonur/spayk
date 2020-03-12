gamefile = "tempgame.txt"
levelfile = "tempgame_levl0.txt"
import random
import copy
import os
from vgdl.core import Action
from vgdl.util.humanplay.human import RecordedController
import vgdl.interfaces.gym
import gym
import vgdl.ai

immovable_str = "\n        opponent > Immovable color=BLUE"
chaser_str = "\n        opponent > Chaser stype=avatar color=RED"
astar_chaser_str = "\n        opponent > AStarChaser stype=avatar color=RED"
mover_str = "\n            opponent > color=DARKBLUE"

skeleton_game = """
BasicGame
    SpriteSet
        goalportal > Immovable color=GREEN
        wall > Immovable color=BLACK
        floor > Immovable color=BROWN{immovable}{chaser}
        players > MovingAvatar
            avatar > alternate_keys=True{mover}
    TerminationSet
        SpriteCounter stype=goalportal limit=0 win=True
        SpriteCounter stype=opponent limit=0 win=False
    InteractionSet
        opponent goalportal > stepBack
        avatar wall > stepBack
        opponent wall > stepBack
        goalportal avatar > killSprite scoreChange=1
        opponent avatar > killSprite scoreChange=-1
    LevelMapping
        E > opponent floor
        G > goalportal
        A > avatar floor
        . > floor
"""

dummy_maze = """
wwwwwwww
wA.....w
w......w
w.G....w
w......w
w......w
w.....Ew
wwwwwwww
"""

dummy_actions = ['Skip', 'Skip', 'Skip', 'Skip', 'Skip', 'Skip', 'Skip'] #Wait only

class GameClass:
    def __init__(self, actions_list=None, game_desc=None, level_desc=None):

        if actions_list is None:
            print("WUT")
            self.actions = copy.deepcopy(dummy_actions)
        else:
            self.actions = actions_list

        if level_desc is None:
            self.level = dummy_maze
        else:
            self.level = level_desc

        if game_desc is None:
            self.game = skeleton_game.format(immovable="", mover="", chaser=chaser_str)
        else:
            self.game = game_desc

        self.__save_game_files()
        self.__register_environment(gamefile, levelfile, None, 32)
        #print(self.actions)
        self.__format_actions()
        #print(self.actions)
        self.__create_controller()

    def __register_environment(self, domain_file, level_file, observer=None, blocksize=None):
        from gym.envs.registration import register, registry
        level_name = '.'.join(os.path.basename(level_file).split('.')[:-1])
        self.env_name = 'vgdl_{}-{}-v0'.format(random.random() ,level_name)

        register(
            id=self.env_name,
            entry_point='vgdl.interfaces.gym:VGDLEnv',
            kwargs={
                'game_file': domain_file,
                'level_file': level_file,
                'block_size': blocksize,
                'obs_type': observer or 'features',
            },
            nondeterministic=True
        )

    def __format_actions(self):
        for i, action in enumerate(self.actions):
            if action == 'A':
                self.actions[i] = 0
            elif action == 'S':
                self.actions[i] = 3
            elif action == 'D':
                self.actions[i] = 1
            elif action == 'W':
                self.actions[i] = 2
            elif action == 'Skip':
                self.actions[i] = -1

    def __create_controller(self):

        self.controller = RecordedController(self.env_name, self.actions, fps=10)


    def __save_game_files(self):

        f = open(gamefile, 'w')
        f.write(self.game)
        f.close()

        f = open(levelfile, 'w')
        f.write(self.level)
        f.close()

    def play(self):
        self.controller.play()
        print(self.controller.cummulative_reward)
        return self.controller.cummulative_reward

if __name__ == "__main__":
    g = GameClass()
    print(g.play())
