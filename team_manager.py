"""
Team selection logic module for Moretus application
Implements the ±2 board placement rule
"""

from itertools import permutations
from typing import List, Dict, Tuple
import random


class TeamManager:
    """Manages team selection and board placement according to rules"""
    
    # Maximum board offset from strength list rank
    MAX_BOARD_OFFSET = 2
    TEAM_SIZE = 6
    
    @staticmethod
    def get_allowed_boards(rank: int, team_size: int = TEAM_SIZE) -> List[int]:
        """
        Get allowed board positions for a player based on their strength list rank.
        
        Args:
            rank: Player's position in strength list (1-indexed, 1 being strongest)
            team_size: Total team size (default 6)
            
        Returns:
            List of valid board positions (1-indexed)
            
        Example:
            rank=3 -> [1, 2, 3, 4, 5] (3±2)
        """
        min_board = max(1, rank - TeamManager.MAX_BOARD_OFFSET)
        max_board = min(team_size, rank + TeamManager.MAX_BOARD_OFFSET)
        return list(range(min_board, max_board + 1))
    
    @staticmethod
    def is_valid_assignment(board_assignment: List[int]) -> bool:
        """
        Check if a board assignment is valid (respects ±2 rule).
        
        Args:
            board_assignment: List where index is player rank (0-indexed) and value is board position (1-indexed)
            
        Returns:
            True if assignment is valid, False otherwise
        """
        for rank_idx, board_pos in enumerate(board_assignment):
            rank = rank_idx + 1  # Convert to 1-indexed
            allowed_boards = TeamManager.get_allowed_boards(rank, len(board_assignment))
            if board_pos not in allowed_boards:
                return False
        return True
    
    @staticmethod
    def get_all_valid_assignments(team_size: int = TEAM_SIZE) -> List[List[int]]:
        """
        Generate all valid board assignments for a team of given size.
        
        Args:
            team_size: Number of players on team (default 6)
            
        Returns:
            List of valid board assignments, where each assignment is a list
            where index = player rank (0-indexed) and value = board position (1-indexed)
        """
        # Generate all possible board permutations (boards 1 to team_size)
        all_permutations = permutations(range(1, team_size + 1))
        
        valid_assignments = []
        for perm in all_permutations:
            board_assignment = list(perm)
            if TeamManager.is_valid_assignment(board_assignment):
                valid_assignments.append(board_assignment)
        
        return valid_assignments
    
    @staticmethod
    def get_count_valid_assignments(team_size: int = TEAM_SIZE) -> int:
        """
        Get count of all valid board assignments without generating all of them.
        Useful for large counts.
        
        Args:
            team_size: Number of players on team (default 6)
            
        Returns:
            Number of valid configurations
        """
        return len(TeamManager.get_all_valid_assignments(team_size))
    
    @staticmethod
    def get_first_valid_assignment(team_size: int = TEAM_SIZE) -> List[int]:
        """
        Get the first valid board assignment (players assigned to their base rank).
        
        Args:
            team_size: Number of players on team (default 6)
            
        Returns:
            First valid assignment (ideal: [1, 2, 3, 4, 5, 6])
        """
        valid_assignments = TeamManager.get_all_valid_assignments(team_size)
        if valid_assignments:
            return valid_assignments[0]
        return list(range(1, team_size + 1))
    
    @staticmethod
    def get_random_valid_assignment(team_size: int = TEAM_SIZE) -> List[int]:
        """
        Get a random valid board assignment from all possibilities.
        
        Args:
            team_size: Number of players on team (default 6)
            
        Returns:
            Random valid board assignment (1-indexed)
        """
        valid_assignments = TeamManager.get_all_valid_assignments(team_size)
        if valid_assignments:
            return random.choice(valid_assignments)
        return list(range(1, team_size + 1))
    
    @staticmethod
    def format_team_assignment(players: List[Dict], board_assignment: List[int]) -> List[Dict]:
        """
        Format team with player data and board assignments.
        
        Args:
            players: List of player dictionaries from database (ordered by strength list)
            board_assignment: Board positions for each player (1-indexed)
            
        Returns:
            List of player dictionaries with 'board' field added
        """
        team = []
        for rank_idx, player in enumerate(players):
            board_pos = board_assignment[rank_idx]
            player_with_board = player.copy()
            player_with_board['board'] = board_pos
            player_with_board['rank'] = rank_idx + 1
            team.append(player_with_board)
        
        # Sort by board position
        team.sort(key=lambda p: p['board'])
        return team


# Example usage and testing
if __name__ == "__main__":
    # Test with 6 players
    valid = TeamManager.get_all_valid_assignments(6)
    print(f"Total valid team configurations for 6 players: {len(valid)}")
    
    # Show some examples
    print("\nFirst 5 valid configurations:")
    for i, config in enumerate(valid[:5]):
        print(f"  Config {i+1}: {config}")
    
    # Test allowed boards
    print("\nAllowed boards by strength rank:")
    for rank in range(1, 7):
        allowed = TeamManager.get_allowed_boards(rank)
        print(f"  Rank {rank}: boards {allowed}")
