from json import dump, load


class Book:
    """класс, методами которого будут основные функции приложения и работа с бд """
    def __init__(self, title, author, year: int, db_adress:str):
        self.title = title
        self.author = author
        self.year = str(year)
        self.status_list = ['в наличии', 'выдана']
        self.db_adress =db_adress

    def load_database(self):
        """ метод для загрузки данных библиотеки из файла """
        with open(self.db_adress) as file:
            try:
                self.library = load(file)
            except:
                self.library = {}


    def save_to_database(self):
        """ метод для сохранения обработанных данных в файл нашей бд """
        with open(self.db_adress, 'w') as file:
            dump(self.library, file)


    def represent_results(self, book: dict):
        """ метод принимает словарь и выводит в терминал данные о книге"""
        return (f'Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, '
              f'Status: {book['status']}\n')


    def add_book(self):
        """метод добавляет данные о книге (экземпляр класса) и проверяет есть ли такая-же"""
        self.load_database()
        already_in = False
        try:
            for i in self.library['books'].values():
                if i['author'] == self.author and i['title'] == self.title and i['year'] == self.year:
                    already_in = True
        except:
            pass
        if already_in == False:
            try:
                self.library['id counter'] += 1
            # на случай, если в бд ничего нет
            except:
                self.library['id counter'] = 0
            try:
                self.library['books'][self.library['id counter']] = {'title': self.title, 'author': self.author,
                                                                     'year': self.year, 'status': self.status_list[0]}
                self.save_to_database()
            # на случай, если в бд ничего нет
            except:
                self.library['books'] = {}
                self.library['books'][self.library['id counter']] = {'title': self.title, 'author': self.author,
                                                                     'year': self.year, 'status': self.status_list[0]}
                self.save_to_database()

            return True
            print('Книга добавлена')
        else:
            print('Такая книга уже есть в библиотеке')

    def delete_book(self, id: int):
        """ метод принимает айди в формате инт, удаляет запись о данной книге, или пишет, что такой книги нет"""
        self.load_database()
        try:
            del self.library['books'][str(id)]
            self.save_to_database()
            print('Книга удалена')
            return True
        except:
            print('Book not found')

    def search_book(self, criterea, type: str):
        """ метод принимает критерий поиска и его значение и выводит все книги по
        заданному критерию, сообщает если таких нет"""
        self.load_database()
        answer_list = []
        found = False
        for key in self.library['books'].keys():
            if self.library['books'][key][type] == criterea:
                answer_list.append(self.library['books'][key])
                found = True
        if found == False:
            print(f'Книга с {type} {criterea} не найдена')
        else:
            answer = f'По запросу: {type} {criterea} найдены книги:'
            return True
            print(answer)
            # переменная дляя итерации по списку ключей(айди)
            counter = 0
            for i in answer_list:
                print(f'"id": {list(self.library['books'].keys())[counter]}')
                counter += 1
                print(self.represent_results(i))

    def get_all(self):
        """ метод возвращает все книги из бд или сообщает, если их там нет """
        self.load_database()
        if self.library['books'] == {} or self.library['books'] == None:
            print('Книг пока нет')
        try:
            for key in self.library['books'].items():
                print(f'id: {key[0]}, ')
                print(self.represent_results(key[1]))
        except:
            print('Книг пока нет')

    def update_status(self, id: int, new: str):
        """ метод принимает id и новый статус, меняет статус книги с указанным айди"""
        self.load_database()
        try:
            self.library['books'][str(id)]['status'] = new
            print('Статус установлен')
        except:
            print('Book not found')


book_instance = Book(1, 1, 1, 'database.json')
parameters_list = ['author', 'title', 'year']
status_list = ['в наличии', 'выдана']


def interaction(book_instance: Book, parameters_list: list, status_list: list):
    """  функия принимает экземпляр класса(не важнно какой), списки статусов и параметров и запускает цикл
    взаимодействия с пользователем"""
    #try:
    while 1 > 0:
            main = int(input("Добро пожаловать в библиотеку,"
                             "для продолжения введите цифру с нужной Вам опцией.\n"
                             "1 Добавление книги \n"
                             "2 Удаление книги \n"
                             "3 Поиск книги \n"
                             "4 Отображение всех книг \n"
                             "5 Изменение статуса книги \n"
                             "6 Выход из приложения\n"
                             "'main' - команда для выхода в главное меню на любой стадии программы \n"
                             ))
            if main == 1:

                while True:
                    title = input('Введите название ')
                    if title == 'main':
                        interaction(book_instance, parameters_list, status_list)
                    if len(title) > 0 and title != ' ':
                        break
                while True:
                    author = input('Введите автора ')
                    if author == 'main':
                        interaction(book_instance, parameters_list, status_list)
                    if len(author) > 0 and author != ' ':
                        break
                while True:
                    try:
                        year = int(input('Введите дату публикации '))
                        if year == 'main':
                            interaction(book_instance, parameters_list, status_list)
                        break
                    except:
                        pass
                book = Book(title, author, year,book_instance.db_adress)
                book.add_book()
            if main == 2:
                while True:
                    try:
                        id = int(input('Введите id книги '))
                        if id == 'main':
                            interaction(book_instance, parameters_list, status_list)
                        break
                    except:
                        pass
                book_instance.delete_book(id)
            if main == 3:
                while True:
                    type = input('Введите параметр, по которому хотите искать: \n'
                                 '"author", "title", "year" ')
                    if type == 'main':
                        interaction(book_instance, parameters_list, status_list)
                    if type in parameters_list:
                        break
                criterea = input('Введите значение параметра ')
                book_instance.search_book(criterea, type)
            if main == 4:
                book_instance.get_all()
            if main == 5:
                while True:
                    try:
                        id = input('Введите id книги ')
                        if id == 'main':
                            interaction(book_instance, parameters_list, status_list)
                        break
                    except:
                        pass
                while True:
                    status = input('Введите новый статус: \n'
                                   '"в наличии" или "выдана" ')
                    if status == 'main':
                        interaction(book_instance, parameters_list, status_list)
                    if status in status_list:
                        break
                book_instance.update_status(id, status)
            if main == 6:
                break
    #except:
            #print('Введите одну из указанных цифр')
            #interaction(book_instance, parameters_list, status_list)

if __name__ == "__main__":
 interaction(book_instance, parameters_list, status_list)
