
class BodyPart:
    def __init__(self, hp=0, size=0, name="", is_critical=False):
        self.max_hp = hp
        self.hp = self.max_hp
        self.size = size
        self.name = name
        self.is_critical = is_critical
        self.dead = True
    def on_death(self):
        self.dead = True
    def on_life(self):
        self.dead = False
    def bleed(self):
        return self.hp - self.max_hp
    def status(self):
        if self.hp == 0:
            return "dead"
        statuses = ["destroyed", "mangled", "broken", "damaged", "scuffed", "fine", "perfect"]
        return statuses[int(float(self.hp)/self.max_hp * (len(statuses)-1))]
    def damage(self, amount):
        prev_hp = self.hp
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            if prev_hp > 0:
                self.on_death()
                return self.is_critical
    def heal(self, amount):
        prev_hp = self.hp
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if prev_hp <= 0 and self.hp > 0:
            self.on_life()
            return self.is_critical

class Arm(BodyPart):
    def __init__(self, hp=15, size=100, name="Arm", is_critical=False):
        BodyPart.__init__(self, hp, size, name, is_critical)

class Leg(BodyPart):
    def __init__(self, hp=10, size=125, name="Leg", is_critical=False):
        BodyPart.__init__(self, hp, size, name, is_critical)

class Torso(BodyPart):
    def __init__(self, hp=25, size=400, name="Torso", is_critical=True):
        BodyPart.__init__(self, hp, size, name, is_critical)
    def bleed(self):
        return (self.hp - self.max_hp)*2

class Head(BodyPart):
    def __init__(self, hp=10, size=25, name="Head", is_critical=True):
        BodyPart.__init__(self, hp, size, name, is_critical)
    def bleed(self):
        return (self.hp - self.max_hp)*4

