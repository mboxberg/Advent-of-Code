class Communicator:
    def __init__(self, file=None):
        if file:
            self.load_buffer(file)
        else:
            self.buffer = None
            self.buffer_length = 0

    def load_buffer(self, file):
        with open(file) as buffer_file:
            self.buffer = buffer_file.readline()
        self.buffer_length = len(self.buffer)

    def get_start_marker_pos(self, marker_length):
        for i in range(marker_length, self.buffer_length):
            test_marker = self.buffer[i - marker_length:i]
            marker = True
            for character in test_marker:
                if test_marker.count(character) > 1:
                    marker = False
                    break
            if marker:
                return i
        return 0

    def get_start_of_package_marker_pos(self):
        return self.get_start_marker_pos(marker_length=4)

    def get_start_of_message_marker_pos(self):
        return self.get_start_marker_pos(marker_length=14)


if __name__ == "__main__":
    malfunctioning_device = Communicator("../dat/06")
    print(malfunctioning_device.get_start_of_package_marker_pos())
    print(malfunctioning_device.get_start_of_message_marker_pos())
