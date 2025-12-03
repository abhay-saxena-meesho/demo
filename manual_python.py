import random
import time

class Fighter:
    def __init__(self, name, hp, min_dmg, max_dmg):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        dmg = random.randint(self.min_dmg, self.max_dmg)
        target.hp -= dmg
        print(f"⚔️  {self.name} hits {target.name} for {dmg} damage!")

    def heal(self):
        heal_amt = random.randint(5, 15)
        self.hp = min(self.max_hp, self.hp + heal_amt)
        print(f"💚 {self.name} heals for {heal_amt} HP. Current HP: {self.hp}")

def game_loop():
    print("--- SIMPLE RPG BATTLE ---")
    player = Fighter("Hero", 50, 5, 12)
    monster = Fighter("Goblin King", 60, 3, 10)

    while player.is_alive() and monster.is_alive():
        print(f"\nYour HP: {player.hp} | Enemy HP: {monster.hp}")
        action = input("Choose action: (1) Attack (2) Heal (3) Run: ").strip()

        if action == '1':
            player.attack(monster)
        elif action == '2':
            player.heal()
        elif action == '3':
            print("🏃 You ran away safely!")
            return
        else:
            print("Invalid choice, you hesitate!")
            continue

        if monster.is_alive():
            time.sleep(0.5) # Add tension
            monster.attack(player)

    if player.is_alive():
        print("\n🏆 VICTORY! You defeated the enemy!")
    else:
        print("\n💀 GAME OVER. You were defeated.")

if __name__ == "__main__":
    game_loop()