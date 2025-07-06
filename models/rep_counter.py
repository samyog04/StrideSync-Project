class RepCounter:
    def __init__(self):
        self.count = 0
        self.state = None

    def update(self, angle):
        if angle > 160:
            self.state = "up"
        elif angle < 60 and self.state == "up":
            self.state = "down"
            self.count += 1
        return self.count