import os
from typing import Optional, Any

class Piece:
    def __init__(self, name: str, color: str, value: float, texture: Optional[Any] = None, texture_rect: Optional[Any] = None):
        self.name = name
        self.color = color
        self.value = value * (1 if color == 'white' else -1)
        self.moves = []
        self.moved = False
        self.texture = texture if texture else self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size: int = 80) -> str:
        """Sets the texture path for the piece."""
        return os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move: Any) -> None:
        """Adds a move to the piece's move list."""
        self.moves.append(move)

    def clear_moves(self) -> None:
        """Clears the piece's move list."""
        self.moves = []

class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__('pawn', color, 1.0)
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False

class Knight(Piece):
    def __init__(self, color: str):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):
    def __init__(self, color: str):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color: str):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color: str):
        super().__init__('king', color, 10000.0)
        self.left_rook = None
        self.right_rook = None
