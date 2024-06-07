class TranslateMove:
    # Dictionaries for translating columns and rows
    col_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    letter_to_col = {v: k for k, v in col_to_letter.items()}  # Reverse mapping
    row_to_digit = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    digit_to_row = {v: k for k, v in row_to_digit.items()}  # Reverse mapping

    @staticmethod
    def translate_to_chesslib(col, row):
        """
        Translate board indices to chess notation.

        Parameters:
            col (int): Column index.
            row (int): Row index.

        Returns:
            str: The chess notation for the given column and row.
        """
        col_traslated = TranslateMove.col_to_letter.get(col, '')
        row_traslated = TranslateMove.row_to_digit.get(row, '')
        return f'{col_traslated}{row_traslated}'

    @staticmethod
    def translate_to_interface(col, row):
        """
        Translate chess notation to board indices.

        Parameters:
            col (str): Column in chess notation.
            row (str): Row in chess notation.

        Returns:
            tuple: The board indices for the given column and row.
        """
        col_traslated = TranslateMove.letter_to_col.get(col, -1)
        row_traslated = TranslateMove.digit_to_row.get(row, -1)
        return (col_traslated, row_traslated)
