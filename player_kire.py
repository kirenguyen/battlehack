import battlecode
import time
import random


# define helper functions here
def nearest_glass_state(state, entity):
    nearest_statue = None
    nearest_dist = 10000
    for other_entity in state.get_entities(entity_type=battlecode.Entity.STATUE):
        if (entity == other_entity):
            continue
        dist = entity.location.adjacent_distance_to(other_entity.location)
        if (dist < nearest_dist):
            dist = nearest_dist
            nearest_statue = other_entity

    return nearest_statue


class Robot():
    def __init__(self, bot):
        # self.state = state
        # self.entity = entity

        # bot variables
        self.bot = bot
        self.loc = bot.location
        self.hp = bot.hp
        self.cooldown_time = 0
        self.last_loc = None
        self.loc_traveled =[]

        # role, defined by: (command, location to execute command)
        self.role = (None, None)

    def update_bot(self, bot):
        self.bot = bot
        self.loc = bot.location
        self.hp = bot.hp

    def update_role(self, new_role, loc=None):
        self.role = (new_role, loc)

    def return_loc(self):
        return self.loc

    def return_role(self):
        return self.role

    def calc_distance(self, loc):
        '''
        calculates distance from robot to a certain location
        :param loc: location object
        :return: distance
        '''

        return ((self.loc.x - loc.x) ** 2 + (self.loc.y - loc.y) ** 2) ** (1 / 2)

    def go_to_loc(self, loc):
        x_dir = 0
        y_dir = 0

        self.loc_traveled.append(self.loc)

        temp_old_loc = self.loc

        x = self.loc.x
        y = self.loc.y

        if self.loc.x < loc[0]:
            x_dir = 1
        elif self.loc.x > loc[0]:
            x_dir = -1

        if self.loc.y < loc[1]:
            y_dir = 1

        elif self.loc.x > loc[1]:
            y_dir = -1

        if x_dir != 0 or y_dir != 0:
            #direction = battlecode.Direction.from_delta(x_dir, y_dir)
            #print(self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)))
            if self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)) and (x+x_dir, y +y_dir) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, y_dir))
                print("move1")
            #try y direction
            elif self.bot.can_move(battlecode.Direction.from_delta(0, y_dir)) and (x, y +y_dir) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(0, y_dir))
                print("move2")
            #try x direction
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, 0)) and (x+x_dir, y) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, 0))
                print("move3")
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(-x_dir, y_dir)) and (x-x_dir, y +y_dir) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(-x_dir, y_dir))
                print("move4")
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, -y_dir)) and (x+x_dir, y-y_dir) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, -y_dir))
                print("move5")
            #try y direction
            elif self.bot.can_move(battlecode.Direction.from_delta(0, -y_dir)) and (x, y-y_dir) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(0, -y_dir))
                print("move6")
            #try x direction
            elif self.bot.can_move(battlecode.Direction.from_delta(-x_dir, 0)) and (x-x_dir, y) not in self.loc_traveled:
                self.bot.queue_move(battlecode.Direction.from_delta(-x_dir, 0))
                print("move7")
            else:
                self.bot.can_move(battlecode.Direction.from_delta(-x_dir, -y_dir))


    def attack_loc(self, loc):

        # calculate distance from self to target location
        if self.calc_distance(loc) > 7:
            # if it is > 7, move closer, otherwise, begin attack sequence
            self.go_to_loc(loc)

        else:
            # attack sequence, first need to get adjacent players
            near_entities = self.bot.entities_within_euclidean_distance(1)
            if len(near_entities) != 0:
                # if there is an adjacent player, throw it, otherwise wait??
                for entity in near_entities:  # entity is entity to be thrown

                    if self.bot.can_pickup(entity):
                        # pickup the entity
                        self.bot.queue_pickup(entity)
                        # throw entity in direction of loc
                        throw_dir = self.loc.direction_to(entity.location)
                        self.bot.queue_throw(throw_dir)
                        break

                # at end of attack seq, set role to None, job is complete
                self.role = None

            else:
                # there are no nearby bots, wait for the follower bot to catch up?
                pass

    def build_loc(self, loc):

        # check if bot is at builder loc
        if abs(loc.x - self.loc.x) <= 1 and abs(loc.y - self.loc.y) <= 1:

            # execute build sequence
            build_dir = self.loc.direction_to(loc)

            # set cooldown_timer to 10
            self.cooldown_time = 10

            # build
            self.bot.queue_build(build_dir)

            # set state to coolingdown
            self.role = ('cooldown', self.loc)

        else:
            self.go_to_loc(loc)

    def brain(self):
        '''
        brain looks at the role that each robot is assigned to and ensures that that role
        is executed properly
        :return:
        '''

        # make sure that there is no cooldown time
        if self.cooldown_time == 0:

            if self.role[0] == 'attack':
                self.attack_loc(self.role[1])

            elif self.role[0] == 'build':
                self.build_loc(self.role[1])

            elif self.role[0] == 'follow':
                self.go_to_loc(self.role[1])

        else:
            # subtract from cooldown time until it hits zero
            self.cooldown_time -= 1

            if self.cooldown_time == 0:
                self.role = (None, None)


def find_nearest_enemy(state, entity, location):
    '''
    finds the nearest enemy to a given location
    :param state:
    :param entity:
    :param location: location object
    :return: distance_from_loc, nearest_enemy_location
    '''
    our_x = location.x
    our_y = location.y

    best_dist, best_loc = None, None

    for enemies in state.get_entities(team=state.other_team):
        enemy_x = enemies.location.x
        enemy_y = enemies.location.y

        dist = ((our_x - enemy_x) ** 2 + (our_y - enemy_y) ** 2) ** (1 / 2)

        if best_loc == None or dist < best_dist:
            best_dist = dist
            best_loc = enemies.location

    return best_dist, best_loc


def assign_bots(state, entity, d):
    '''
    map a number to each bot so that it becomes hashable
    :param d: our_bots
    :return: the dictionary object
    '''

    i = 0
    for bot in state.get_entities(team=state.my_team):
        d[i] = {"bot": bot, "role": None}
        i += 1

    return d


def assign_roles(d, bot, role):
    '''
    assigns a role to a robot, if robot not in role_fn, adds to role_fn
    :param d: role_fn role dictionary
    :param bot: the bot
    :param role:
    :return:
    '''
    pass


if __name__ == "__main__":
    # Start a game
    game = battlecode.Game('KIRE, NOT KENNY!!!')

    start = time.clock()

    our_bots = {}

    for state in game.turns():
        entity_loc = []
        for entity in state.get_entities():
            entity_loc.append(entity.location)

        # check all robots exist, else add them into the dictionary our_bots
        for entity in state.get_entities(team=state.my_team):
            if entity.id not in our_bots:
                our_bots[entity.id] = Robot(entity)
            else:
                our_bots[entity.id].update_bot(entity)

        #TODO: location change
        for bot in our_bots.values():
            bot.go_to_loc((0,0))

        # Your Code will run within this loop
        for entity in state.get_entities(team=state.my_team):
            # This line gets all the bots on your team

            '''
            target all other robots
            '''


            # if(state.turn % 10 == 0):
            #     for direction in battlecode.Direction.directions():
            #         if entity.can_build(direction):
            #             entity.queue_build(direction)
            #
            # my_location = entity.location
            # near_entites = entity.entities_within_euclidean_distance(1.9)
            # near_entites = list(filter(lambda x: x.can_be_picked, near_entites))
            #
            # for pickup_entity in near_entites:
            #     assert entity.location.is_adjacent(pickup_entity.location)
            #     if entity.can_pickup(pickup_entity):
            #         entity.queue_pickup(pickup_entity)
            #
            # statue = nearest_glass_state(state, entity)
            # if(statue != None):
            #     direction = entity.location.direction_to(statue.location)
            #     if entity.can_throw(direction):
            #         entity.queue_throw(direction)
            #
            # for direction in battlecode.Direction.directions():
            #     if entity.can_move(direction):
            #         entity.queue_move(direction)

    end = time.clock()
    print('clock time: ' + str(end - start))
    print('per round: ' + str((end - start) / 1000))