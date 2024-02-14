from .server_manager import ServerManager


class Pycasso:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.instructions = []

        # Start servers and open browser
        initial_message = serialize([("resize", f"{self.width};{self.height}")])
        self.server_manager = ServerManager(42069, 3001, True, initial_message)
        self.server_manager.run()

    def clear(self):
        self.instructions.append(("clear", f"0;0;{self.width};{self.height}"))

    def fillStyle(self, color):
        self.instructions.append(("fillStyle", color))

    def fillRect(self, x, y, width, height):
        self.instructions.append(("fillRect", f"{x};{y};{width};{height}"))

    def draw(self):
        instruction = "\n".join([f"{i[0]}:{i[1]}" for i in self.instructions])

        self.server_manager.broadcast(instruction)

        self.instructions.clear()


def serialize(instructions):
    return "\n".join([f"{i[0]}:{i[1]}" for i in instructions])
