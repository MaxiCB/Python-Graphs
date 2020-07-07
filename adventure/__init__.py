from adventure.room import Room
from adventure.player import Player
from adventure.world import World
from graph.util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = dict()


def mark_visited(room_id, direction=None, next_room_id=None):
    # If not visited add it into the visited arr
    if room_id not in visited:
        visited[room_id] = {room_exit: None for room_exit in player.current_room.get_exits()}
    #     If the direction, and next room are defined add to visited
    if direction is not None and next_room_id is not None:
        visited[room_id][direction] = next_room_id


def find_dead_end():
    reverse = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }

    while True:
        # Set the current room, and mark as visited
        cur_room_id = player.current_room.id
        mark_visited(cur_room_id)
        # Gather all of the exits available in the room
        exits = [e for e in player.current_room.get_exits() if visited[cur_room_id][e] is None]
        # If there are no exits break
        if len(exits) == 0:
            break
        # Set current room as previous
        prev_room_id = cur_room_id
        # Pick a random direction from the available choices
        direction = random.choice(exits)
        # Move the player in the chose direction
        player.travel(direction)
        # Add the move to the traversal path
        traversal_path.append(direction)
        # Update the current room
        cur_room_id = player.current_room.id
        # Mark the previous room, and the current room as visited with both direction and previous room
        mark_visited(prev_room_id, direction, cur_room_id)
        mark_visited(cur_room_id, reverse[direction], prev_room_id)


def find_new_path():
    queue = Queue()
    # Initialize the current room
    cur_room_id = player.current_room.id
    # Initialize the bfs visited
    breadth_visited = {cur_room_id}
    # Iterate over the directions and rooms available and add to the queue
    for direction, room in visited[cur_room_id].items():
        queue.enqueue([(room, direction)])
    # While the queue length > 0
    while queue.size() > 0:
        # Deque the current room
        cur_path = queue.dequeue()
        # Mark the next room with room_id
        next_room = cur_path[-1][0]
        # Check for none in visited next room values
        if None in visited[next_room].values():
            # Explore possible directions to remove None values
            for room, direction in cur_path:
                traversal_path.append(direction)
                player.travel(direction)
            break
        # If directions and rooms exist
        for direction, room in visited[next_room].items():
            # Create reference to the current path
            path_copy = cur_path.copy()
            # Check if room is not visited
            if room not in breadth_visited:
                # Add to bfs visited
                breadth_visited.add(room)
                # Append to the path copy
                path_copy.append((room, direction))
                # Queue the new path
                queue.enqueue(path_copy)
        # Add the next room to bfs visited
        breadth_visited.add(next_room)


def traverse_map():
    # While the length of visited rooms is less than current graph
    while len(visited) < len(room_graph):
        # Search for dead ends, and available paths
        find_dead_end()
        find_new_path()


# This allows for better traversal speeds
random.seed(345047)
# Traverse the current map
traverse_map()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
