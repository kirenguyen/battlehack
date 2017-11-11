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
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, -y_dir)) and (x-x_dir, y-y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, -y_dir))
            elif self.bot.can_move(battlecode.Direction.from_delta(-1, y_dir)) and (x-1, y+y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(-1, y_dir))
            elif self.bot.can_move(battlecode.Direction.from_delta(1, y_dir)) and (x+1, y+y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(1, y_dir))

        elif x_dir != 0 and y_dir == 0:
            if self.bot.can_move(battlecode.Direction.from_delta(x_dir, y_dir)) and (x+x_dir, y +y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, y_dir))
            #try another direction
            elif self.bot.can_move(battlecode.Direction.from_delta(-x_dir, y_dir)) and (x-x_dir, y+y_dir) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(-x_dir, y_dir))
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, 1)) and (x+x_dir, y+1) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, 1))
            elif self.bot.can_move(battlecode.Direction.from_delta(x_dir, -1)) and (x+x_dir, y-1) != self.last_loc:
                self.bot.queue_move(battlecode.Direction.from_delta(x_dir, -1))

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


def analyze_map(state, num_buildings, num_attacks):
   '''
   takes the state of the map, number of towers to be built, number of towers to attack
   uses heuristic to determine best location to build in, best location to attack
   :param state: state of the map
   :param num_buildings: equal to # of builder bots
   :param num_attacks: equal to remaining bots / 2 (one attacker, one follower per tower)
   :return: dictionary giving list of top building locations, top attacking locations
   '''

   #list that holds all of map's sectors
   sectors = []
   x = 0
   y = 0

   #while loops iterate through and build a list of all of map's sectors
   while x < state.map.width:
       while y < state.map.height:
           item = state.map.sector_at(x, y)
           sectors.append(item)
           y += 5
       x += 5
       y = 0

   #list that holds all of the unclaimed sectors
   available_sectors = []

   #iterates through sectors, adding sectors that don't belong to us or them to the "unclaimed" list
   for sector in sectors:
       if ((sector.team != state.enemy_team) and (sector.team != state.my_team)):
           available_sectors.append(sector)

   #list that holds locations where we want to build towers
   desired_buildings = []
   entities = state.get_entities()
   entity_locations = []
   for entity in entities:
       entity_locations.append(entity.location)

   #if there are fewer available spots than we want, return all of the available spots
   if num_buildings >= len(available_sectors):
       for y in available_sectors:
           x = 0
           y = 0
           i = 0
           while ((i.top_left.x - x), (i.top_left.y - y)) in entity_locations and (x < 5 and y < 5):
               if i < 5:
                   x += 1
                   i += 1
               else:
                   y += 1
                   i = 0
                   x = 0
           desired_buildings.append((i.top_left.x - x), (i.top_left.y - y))

   #else, return only as many locations as we want
   else:
       while len(desired_buildings) < num_buildings:
           for y in available_sectors:
               x = 0
               y = 0
               i = 0
               while ((i.top_left.x - x), (i.top_left.y - y)) in entity_locations and (x < 5 and y < 5):
                   if i < 5:
                       x += 1
                       i += 1
                   else:
                       y += 1
                       i = 0
                       x = 0
               desired_buildings.append((i.top_left.x - x), (i.top_left.y - y))

   #list that holds the distances from our first robot's initial location and all of the enemy towers
   distances = []

   #list of all of the enemy's towers - for loop below calculates distances
   enemy_towers = state.get_entities(entity_type=battlecode.Entity.STATUE, team=state.enemy_team)
   for tower in enemy_towers:
       distance = first_location.distance_to(tower.location)
       distances.append(distance)

   #dictionary that maps enemy towers to their distance from our initial location
   tower_distances = {}
   for i in range(len(distances)):
       tower_distances[distances[i]] = enemy_towers[i]

   #sorts distances from lowest to highest
   sorted_distances = sorted(tower_distances.keys)

   #list that holds towers to attack, sorted by their distance from home base
   ordered_tower_locations = []
   for i in sorted_distances:
       ordered_tower_locations.append(tower_distances[i].location)

   #constructs and returns a dictionary with an ordered list of locations to build and locations to attack
   dictionary = {"build_on":desired_buildings, "attack":ordered_tower_locations}
   return(dictionary)

if __name__ == "__main__":
    # Start a game
    game = battlecode.Game('Kire is Dead')

    start = time.clock()

    our_bots = {}

    important_locations = {}

    for state in game.turns():

        hedges_loc = []

        #TODO: Elaine's random target generator --- switch with McCoy's list location
        max_x = state.map.width
        max_y = state.map.height

        entity_loc = {}

        for entity in state.get_entities(team=0):
            if entity.is_hedge:
                hedges_loc.append(entity.location)


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
            if entity.id < lowest_id:
                lowest_id = entity.id
        first_robot = our_bots[lowest_id]
        first_location = first_robot.loc

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








                #TODO: ELaine's random location generator part 2, switch with McCoy's location generator
                target_coord = (random.randrange(1,max_x-1), random.randrange(1,max_y-1))
                if target_coord not in hedges_loc and target_coord != our_bots[entity.id].loc:
                    target = battlecode.Location(target_coord)
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