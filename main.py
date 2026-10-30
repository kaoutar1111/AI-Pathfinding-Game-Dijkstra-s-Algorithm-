import tkinter as tk
import heapq
import random  # For random AI behavior


class AvoidObstaclesGameDijkstra:
    def __init__(self, master):
        self.master = master
        self.master.title("Avoid Obstacles: Balanced AI")

        # Game setup
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.grid_width = self.width // self.cell_size
        self.grid_height = self.height // self.cell_size
        self.player_size = self.cell_size
        self.obstacle_size = self.cell_size
        self.speed = 20
        self.game_over = False
        self.player_x = self.width // 2
        self.player_y = self.height // 2
        self.obstacles = []
        self.num_obstacles = 3


        # AI difficulty adjustments
        self.ai_delay = 300  # Initial AI movement delay in ms
        self.random_move_chance = 0.15  # Probability of a random move
        self.difficulty_increment = 10  # Reduce AI delay every 10 steps
        self.difficulty_timer = 0  # Track time for increasing difficulty

        # Create the canvas
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()

        # Draw player (blue square)
        self.player = self.canvas.create_rectangle(self.player_x, self.player_y,
                                                   self.player_x + self.player_size,
                                                   self.player_y + self.player_size,
                                                   fill="blue")

        # Create AI obstacles (red squares)
        self.create_obstacles()

        # Game control
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

        # Start the game loop
        self.move_obstacles()

    def create_obstacles(self):
        """Generate AI obstacles in random positions"""
        for _ in range(self.num_obstacles):
            x = random.randint(0, self.grid_width - 1) * self.cell_size
            y = random.randint(0, self.grid_height - 1) * self.cell_size
            obstacle = self.canvas.create_rectangle(x, y, x + self.obstacle_size, y + self.obstacle_size, fill="red")
            self.obstacles.append(obstacle)

    def move_left(self, event):
        """Move the player left"""
        if not self.game_over:
            self.player_x -= self.speed
            self.update_player_position()

    def move_right(self, event):
        """Move the player right"""
        if not self.game_over:
            self.player_x += self.speed
            self.update_player_position()

    def move_up(self, event):
        """Move the player up"""
        if not self.game_over:
            self.player_y -= self.speed
            self.update_player_position()

    def move_down(self, event):
        """Move the player down"""
        if not self.game_over:
            self.player_y += self.speed
            self.update_player_position()

    def update_player_position(self):
        """Update player position on canvas"""
        self.canvas.coords(self.player, self.player_x, self.player_y,
                           self.player_x + self.player_size, self.player_y + self.player_size)
        self.check_collision()

    def get_grid_position(self, x, y):
        """Convert canvas coordinates to grid coordinates"""
        return x // self.cell_size, y // self.cell_size

    def get_canvas_position(self, grid_x, grid_y):
        """Convert grid coordinates to canvas coordinates"""
        return grid_x * self.cell_size, grid_y * self.cell_size

    def dijkstra(self, start, goal):
        """Find the shortest path using Dijkstra's algorithm"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = []
        heapq.heappush(queue, (0, start))
        visited = set()
        came_from = {}

        while queue:
            cost, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                break

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < self.grid_width and 0 <= neighbor[1] < self.grid_height:
                    if neighbor not in visited:
                        heapq.heappush(queue, (cost + 1, neighbor))
                        if neighbor not in came_from:
                            came_from[neighbor] = current

        # Reconstruct path
        path = []
        current = goal
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def move_obstacles(self):
        """Move the AI obstacles using Dijkstra's algorithm or random movement"""
        if self.game_over:
            return

        player_grid = self.get_grid_position(self.player_x, self.player_y)

        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            obstacle_grid = self.get_grid_position(obstacle_coords[0], obstacle_coords[1])

            if random.random() < self.random_move_chance:
                # Random movement
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                dx, dy = random.choice(directions)
                next_step = (obstacle_grid[0] + dx, obstacle_grid[1] + dy)
            else:
                # Dijkstra movement
                path = self.dijkstra(obstacle_grid, player_grid)
                next_step = path[0] if path else obstacle_grid

            next_x, next_y = self.get_canvas_position(next_step[0], next_step[1])
            self.canvas.coords(obstacle, next_x, next_y,
                               next_x + self.obstacle_size, next_y + self.obstacle_size)

        # Check for collisions
        self.check_collision()

        # Gradually increase difficulty
        self.difficulty_timer += 1
        if self.difficulty_timer % self.difficulty_increment == 0 and self.ai_delay > 150:
            self.ai_delay -= 10  # Increase AI speed over time

        # Continue moving obstacles
        self.master.after(self.ai_delay, self.move_obstacles)

    def check_collision(self):
        """Check if any obstacle collides with the player"""
        player_coords = self.canvas.coords(self.player)
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if (player_coords[2] > obstacle_coords[0] and
                    player_coords[0] < obstacle_coords[2] and
                    player_coords[3] > obstacle_coords[1] and
                    player_coords[1] < obstacle_coords[3]):
                self.game_over = True
                self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", font=("Arial", 24, "bold"),
                                        fill="red")
                return


# Create the Tkinter root window
root = tk.Tk()
game = AvoidObstaclesGameDijkstra(root)
root.mainloop()
