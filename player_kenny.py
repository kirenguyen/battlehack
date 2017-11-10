import battlecode
import time
import random

#Start a game
game = battlecode.Game('testplayer')

start = time.clock()

our_bots = {}

#define helper functions here
def nearest_glass_state(state, entity):
    nearest_statue = None
    nearest_dist = 10000
    for other_entity in state.get_entities(entity_type=battlecode.Entity.STATUE):
        if(entity == other_entity):
            continue
        dist = entity.location.adjacent_distance_to(other_entity.location)
        if(dist< nearest_dist):
            dist = nearest_dist
            nearest_statue = other_entity

    return nearest_statue

class Robot():

    def __init__(self, state, entity, bot):
        self.state = state
        self.entity = entity

        # bot variables
        self.bot = bot
        self.loc = bot.location
        self.hp = bot.hp
        self.cooldown_end = None

        # role
        self.role = None

    def update_bot(self, bot):
        self.bot = bot
        self.loc = bot.location
        self.hp = bot.hp

    def update_role(self, new_role):
        self.role = new_role

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

        if self.loc.x < loc:
            x_dir = 1
        elif self.loc.x > loc:
            x_dir = -1

        if self.loc.y < loc:
            y_dir = 1
        elif self.loc.x > loc:
            y_dir = -1

        if x_dir != 0 and y_dir != 0:
            direction = battlecode.Direction(x_dir, y_dir)
            self.entity.queue_move(direction)

    def attack_loc(self, loc):

        # calculate distance from self to target location
        if self.calc_distance(loc) > 7:
            # if it is > 7, move closer, otherwise, begin attack sequence
            self.go_to_loc(loc)

        else:
            # attack sequence, first need to get adjacent players





            # if there is an adjacent player, throw it, otherwise wait??







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

        dist = ((our_x - enemy_x)**2 + (our_y - enemy_y)**2)**(1/2)

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
        d[i] = {"bot": bot, "role" : None}
        i+=1

    return d




def assign_roles(d, bot, role):
    '''
    assigns a role to a robot, if robot not in role_fn, adds to role_fn
    :param d: role_fn role dictionary
    :param bot: the bot
    :param role:
    :return:
    '''
    if bot in d:






for state in game.turns():
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
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
