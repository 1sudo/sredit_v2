

class STFWriter:

    """
    Notes for values:
    -----------------------------------------------------------------------
    The first 9 bytes account for STF file validation (ABCD)
    The 10th and 11th reversed hex is the row count (or 16bit int on the 10th byte)
    -----------------------------------------------------------------------
    These iterate:
    4 more bytes afterwards count for the row number
    4 more bytes afterwards are all full 8bit bytes (255)
    4 more bytes afterwards count for the character count for the value
    The rest of the row consists of character count + 1 empty 8bit byte
    -----------------------------------------------------------------------
    """

    def __init__(self):
        self.b = bytearray()
        self.row_count = None
        self.character_count = None
        self.fname = None

    def parse_bytes(self, value, num_bytes=None):

        """
        There should never be a reason you would manually pass through a value higher than
        65535 - If you are, you're doing it wrong.
        """

        # Specify a number of bytes for the byte array
        if num_bytes is not None:
            x = value.to_bytes(num_bytes, 'little')
            self.b.extend(x)
        # 8 Bit
        elif value <= 255:
            self.b.extend([value])
        # 16 Bit
        elif (value > 255) and (value <= 65535):
            x = value.to_bytes(2, 'little')
            self.b.extend(x)
        # 24 Bit
        elif (value > 65535) and (value <= 16777215):
            x = value.to_bytes(3, 'little')
            self.b.extend(x)
        # 32 Bit
        elif (value > 16777215) and (value <= 335544319):
            x = value.to_bytes(4, 'little')
            self.b.extend(x)
        # 64 Bit
        else:
            x = value.to_bytes(8, 'little')
            self.b.extend(x)

    def save_data(self, data, filepath=None):

        # [205, 171] STF file validation (ABCD)
        self.b.extend([205, 171, 0, 0, 0, 0, 0, 0, 0])

        # Row count for values
        self.row_count = len(data)
        self.parse_bytes(self.row_count, 4)
        print("Row Count for value: {}".format(self.row_count))

        # Iterate through the VALUE rows
        for i in range(self.row_count):

            # Add the row number to the byte array
            self.parse_bytes(i + 1, 4)
            self.b.extend([255, 255, 255, 255])

            # Get character count for value of each row
            self.character_count = len(data[i][1])
            self.parse_bytes(self.character_count, 4)
            print("Character count for value: {}".format(self.character_count))

            # Iterate through characters in the row, parse their decimal values, and add an empty byte
            for i in data[i][1]:
                self.parse_bytes(ord(i))
                self.b.extend([0])

        # Iterate through KEY rows
        for i in range(self.row_count):

            # Add the row number to the byte array
            self.parse_bytes(i + 1, 4)

            # Get character count for key of each row
            self.character_count = len(data[i][0])
            self.parse_bytes(self.character_count, 4)
            print("Character count for key: {}".format(self.character_count))

            # Iterate through characters in the row and parse their decimal values
            for i in data[i][0]:
                self.parse_bytes(ord(i))

        if filepath is not None:
            output_file = open(filepath, "wb")
            output_file.write(self.b)
