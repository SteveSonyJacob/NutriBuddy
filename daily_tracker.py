class DailyTracker:
    def __init__(self):
        self.items = []

    def add_item(self, name, grams, nutrition):
        self.items.append({
            "name": name,
            "grams": grams,
            "nutrition": nutrition
        })

    def summary(self):
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for item in self.items:
            for k in total:
                total[k] += item['nutrition'].get(k, 0)
        return total

    def reset(self):
        self.items = []
