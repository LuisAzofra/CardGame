import random

# Clase Card
class Card:
    def __init__(self, name, card_type, attack, health, skills):
        self.name = name
        self.card_type = card_type
        self.attack = attack
        self.health = health
        self.skills = skills

    def use_skill(self, opponent_card, player, opponent):
        for skill in self.skills:
            if skill == "Counterattack":
                damage = self.attack // 2
                opponent_card.take_damage(damage)
            elif skill == "Fireball":
                opponent.take_damage(3)
            elif skill == "Shield":
                self.health += 2  # Reduce incoming damage effect
            elif skill == "Berserk":
                if self.health <= 2:
                    self.attack += 2
            elif skill == "Intimidate":
                if opponent.hand:
                    removed_card = opponent.hand.pop(random.randint(0, len(opponent.hand) - 1))
                    print(f"Intimidate removed {removed_card.name} from opponent's hand!")
            elif skill == "Burn":
                opponent.take_damage(2)

    def take_damage(self, damage):
        self.health -= damage

    def is_destroyed(self):
        return self.health <= 0

# Clase Player
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 20
        self.hand = []

    def play_card(self, index):
        if 0 <= index < len(self.hand):
            return self.hand.pop(index)
        else:
            print("Invalid card choice! Losing turn.")
            return None

    def take_damage(self, damage):
        self.health -= damage

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def is_defeated(self):
        return self.health <= 0

# Clase Game
class Game:
    def __init__(self):
        self.player = Player("Player")
        self.computer = Player("Computer")
        self.predefined_cards = [
            Card("Swordsman", "Warrior", 6, 5, ["Counterattack"]),
            Card("Berserker", "Warrior", 8, 4, ["Berserk"]),
            Card("Fireball Mage", "Mage", 5, 3, ["Fireball"]),
            Card("Ice Sorcerer", "Mage", 4, 4, ["Shield"]),
            Card("Baby Dragon", "Dragon", 7, 8, ["Intimidate"]),
            Card("Dragon King", "Dragon", 10, 12, ["Burn"]),
        ]

    def start_game(self):
        self.player.hand = random.sample(self.predefined_cards, 3)
        self.computer.hand = random.sample(self.predefined_cards, 3)
        
        print("Game Start!")
        while not self.player.is_defeated() and not self.computer.is_defeated() and (self.player.hand or self.computer.hand):
            self.player_turn()
            if self.computer.is_defeated():
                break
            self.computer_turn()

        self.check_winner()

    def player_turn(self):
        print(f"\nYour Health: {self.player.health}")
        print("Your Cards:")
        for i, card in enumerate(self.player.hand):
            print(f"{i}: {card.name} ({card.card_type}) - ATK: {card.attack}, HP: {card.health}, Skills: {', '.join(card.skills)})")

        try:
            choice = int(input("Choose a card to play (0-2): "))
            player_card = self.player.play_card(choice)
            if not player_card:
                return
        except ValueError:
            print("Invalid input! Losing turn.")
            return

        computer_card = random.choice(self.computer.hand)

        print(f"You played {player_card.name} vs Computer's {computer_card.name}")

        player_card.use_skill(computer_card, self.player, self.computer)
        computer_card.use_skill(player_card, self.computer, self.player)

        computer_card.take_damage(player_card.attack)
        player_card.take_damage(computer_card.attack)

        if computer_card.is_destroyed():
            print(f"Computer's {computer_card.name} is destroyed!")
            self.computer.remove_card(computer_card)
        if player_card.is_destroyed():
            print(f"Your {player_card.name} is destroyed!")

    def computer_turn(self):
        if not self.computer.hand:
            print("Computer has no cards left! Skipping turn.")
            return

        computer_card = self.computer.play_card(random.randint(0, len(self.computer.hand) - 1))
        if not self.player.hand:
            print("You have no cards left to defend! Computer deals direct damage.")
            self.player.take_damage(computer_card.attack)
            return

        player_card = random.choice(self.player.hand)

        print(f"Computer played {computer_card.name} vs Your {player_card.name}")

        computer_card.use_skill(player_card, self.computer, self.player)
        player_card.use_skill(computer_card, self.player, self.computer)

        player_card.take_damage(computer_card.attack)
        computer_card.take_damage(player_card.attack)

        if player_card.is_destroyed():
            print(f"Your {player_card.name} is destroyed!")
            self.player.remove_card(player_card)
        if computer_card.is_destroyed():
            print(f"Computer's {computer_card.name} is destroyed!")

    def check_winner(self):
        print("\nGame Over!")
        if self.player.is_defeated():
            print("Computer wins!")
        elif self.computer.is_defeated():
            print("You win!")
        elif self.player.health > self.computer.health:
            print("You win by health points!")
        elif self.computer.health > self.player.health:
            print("Computer wins by health points!")
        else:
            print("It's a draw!")

# Ejecutar el juego
if __name__ == "__main__":
    game = Game()
    game.start_game()
