class DeckGenerator:
    """
    A class used to generate a deck from an simple input file and write it to an output file.

    ...

    Attributes
    ----------
    input_file : str
        a string representing the path to the input file
    output_file : str
        a string representing the path to the output file
    last_number : int
        an integer representing the last number processed from the input file
    comment_line : str
        a string representing the current comment line being processed
    deck_line : str
        a string representing the current deck line being processed
    spacing_line : str
        a string representing the spacing line
    output : str
        a string representing the output to be written to the output file

    Methods
    -------
    is_all_spaces(string)
        Checks if a string consists only of spaces.
    write_to_output(comment_line, deck_line)
        Writes the comment line and deck line to the output.
    fill_with_spaces(field_content='0', desired_length=10)
        Fills a field with spaces to a desired length.
    process_line(line)
        Processes a line from the input file.
    generate_deck()
        Generates the deck from the input file and writes it to the output file.
    """

    def __init__(self, input_file, output_file):
        """
        Constructs all the necessary attributes for the DeckGenerator object.

        Parameters
        ----------
            input_file : str
                a string representing the path to the input file
            output_file : str
                a string representing the path to the output file
        """

        self.input_file = input_file
        self.output_file = output_file
        self.last_number = 0
        self.comment_line = ''
        self.deck_line = ''
        self.spacing_line = '#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|'
        self.output = self.spacing_line + '\n'

    @staticmethod
    def is_all_spaces(string):
        """
        Checks if a string consists only of spaces.

        Parameters
        ----------
            string : str
                a string to check

        Returns
        -------
            bool
                True if the string consists only of spaces, False otherwise
        """

        return not string.isspace()

    @staticmethod
    def write_to_output(comment_line, deck_line):
        """
        Writes the comment line and deck line to the output.

        Parameters
        ----------
            comment_line : str
                a string representing the comment line
            deck_line : str
                a string representing the deck line

        Returns
        -------
            str
                a string representing the comment line and deck line written to the output
        """

        comment_line = '#' + comment_line[1:]
        return comment_line + '\n' + deck_line + '\n'

    @staticmethod
    def fill_with_spaces(field_content='0', desired_length=10):
        """
        Fills a field with spaces to a desired length.

        Parameters
        ----------
            field_content : str, optional
                a string representing the field content (default is '0')
            desired_length : int, optional
                an integer representing the desired length (default is 10)

        Returns
        -------
            str
                a string representing the field content filled with spaces to the desired length
        """

        return f"{field_content:>{desired_length}}"

    def process_line(self, line):
        """
        Processes a line from the input file.

        Parameters
        ----------
            line : str
                a string representing a line from the input file
        """

        line = line.strip()
        if len(line) == 0:
            if len(self.comment_line) > 0 or len(self.deck_line) > 0:
                self.output += self.write_to_output(self.comment_line, self.deck_line)
                self.comment_line = ''
                self.deck_line = ''
                self.last_number = 0
            self.output += self.spacing_line + '\n'
        elif line[0].isdigit():
            values = [*line.split(' ', 2)]
            number = int(values[0])
            comment = values[1]
            default_value = values[2] if len(values) > 2 and self.is_all_spaces(values[2]) else '0'
            field_length = (number - self.last_number) * 10

            if field_length > 0:
                self.comment_line += self.fill_with_spaces(comment, field_length)
                self.deck_line += self.fill_with_spaces(default_value, field_length)
            else:
                self.output += self.write_to_output(self.comment_line, self.deck_line)
                self.comment_line = ''
                self.deck_line = ''
                self.last_number = 0
                field_length = (number - self.last_number) * 10
                self.comment_line += self.fill_with_spaces(comment, field_length)
                self.deck_line += self.fill_with_spaces(default_value, field_length)
            self.last_number = number
        else:
            self.output += line + '\n'

    def generate_deck(self):
        """
        Generates the deck from the input file and writes it formated to the output file.
        """

        with open(self.input_file, 'r') as file:
            content = file.readlines()

        for line in content:
            self.process_line(line)

        self.output += self.write_to_output(self.comment_line, self.deck_line)
        self.output += self.spacing_line + '\n'

        with open(self.output_file, 'w') as file:
            file.write(self.output)
        print('Done!')


if __name__ == '__main__':
    deck_generator = DeckGenerator('input_deck.txt', 'input_deck_formated.txt')
    deck_generator.generate_deck()
