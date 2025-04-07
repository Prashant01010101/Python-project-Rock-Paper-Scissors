import random
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('rps_game.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS game_results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  player_choice TEXT,
                  computer_choice TEXT,
                  result TEXT)''')
    conn.commit()
    conn.close()


def save_result(player_choice, computer_choice, result):
    conn = sqlite3.connect('rps_game.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO game_results (timestamp, player_choice, computer_choice, result) VALUES (?, ?, ?, ?)",
              (datetime.now(), player_choice, computer_choice, result))
    conn.commit()
    conn.close()


def get_statistics():
    conn = sqlite3.connect('rps_game.db')
    c = conn.cursor()
    
    
    c.execute("SELECT COUNT(*) FROM game_results")
    total_games = c.fetchone()[0]
    
    
    c.execute("SELECT COUNT(*) FROM game_results WHERE result='win'")
    player_wins = c.fetchone()[0]
    

    c.execute("SELECT COUNT(*) FROM game_results WHERE result='lose'")
    computer_wins = c.fetchone()[0]
    

    c.execute("SELECT COUNT(*) FROM game_results WHERE result='tie'")
    ties = c.fetchone()[0]
    

    c.execute("SELECT player_choice, COUNT(*) as count FROM game_results GROUP BY player_choice ORDER BY count DESC LIMIT 1")
    frequent_player_choice = c.fetchone()
    
    
    c.execute("SELECT computer_choice, COUNT(*) as count FROM game_results GROUP BY computer_choice ORDER BY count DESC LIMIT 1")
    frequent_computer_choice = c.fetchone()
    
    conn.close()
    
    return {
        'total_games': total_games,
        'player_wins': player_wins,
        'computer_wins': computer_wins,
        'ties': ties,
        'frequent_player_choice': frequent_player_choice,
        'frequent_computer_choice': frequent_computer_choice
    }


def play_game():
    options = ("rock", "paper", "scissors")
    init_db()
    
    while True:
        player = None
        computer = random.choice(options)

        while player not in options:
            player = input("Enter a choice (rock, paper, scissors): ").lower()

        print(f"Player: {player}")
        print(f"Computer: {computer}")

        if player == computer:
            print("It's a tie!")
            result = 'tie'
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            print("You win! 🎉")
            result = 'win'
        else:
            print("You lose! 💀")
            result = 'lose'
        
    
        save_result(player, computer, result)
        
        
        if input("View statistics? (y/n): ").lower() == 'y':
            stats = get_statistics()
            print("=== Game Statistics ===")
            print(f"Total games played: {stats['total_games']}")
            print(f"Player wins: {stats['player_wins']}")
            print(f"Computer wins: {stats['computer_wins']}")
            print(f"Ties: {stats['ties']}")
            if stats['frequent_player_choice']:
                print(f"Your most frequent choice: {stats['frequent_player_choice'][0]} ({stats['frequent_player_choice'][1]} times)")
            if stats['frequent_computer_choice']:
                print(f"Computer's most frequent choice: {stats['frequent_computer_choice'][0]} ({stats['frequent_computer_choice'][1]} times)")
            print("======================")
        
        if input("Play again? (y/n): ").lower() != 'y': 
            break
            
    print("Thanks for playing!")


if __name__ == "__main__":
    play_game()