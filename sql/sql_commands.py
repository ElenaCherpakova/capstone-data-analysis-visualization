import sqlite3
import sys
import os

def exit_app():
    print('👋 Bye, see you soon!')
    sys.exit()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def list_players(cursor):
    league_input = input("Choose league 1 - American, 2 - National, OR nothing for all leagues ").strip()
    clear_screen()
    try:
        if league_input == "":
            cursor.execute("""SELECT p.player_id, p.name, p.team, l.league_type  FROM Players p JOIN league l ON p.league_id = l.id""")        
        else:
            league_id = int(league_input)
            if league_id not in (1, 2):
                print("Please enter either 1, 2 or leave blank.")
                return
            cursor.execute("""SELECT p.player_id, p.name, p.team, l.league_type  FROM Players p JOIN league l ON p.league_id = l.id WHERE l.id = ?""", (league_id,))
    except ValueError:
        print("Invalid input. Please enter 1, 2, or nothing.")
        return

    players = cursor.fetchall()
    if players:
            print("All Players:")
            for pid, name, team, league in players:
                print(f"{pid}: {name} ({team}) - {league}")
    else:
        print("No players found in that league.")


def show_career_stats(cursor):
    name = input("Type player name to find (partial or full): ").strip()
    if not name:
        print("Please enter a player name.")
        return
    cursor.execute("""
        SELECT p.name, p.team, c.career_length, c.games_played, c.hits
        FROM Players p
        LEFT JOIN CareerStats c ON p.player_id = c.player_id
        WHERE p.name LIKE ?
        ORDER BY p.name
    """, (f"%{name}%",))
    results = cursor.fetchall()
    if not results:
        print("No players found with that name.")
        return
    for name, team, career_length, games_played, hits in results:
        print(f"\nStats for {name} ({team}):")
        if career_length is not None:
            print("="*40)
            print(f"Career Length: {career_length} years")
            print(f"Games Played: {games_played}")
            print(f"Hits: {hits}")
            print("="*40 + "\n")  # Add spacing after list

        else:
            print("No career stats available.")


def show_stats_by_year_range(cursor):
    try:
        start_year = int(input("Start year: ").strip())
        end_year = int(input("End year: ").strip())
    except ValueError:
        print("Please enter valid years.")
        return

    if start_year > end_year:
        print("Start year must be <= end year.")
        return

    cursor.execute("""
        SELECT p.name, p.team, ps.statistic, ps.value, ps.year, l.league_type
        FROM Players p
        JOIN League l ON p.league_id = l.id
        JOIN PlayerStats ps ON p.player_id = ps.player_id
        WHERE ps.year BETWEEN ? AND ?
        ORDER BY ps.year, p.name
    """, (start_year, end_year))

    results = cursor.fetchall()
    if results:
        current_year = None
        for name, team, stat, value, year, league in results:
            if year != current_year:
                current_year = year
                print(f"\nYear: {year}")
            print(f"{name} ({team}-{league}): {stat} = {value}")
    else:
        print("No stats found for that range.")


def main():
    try:
        with sqlite3.connect("../db/players.db") as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()

            while True:
                print("\nPlease choose one of the following commands:\n")
                print("pick - Choose a league")
                print("find — Search player by name and show career stats")
                print("range — Show players stats filtered by year range")
                print("exit — Quit the program")

                command = input("> ").strip().lower()

                if command == "pick":
                    list_players(cursor)
                elif command == "find":
                    show_career_stats(cursor)
                elif command == "range":
                    show_stats_by_year_range(cursor)
                elif command == "exit":
                    exit_app()
                else:
                    print("Unknown command, try again.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit()


if __name__ == "__main__":
    main()
