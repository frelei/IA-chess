"""
	REPRESENTA UM PEAO NO CAMPO
"""

class Pawn(Piece):

	def __init__(self,position):
		Piece.__init__(self,position,'p') # Pode ser P ou p