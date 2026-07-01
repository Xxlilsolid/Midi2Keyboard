import os
import sys

class Filey:
    def find_data_file(self, filename):
        if getattr(sys, "frozen", False):
            # The application is frozen
            datadir = sys.prefix
        else:
            # The application is not frozen
            # Change this bit to match where you store your data files:
            datadir = os.path.dirname(__file__)
        return os.path.join(datadir, filename)