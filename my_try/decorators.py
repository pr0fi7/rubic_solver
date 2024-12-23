def update_white_sides_after(func):
    def wrapper(self, *args, **kwargs):
        # print("Updating white sides")
        result = func(self, *args, **kwargs)
        self.white_sides = self.find_white_sides()  # Recalculate white_sides
        return result
    return wrapper