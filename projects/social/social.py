import random
import string
from util import Queue

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name, self.last_id)
        self.friendships[self.last_id] = set()

    def create_random_name(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(6))

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(i)
        # Create friendships
        for i in self.users:
            self.friendships[i] = set()
        total_friendhsips = num_users * avg_friendships

        while total_friendhsips > 0:
            user_1 = random.randint(1, num_users)
            user_2 = random.randint(1, num_users)
            while user_2 == user_1:
                user_2 = random.randint(1, num_users)
            if user_2 not in self.friendships[user_1]:
                self.add_friendship(user_1, user_2)
                total_friendhsips -= 2
        # for _u, _key in enumerate(self.users):
        #     add = random.choices(range(1, num_users), k=avg_friendships)
        #     for item in add:
        #         self.add_friendship(_u+1, item)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        q = Queue()
        q.enqueue([user_id])

        while q.size() > 0:
            path = q.dequeue()
            seen = path[-1]

            if seen not in visited:
                visited[seen] = path

                for neighbor in self.friendships[seen]:
                    copy = list(path)
                    copy.append(neighbor)
                    q.enqueue(copy)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)