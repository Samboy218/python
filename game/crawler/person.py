import parts
import random

class Person():
    def __init__(self, name="noone"):
        self.parts = []
        self.parts.append(parts.Arm(name="Right Arm"))
        self.parts.append(parts.Arm(name="Left Arm"))
        self.parts.append(parts.Leg(name="Right Leg"))
        self.parts.append(parts.Leg(name="Left Arm"))
        self.parts.append(parts.Head(name="Head"))
        self.parts.append(parts.Torso(name="Torso"))
        self.max_blood = sum([part.size for part in self.parts])
        self.blood = self.max_blood

    def isDead(self):
        for part in self.parts:
            if part.is_critical and part.dead:
                return True
    def getRandomPart(self):
        curr_total = 0
        totals = [0]
        for  part in self.parts:
            curr_total += part.size
            totals.append(curr_total)
        select = random.randrange(curr_total)
        for i, choice in enumerate(totals):
            if totals[i] > select:
                return self.parts[i-1]
    def attack(self, amount):
        part = self.getRandomPart()
        return (part, part.damage(amount))

bob = Person("bob")
while True:
    damage = random.randrange(10)
    part, res = bob.attack(damage)
    print("you attacked bob's {} for {} damage and the part is {}.".format(part.name, damage, part.status()))
    if res:
        print("And you killed him!\n")
        break
    input("")

