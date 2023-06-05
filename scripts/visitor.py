class Visitor:
    def __init__(self, id: str, name: str, surname: str, age: str, email: str):
        self.id = int(id)
        self.name = name
        self.surname = surname
        self.age = int(age)
        self.email = email

    def return_tuple(self):
        return (self.id, self.name, self.surname, self.age, self.email)

    def __repr__(self):
        return "visitor({}, {}, {}, {}, {})".format(self.id, self.name, self.surname, self.age, self.email)