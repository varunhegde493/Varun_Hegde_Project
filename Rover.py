class Command:
    def execute(self):
        pass

class MoveCommand(Command):
    def __init__(self, rover):
        self.rover = rover

    def execute(self):
        self.rover.move()

class TurnLeftCommand(Command):
    def __init__(self, rover):
        self.rover = rover

    def execute(self):
        self.rover.turn_left()

class TurnRightCommand(Command):
    def __init__(self, rover):
        self.rover = rover

    def execute(self):
        self.rover.turn_right()

class Rover:
    DIRECTIONS = ['N', 'E', 'S', 'W']

    def __init__(self, x, y, direction, grid, obstacles):
        self.x = x
        self.y = y
        self.direction = direction
        self.grid = grid
        self.obstacles = obstacles

    def move(self):
        x, y = self.x, self.y

        if self.direction == 'N' and y < self.grid.size[1] - 1:
            y += 1
        elif self.direction == 'E' and x < self.grid.size[0] - 1:
            x += 1
        elif self.direction == 'S' and y > 0:
            y -= 1
        elif self.direction == 'W' and x > 0:
            x -= 1
        else:
            print("Cannot move. Out of bounds.")

        # Check for obstacles
        if any(obstacle.is_at(x, y) for obstacle in self.obstacles):
            print("Obstacle detected. Rover cannot move.")
        else:
            self.x, self.y = x, y

    def turn_left(self):
        current_direction_index = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(current_direction_index - 1) % 4]

    def turn_right(self):
        current_direction_index = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(current_direction_index + 1) % 4]

    def send_status_report(self):
        return f"Rover is at ({self.x}, {self.y}) facing {self.direction}. No obstacles detected."

class Grid:
    def __init__(self, size):
        self.size = size

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_at(self, x, y):
        return self.x == x and self.y == y

# Function for safe integer input within a range
def get_integer_input(prompt, min_value, max_value):
    while True:
        try:
            user_input = int(input(prompt))
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print(f"Please enter a value between {min_value} and {max_value}.")

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Function to validate direction input
def validate_direction(direction):
    valid_directions = ['N', 'E', 'S', 'W']
    return direction.upper() in valid_directions

# Get input from the user with error handling
try:
    # Get grid size
    rows = get_integer_input("Enter the number of rows in the grid: ", 1, float('inf'))
    columns = get_integer_input("Enter the number of columns in the grid: ", 1, float('inf'))
    grid_size = (rows, columns)

    # Get starting position
    while True:
        starting_position = input("Enter starting position (x, y, direction): ").split()
        if len(starting_position) == 3 and starting_position[2].upper() in ['N', 'E', 'S', 'W']:
            starting_position = tuple(map(int, starting_position[:2])) + (starting_position[2].upper(),)
            break
        else:
            print("Invalid input. Please enter in the format: x y direction (e.g., 0 0 N)")

    commands = input("Enter commands (e.g., 'MMLR'): ").upper()

    # Get the number of obstacles
    num_obstacles = get_integer_input("Enter the number of obstacles: ", 0, float('inf'))
    obstacles = []
    for i in range(num_obstacles):
        while True:
            obstacle = input(f"Enter obstacle {i+1} position (x, y): ").split()
            if len(obstacle) == 2:
                obstacle = tuple(map(int, obstacle))
                break
            else:
                print("Invalid input. Please enter in the format: x y")

        obstacles.append(obstacle)

    # Initialize the grid and obstacles
    grid = Grid(grid_size)
    obstacle_objects = [Obstacle(x, y) for x, y in obstacles]

    # Initialize the Rover
    rover = Rover(starting_position[0], starting_position[1], starting_position[2], grid, obstacle_objects)

    # Execute commands using the Command pattern
    for command in commands:
        if command == 'M':
            move_command = MoveCommand(rover)
            move_command.execute()
        elif command == 'L':
            left_command = TurnLeftCommand(rover)
            left_command.execute()
        elif command == 'R':
            right_command = TurnRightCommand(rover)
            right_command.execute()

    # Get the status report
    status_report = rover.send_status_report()
    print("Final Position:", f"({rover.x}, {rover.y}, {rover.direction})")
    print("Status Report:", status_report)

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
except Exception as e:
    print("An error occurred:", str(e))

