import random

# Clase Card
class Card:
    def __init__(self, name, card_type, attack, health, skills):
        self.name = name
        self.card_type = card_type
        self.base_attack = attack  # Guardar el ataque base
        self.base_health = health  # Guardar la salud base
        self.attack = attack
        self.health = health
        self.skills = skills
        self.disabled = False  # Flag for "Intimidate" effect
        self.shield_used = False  # Flag for "Shield" effect in computer card 

    def reset_stats(self):
        """Resetea los valores de ataque y salud a sus valores originales."""
        self.attack = self.base_attack
        self.health = self.base_health

    def use_skill(self, opponent_card, player, opponent, is_player, direct_attack=False):
        for skill in self.skills:
            owner = "Your" if is_player else "Computer's"
            if skill == "Counterattack" and opponent_card:
                damage = self.attack // 2
                initial_health = opponent_card.health
                opponent_card.take_damage(damage)
                print(f"{owner} {self.name} used Counterattack, dealing {damage} damage to {opponent_card.name}. {opponent_card.name}'s health reduced from {initial_health} to {opponent_card.health}.")
            elif skill == "Fireball":
                opponent.take_damage(3)
                print(f"{owner} {self.name} used Fireball, dealing 3 damage to {opponent.name}. Remaining health: {opponent.health}.")
            elif skill == "Shield":
                if not self.shield_used:  # Solo usa Shield si no ha sido activado en este turno
                    self.health += 2
                    self.shield_used = True
                    print(f"{owner} {self.name} used Shield, increasing health by 2. Current health: {self.health}.")

            elif skill == "Berserk":
                if self.health <= 2:
                    self.attack += 2
                    print(f"{owner} {self.name} used Berserk, gaining 2 attack. Current attack: {self.attack}.")
            elif skill == "Intimidate":
                if opponent.hand:
                    removed_card = opponent.hand.pop(random.randint(0, len(opponent.hand) - 1))
                    removed_card.disabled = True  # Disable the card for the next turn
                    opponent.intimidated_card = removed_card  # Track the intimidated card
                    if is_player:
                        print(f"{owner} {self.name} used Intimidate, removing {removed_card.name} from opponent's hand for one turn!")
                    else:
                        print(f"{owner} {self.name} used Intimidate, removing {removed_card.name} from your hand for one turn!")
            elif skill == "Burn" and direct_attack:
                opponent.take_damage(2)
                print(f"{owner} {self.name} used Burn, dealing 2 extra damage to {opponent.name}. Remaining health: {opponent.health}.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_destroyed(self):
        return self.health <= 0

# Clase Player
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 20
        self.hand = []
        self.intimidated_card = None  # Track the intimidated card

    def play_card(self, index):
        if 0 <= index < len(self.hand):
            card = self.hand[index]
            if card.disabled:
                print(f"{card.name} is disabled and cannot be played this turn.")
                return None
            elif card.is_destroyed():
                print(f"{card.name} has been destroyed and cannot be played.")
                return None
            else:
                return card
        else:
            print("Invalid card choice! Losing turn.")
            return None

    def finalize_play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def restore_intimidated_card(self):
        if self.intimidated_card:
            self.hand.append(self.intimidated_card)
            print(f"{self.intimidated_card.name} returns to the hand after being intimidated.")
            self.intimidated_card.disabled = False
            self.intimidated_card = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

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
        self.player.hand = [Card(card.name, card.card_type, card.base_attack, card.base_health, card.skills[:]) for card in random.sample(self.predefined_cards, 3)]
        self.computer.hand = [Card(card.name, card.card_type, card.base_attack, card.base_health, card.skills[:]) for card in random.sample(self.predefined_cards, 3)]
    
        print("\n====================== GAME START ======================")
        while not self.player.is_defeated() and not self.computer.is_defeated() and (self.player.hand or self.computer.hand):
            self.battle_turn()

        self.check_winner()

    def display_action(self, action):
        print(f"\n{'-'*10} {action} {'-'*10}")

    def display_tutorial(self, cards):
        print("\n--- Skills Information ---")
        for card in cards:
            for skill in card.skills:
                if skill == "Counterattack":
                    print("Counterattack: Deals half of the attack damage back to the attacker.")
                elif skill == "Fireball":
                    print("Fireball: Deals 3 direct damage to the opponent's health.")
                elif skill == "Shield":
                    print("Shield: Increases the card's health by 2.")
                elif skill == "Berserk":
                    print("Berserk: Increases attack by 2 if the card's health is 2 or less.")
                elif skill == "Intimidate":
                    print("Intimidate: Removes a card from the opponent's hand for one turn.")
                elif skill == "Burn":
                    print("Burn: Deals 2 extra damage to the opponent's health (not to cards).")
        print("--- End of Skills Information ---\n")

    def battle_turn(self):
        #Restarts shield used flag for all cards 
        for card in self.player.hand + self.computer.hand:
            card.shield_used = False
        self.player.restore_intimidated_card()
        self.computer.restore_intimidated_card()

        self.player.hand = [card for card in self.player.hand if not card.is_destroyed()]
        self.computer.hand = [card for card in self.computer.hand if not card.is_destroyed()]

        if not self.player.hand:
            print("You have no cards left! Skipping turn.")
            self.computer_direct_attack()
            return

        if not self.computer.hand:
            print("Computer has no cards left! Skipping turn.")
            self.player_direct_attack()
            return

        print(f"\nYour Health: {self.player.health}")
        print("Your Cards:")
        for i, card in enumerate(self.player.hand):
            print(f"{i}: {card.name} ({card.card_type}) - ATK: {card.attack}, HP: {card.health}, Skills: {', '.join(card.skills)})")
        
        tutorial_choice = input(f"Choose a card to play (0-{len(self.player.hand) - 1}) or type 'info' to view skills: ").strip().lower()
        if tutorial_choice == "info":
            self.display_tutorial(self.player.hand)
            tutorial_choice = input(f"Now choose a card to play (0-{len(self.player.hand) - 1}): ").strip()

        try:
            choice = int(tutorial_choice)
            player_card = self.player.play_card(choice)
            if not player_card:
                return
        except ValueError:
            print("Invalid input! Losing turn.")
            return

        computer_card = random.choice(self.computer.hand)

        print(f"\nYour {player_card.name} vs Computer's {computer_card.name}")

        # Player's Card Attack
        self.display_action("Player's Card Attack")
        if "Shield" in computer_card.skills and computer_card.name == "Ice Sorcerer" and not computer_card.shield_used:
            computer_card.use_skill(player_card, self.computer, self.player, False)

        computer_old_health = computer_card.health
        player_card.use_skill(computer_card, self.player, self.computer, True)
        computer_card.take_damage(player_card.attack)
        eliminated = " (Eliminated)" if computer_card.health == 0 else ""
        print(f"Your {player_card.name} dealt {player_card.attack} damage to Computer's {computer_card.name}. "
        f"Computer's {computer_card.name} health reduced from {computer_old_health} to {computer_card.health}{eliminated}.")
        
        # Computer's Card Attack
        self.display_action("Computer's Card Attack")
        player_old_health = player_card.health
        computer_card.use_skill(player_card, self.computer, self.player, False)
        player_card.take_damage(computer_card.attack)
        eliminated = " (Eliminated)" if player_card.health == 0 else ""
        print(f"Computer's {computer_card.name} dealt {computer_card.attack} damage to Your {player_card.name}. Your {player_card.name} health reduced from {player_old_health} to {player_card.health}{eliminated}.")

        if player_card.health == 0:
            print(f"Your {player_card.name} has been destroyed.")
            self.player.finalize_play_card(player_card)
        if computer_card.health == 0:
            print(f"Computer's {computer_card.name} has been destroyed.")
            self.computer.remove_card(computer_card)

    def check_winner(self):
        print("\n====================== GAME OVER ======================")
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

    def player_direct_attack(self):
        if not self.player.hand:
            print("You have no cards left to attack.")
            return
        card = random.choice(self.player.hand)
        card.use_skill(None, self.player, self.computer, True, direct_attack=True)
        self.computer.take_damage(card.attack)
        print(f"Your {card.name} attacks directly, dealing {card.attack} damage to the computer. Remaining health: {self.computer.health}")

    def computer_direct_attack(self):
        if not self.computer.hand:
            print("Computer has no cards left to attack.")
            return
        card = random.choice(self.computer.hand)
        card.use_skill(None, self.computer, self.player, False, direct_attack=True)
        self.player.take_damage(card.attack)
        print(f"Computer's {card.name} attacks directly, dealing {card.attack} damage to you. Remaining health: {self.player.health}")


if __name__ == "__main__":
    game = Game()
    game.start_game()
