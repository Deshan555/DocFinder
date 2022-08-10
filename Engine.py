import os

import pickle


class file_finder:

    def __init__(self):

        self.file_index = []

        self.results = []

        self.matches = 0

        self.records = 0

    def new_index(self, root_path):

        """" create new index file and save that file """

        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        """" save that file with details"""

        with open('file_index.pkl', 'wb') as source_file:

            pickle.dump(self.file_index, source_file)

    def load_existing_index(self):

        try:
            with open("file_index.pkl", 'rb') as source_file:

                self.file_index = pickle.load(source_file)
        except:
            self.file_index = []

    def search(self, term, search_options = 'contains'):

