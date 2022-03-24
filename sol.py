class Sol:

    def __init__(self):
        self.__question = None
        self.__author_name = None
        self.__description = None
        self.__text = None
        self.__url = None

    def set_question(self, question):
        self.__question = question

    def set_author_name(self, author_name):
        self.__author_name = author_name

    def set_description(self, description):
        self.__description = description

    def set_text(self, text):
        self.__text = text

    def set_url(self, url):
        self.__url = url

    def get_question(self):
        return self.__question

    def get_author_name(self):
        return self.__author_name

    def get_description(self):
        return self.__description

    def get_text(self):
        return self.__text

    def get_url(self):
        return self.__url

