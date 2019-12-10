import io
import numpy as np


class STFReader:
    def __init__(self):
        self.buffer = None
        self.value_array = {}
        self.key_array = {}
        self.char = ""

    def read_byte(self, num_bytes):
        buffer = self.buffer.read(num_bytes)

        # Set to 32bit and little endian byte order ('<' == lowest end of the byte takes precedence)
        dt = np.dtype(np.int32)
        dt = dt.newbyteorder('<')
        bytes = np.frombuffer(buffer, dtype=dt)
        return bytes

    def read_stf(self, file_data):

        self.buffer = io.BytesIO(file_data)

        # Skip first 9 bytes, then get row count
        self.buffer.read(9)
        row_count = self.read_byte(4)

        for i in range(row_count[0]):
            # Get row count, throw away the next 4 bytes, then get character count
            row_number = self.read_byte(4)
            self.read_byte(4)
            character_count = self.read_byte(4)

            for i in range(character_count[0]):
                # Get the character of the next 2 bytes (little endian byte order puts the 0 in
                # front, so the character returns correctly
                character = chr(self.buffer.read(2)[0])
                self.char = self.char + character
                self.value_array[row_number[0]] = self.char

            # Clear the character variable so it doesn't stack rows in your array
            self.char = ""

        for i in range(row_count[0]):
            # Get the row count and character counts
            row_number = self.read_byte(4)
            character_count = self.read_byte(4)

            for i in range(character_count[0]):
                # Get the character of the next 2 bytes (little endian byte order puts the 0 in
                # front, so the character returns correctly
                character = chr(self.buffer.read(1)[0])
                self.char = self.char + character
                self.key_array[row_number[0]] = self.char

            # Clear the character variable so it doesn't stack rows in your array
            self.char = ""

        data = {}
        # Iterate through arrays in a try/catch to catch missing row exceptions
        for i in range(row_count[0]):
            # If the value has no character count, return an empty string so the column has an actual value.
            # This prevents errors when printing or populating data.
            value = ""
            try:
                key = self.key_array[i + 1]
                value = self.value_array[i + 1]
                data[i] = [key, value]
            except:
                data[i] = [key, value]
            pass

        return data
