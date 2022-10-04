
docx.Document('demo.docx')



#https://realpython.com/python3-object-oriented-programming/

class Dog:
    # Class attribute: to define properties that should have the same value for every class instance
    species = "Canis familiaris"

    def __init__(self, name, age):
        # Instance attributes: properties that vary from one instance to another
        self.name = name
        self.age = age

    def __str__(self):
        # Instance methods: functions that are defined inside a class and can only be called from an instance of that class. An instance method’s first parameter is always self.
        return f"{self.name} is {self.age} years old"

    def speak(self, sound):
        return f"{self.name} says {sound}"


#Methods like .__init__() and .__str__() are called dunder methods because they begin and end with double underscores.

#To pass arguments to the name and age parameters, put values into the parentheses after the class name:
# buddy = Dog("Buddy", 9)
# miles = Dog("Miles", 4)

#After you create the Dog instances, you can access their instance attributes using dot notation:
# buddy.age
