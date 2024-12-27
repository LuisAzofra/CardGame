# Turn-Based Strategy Card Game

A Python-based turn-based card game where players use cards with unique abilities to compete. The objective is to defeat the opponent by reducing their health to zero or destroying all their cards.

---

## Features

### 1. Classes and Objects
- **`Card` Class:** Represents a card with attributes such as:
  - `name`: Card's name
  - `card_type`: Type of card (e.g., Warrior, Mage, Dragon)
  - `attack`: Attack power
  - `health`: Health points
  - `skills`: List of special abilities.
  - Methods include:
    - `use_skill`: Activates the card's abilities during a match.
    - `take_damage`: Reduces the card's health when attacked.
    - `is_destroyed`: Checks if the card's health has dropped to zero.

- **`Player` Class:** Represents each player with:
  - Attributes:
    - `health`: Player's health, starting at 20.
    - `hand`: The player's current cards.
  - Methods include:
    - `play_card`: Allows the player to select and play a card from their hand.
    - `take_damage`: Reduces the player's health.
    - `remove_card`: Removes a destroyed card from the player's hand.
    - `is_defeated`: Checks if the player's health has reached zero.

- **`Game` Class:** Manages the overall gameplay:
  - Handles turn-based mechanics.
  - Manages card interactions between players.
  - Determines the winner at the end of the game.

---

### 2. Gameplay Mechanics
- **Game Setup:**
  - Both players are dealt 3 random cards from a predefined deck.
  - Each card has its own attack, health, and abilities.
  
- **Turn Flow:**
  1. Players take turns selecting and playing a card.
  2. Cards battle each other, with their skills activated during combat.
  3. If a card's health reaches zero, it is removed from the game.
  
- **Win Condition:**
  - Reduce the opponent's health to zero, or destroy all their cards.

---

### 3. Card Abilities
The predefined cards come with the following special abilities:

| Skill           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Counterattack**| Reflects part of the attack damage back to the opponent's card.            |
| **Fireball**     | Inflicts direct damage to the opponent's health.                           |
| **Shield**       | Increases the card's health, making it more resistant to attacks.          |
| **Berserk**      | Boosts the card's attack when its health is critically low.                |
| **Intimidate**   | Removes a random card from the opponent's hand.                            |
| **Burn**         | Inflicts continuous damage to the opponent over multiple turns.            |

---

### 4. Predefined Cards
| Name           | Type    | Attack | Health | Skills          |
|----------------|---------|--------|--------|-----------------|
| Swordsman      | Warrior | 6      | 5      | Counterattack   |
| Berserker      | Warrior | 8      | 4      | Berserk         |
| Fireball Mage  | Mage    | 5      | 3      | Fireball        |
| Ice Sorcerer   | Mage    | 4      | 4      | Shield          |
| Baby Dragon    | Dragon  | 7      | 8      | Intimidate      |
| Dragon King    | Dragon  | 10     | 12     | Burn            |

---

### 5. Example Gameplay
- Both the player and the computer are dealt 3 random cards from the deck.
- The player chooses a card from their hand to play, and the computer responds with its own card.
- Each card attacks and activates its skills:
  - Damage is dealt to the opponent's card or health.
  - Skills like "Burn" or "Intimidate" are triggered based on the card's abilities.
- A card is destroyed when its health reaches zero and is removed from play.
- The game continues until one player's health is reduced to zero or no cards remain.
