import battlecode
import time
import random


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

def categorize_entities(state):
    hedges_loc = []
    my_lob = []
    my_glass = []
    opp_lob = []
    opp_glass = []
    for entity in state.get_entities(team=state.my_team):
        if entity.is_statue:
            my_glass.append(entity)
        if entity.is_thrower:
            my_lob.append(entity)

    for entity in state.get_entities(team=0):
        if entity.is_hedge:
            hedges_loc.append(entity.location)

    for entity in state.get_entities(team=state.other_team):
        if entity.is_statue:
            opp_glass.append(entity)
        if entity.is_thrower:
            opp_lob.append(entity)
    return [hedges_loc, my_lob, my_glass, opp_lob, opp_glass]

def check_targets(state, bot, entity_list):
    #creates a list of lists that holds all the entities that are in throwing direction of bot
    #an empty square is represented by None
    direction_change = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]
    targets = []
    for direction in direction_change:
        targ_list_dir = []
        #creates a list of all the objects within 7 sqares in the given direction
        for i in range(1,8):
            location = (bot.loc.x+direction[0]*i, bot.loc.y+direction[1]*i)
            if location in entity_list.keys:
                targ_list_dir.append(entity_list[location][0])
            else:
                targ_list_dir.append(None)
        targets.append(targ_list_dir)
    return targets

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

    def update_role(self, new_role, loc = None):
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

        if x_dir != 0 and y_dir != 0:
            #direction = battlecode.Direction.from_delta(x_dir, y_dir)
            #print(self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)))
            if self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)) and (x+x_dir, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, y_dir))
            #try y direction
            elif self.bot.can_move(battlecode.Direction.from_delta(0, y_dir)) and (x, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(0, y_dir))
            #try x direction
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, 0)) and (x+x_dir, y) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, 0))
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(-x_dir, y_dir)) and (x-x_dir, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(-x_dir, y_dir))
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, -y_dir)) and (x+x_dir, y-y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, -y_dir))
            #try y direction
            elif self.bot.can_move(battlecode.Direction.from_delta(0, -y_dir)) and (x, y-y_dir)!= self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(0, -y_dir))
            #try x direction
            elif self.bot.can_move(battlecode.Direction.from_delta(-x_dir, 0)) and (x-x_dir, y) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(-x_dir, 0))
            # else:
            #     self.bot.can_move(battlecode.Direction.from_delta(-x_dir, -y_dir))
        elif x_dir == 0 and y_dir != 0:
            if self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)) and (x+x_dir, y +y_dir)!= self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, y_dir))
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, -y_dir)) and (x-x_dir, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, -y_dir))

        elif x_dir != 0 and y_dir == 0:
            if self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)) and (x+x_dir, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, y_dir))
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(-x_dir, y_dir)) and (x-x_dir, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(-x_dir, y_dir))

        self.last_loc = temp_old_loc

    def attack_loc(self, loc):

        # calculate distance from self to target location
        if self.calc_distance(loc) >= 7:
            # if it is > 7, move closer, otherwise, begin attack sequence
            self.go_to_loc(loc)

        else:
            # attack sequence, first need to get adjacent players
            near_entities = [x for x in self.bot.entities_within_euclidean_distance(1)]
            if len(near_entities) != 0:
                # if there is an adjacent player, throw it, otherwise wait??
                for entity in near_entities: # entity is entity to be thrown

                    if self.bot.can_pickup(entity):
                        # pickup the entity
                        self.bot.queue_pickup(entity)
                        # throw entity in direction of loc
                        throw_dir = self.loc.direction_to(loc)
                        self.bot.queue_throw(throw_dir)
                        break

                # at end of attack seq, set role to None, job is complete
                print("REAWWWWR")
                self.role = (None, None)

            else:
                # there are no nearby bots, wait for the follower bot to catch up?
                pass

    def build_loc(self, loc):
        print(self.role)
        if self.cooldown_time == 0:
            # check if bot is at builder loc
            # if abs(loc[0] - self.loc[0]) <= 1 and abs(loc[1] - self.loc[1]) <= 1:
            print(self.loc[0], self.loc[1], "target:", (loc[0], loc[1]))
            if self.loc.is_adjacent(loc):

                # execute build sequence
                build_dir = self.loc.direction_to(loc)

                # set cooldown_timer to 10
                self.cooldown_time = 10

                # build
                if self.bot.can_build(build_dir):
                    self.bot.queue_build(build_dir)

                # set state to coolingdown
                self.role = ('cooldown', self.loc)
                print(self.role)

                print("already built")

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

            # print(self.role)
            # print("location", self.loc)


            if self.role[0] == 'attack':
                self.attack_loc(self.role[1])

            elif self.role[0] == 'build':
                self.build_loc(self.role[1])

            elif self.role[0] == 'follow':
                self.go_to_loc(self.role[1])

        else:
            # subtract from cooldown time until it hits zero
            if self.cooldown_time > 0:
                self.cooldown_time -= 1
                print(self.cooldown_time)
            else:
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
    pass




if __name__ == "__main__":
    # Start a game
    game = battlecode.Game('Pusheen')

    start = time.clock()

    our_bots = {}

    important_locations = {}

    for state in game.turns():
        max_x = state.map.width
        max_y = state.map.height
        entity_loc = {}
        for entity in state.get_entities():
            if entity.location not in entity_loc.keys():
                entity_loc[entity.location] = [entity]
            else:
                entity_loc[entity.location].append(entity)

        # check all robots exist, else add them into the dictionary our_bots
        for entity in state.get_entities(entity_type='thrower',team=state.my_team):
            if entity.id not in our_bots: #and entity.is_thrower:
                our_bots[entity.id] = Robot(entity)
            else:
                our_bots[entity.id].update_bot(entity)

        # identify locations of towers
        statue_list = []
        for enemy in state.get_entities(team=state.other_team):
            if enemy.is_statue:
                statue_list.append(enemy)


        # Your Code will run within this loop
        for entity in state.get_entities(entity_type='thrower', team=state.my_team):
            # This line gets all the bots on your team

            robot_class = our_bots[entity.id]

            if our_bots[entity.id].return_role()[0] == None:
                print("henloooo")

                target = battlecode.Location(random.randrange(1,max_x), random.randrange(1,max_y))
                if our_bots[entity.id].cooldown_time == 0:
                    our_bots[entity.id].update_role('build', target)
                    # our_bots[entity.id].cooldown_time = 10



            robot_class.brain()


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