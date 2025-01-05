

class Person:

    def __init__(self,name,last_name,birth_date,dead_date="",gender="",age = 0,mother = None, father = None,couple = None,parent = None):
        # Personal Data
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.dead_date = dead_date
        self.gender = gender
        self.age = None
        
        # Familiar Data
        self.mother = mother
        self.father = father
        self.couple = couple
        self.children = []

    def print_children(self):
        print(f"the children of {self} are :")
        for child in self.children:
            print(child)

    def __str__(self):
        return self.name

    def setParents(self,mother=None,father=None):
        if(mother != None):
            self.mother = mother
            if(self not in self.mother.children):
                #print(f"child {self} wasnot in list of child of {self.mother}")
                self.mother.setChild(self)
            print(f"the mother of {self} is {mother}")
        if(father != None):
            self.father = father
            if(self not in self.father.children):
                #print(f"child {self} wasnot in list of child of {self.father}")
                self.father.setChild(self)
            print(f"the father of {self} is {father}")

    def setChild(self,child=None):
        if(child != None):
            self.children.append(child)
            if self.gender == "Male":
                if child.father == None:
                    child.setParents(mother=None,father=self)
                print(f"{self} is father of {child}")
            else:
                if child.mother == None:
                    child.setParents(mother=self,father=None)
                print(f"{self} is mother of {child}")
        
