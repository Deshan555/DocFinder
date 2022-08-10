import os

import pickle

import PySimpleGUI as ui

ui.change_look_and_feel('Dark')


class Gui:

    def __init__(self):

        self.layout = [
            [ui.Text("Search Term", size=(10, 1)),

             ui.Input(size=(45, 1), focus=True, key="TERM"),

             ui.Radio('Contains', group_id='choice', key="CONTAINS", default=True),

             ui.Radio('StartsWith', group_id='choice', key="STARTSWITH"),

             ui.Radio('EndsWith', group_id='choice', key="ENDSWITH")],

             [ui.Text('Root Path', size=(10, 1)),

              ui.Input('C:/', size=(45, 1), key="FOLDER_PATH"),

              ui.FolderBrowse('Browse'),

              ui.Button('Re-Index', size=(10, 1), key="REINDEX_DATA"),

              ui.Button('Search', size=(10, 1), key="FINDER")],

             [ui.Output(size=(180, 40))]
        ]

        self.window = ui.Window('Finder').Layout(self.layout)


class file_finder:

    def __init__(self):

        self.file_index = []

        self.results = []

        self.matches = 0

        self.records = 0

    def new_index(self, values):

        """" create new index file and save that file """

        root_path = values['FOLDER_PATH']

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

    def search(self, val_dic):

        self.results.clear()

        self.matches = 0

        self.records = 0

        term = val_dic['TERM']

        for path, files in self.file_index:

            for file in files:

                self.records += 1

                if (val_dic['CONTAINS'] and term.lower() in file.lower() or
                        val_dic['STARTSWITH'] and file.lower().startswith(term.lower()) or
                        val_dic['ENDSWITH'] and file.lower().endswith(term.lower())):

                    result = path.replace('\\', '/') + '/' + file

                    self.results.append(result)

                    self.matches += 1

                else:
                    continue

        with open('search_results.txt', 'w') as file_source:

            for row in self.results:

                file_source.write(row + '\n')


def main():
    ''' The main loop for the program '''
    g = Gui()
    s = file_finder()
    s.load_existing_index() # load if exists, otherwise return empty list

    while True:
        event, values = g.window.read()

        if event is None:
            break
        if event == 'REINDEX_DATA':
            s.new_index(values)
            print()
            print(">> New index created")
            print()
        if event == 'FINDER':
            s.search(values)

            # print the results to output element
            print()
            for result in s.results:
                print(result)

            print()
            print(">> Searched {:,d} records and found {:,d} matches".format(s.records, s.matches))
            print(">> Results saved in working directory as search_results.txt.")


if __name__ == '__main__':
    print('Starting program...')
    main()