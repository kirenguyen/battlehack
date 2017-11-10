import battlecode
import time
import random

#Start a game
game = battlecode.Game('Pusheen')

start = time.clock()

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

for state in game.turns():
    # Your Code will run within this loop
    '''
    lists = categorize_entities(state)
    hedges_loc = lists[0]
    my_lob = lists[1]
    my_glass = lists[2]
    opp_lob = lists[3]
    opp_glass = lists[4]
    '''
'''
    sectors = state.map._sectors

    my_glass = []
    my_lob = []
    opp_lob = []
    opp_glass = []
    for sector in sectors.values():
        if sector.team != state.my_team:
            for entity in sector.entities_in_sector():
                if entity.team == state.my_team:
                    if entity.is_statue:
                        my_glass.append(entity)
                    if entity.is_thrower:
                        my_lob.append(entity)
                elif entity.team == state.other_team:
                    if entity.is_statue:
                        opp_glass.append(entity)
                    if entity.is_thrower:
                        opp_lob.append(entity)
            if opp_glass != []:
                for glass in opp_glass:
                    for robo in glass.entities_within_euclidean_distance(5, True, my_lob):
                        location = robo.location
                        if robo.can_throw(location.direction_to(glass.location)):
                            robo.queue_throw(location.direction_to(glass.location))
            else:
                for entity in my_lob:
                    if (state.turn % 10 == 0):
                        for direction in battlecode.Direction.directions():
                            if entity.can_build(direction):
                                entity.queue_build(direction)

        else:
            for entity in my_lob:
                num = random(0,8)
                while not entity.can_move(battlecode.Direction.directions[num]):
                    num = random(0,8)
                entity.queue_move(battlecode.Direction.directions[num])
'''  


'''
    for entity in state.get_entities(team=state.my_team):
        # This line gets all the bots on your team

        if(state.turn % 10 == 0):
            for direction in battlecode.Direction.directions():
                if entity.can_build(direction):
                    entity.queue_build(direction)

        my_location = entity.location
        near_entites = entity.entities_within_euclidean_distance(2)
        near_entites = list(filter(lambda x: x.can_be_picked, near_entites))

        for pickup_entity in near_entites:
            #assert entity.location.is_adjacent(pickup_entity.location)
            if entity.can_pickup(pickup_entity):
                entity.queue_pickup(pickup_entity)

        statue = nearest_glass_state(state, entity)
        if(statue != None):
            direction = entity.location.direction_to(statue.location)
            if entity.can_throw(direction):
                entity.queue_throw(direction)

        for direction in battlecode.Direction.directions():
            if entity.can_move(direction):
                entity.queue_move(direction)
'''

end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
