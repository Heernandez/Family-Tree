import unittest
import sys
import os
# Agregar la carpeta raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from person import Person
class TestPerson(unittest.TestCase):

    def setUp(self):
        # Configuración inicial antes de cada prueba
        self.person = Person(
            name="John",
            last_name="Doe",
            birth_date="1990-01-01",
            dead_date=None,
            gender="Male"
        )

    def test_initialization(self):
        # Verificar la inicialización de atributos
        self.assertEqual(self.person.name, "John")
        self.assertEqual(self.person.last_name, "Doe")
        self.assertEqual(self.person.birth_date, "1990-01-01")
        self.assertIsNone(self.person.dead_date)
        self.assertEqual(self.person.gender, "Male")
        self.assertIsNone(self.person.mother)
        self.assertIsNone(self.person.father)
        self.assertEqual(self.person.children, [])

    def test_set_parents(self):
        # Crear padres ficticios
        mother = Person(
            name="Jane",
            last_name="Smith",
            birth_date="1970-05-10",
            dead_date=None,
            gender="Female"
        )
        father = Person(
            name="Robert",
            last_name="Smith",
            birth_date="1968-07-15",
            dead_date=None,
            gender="Male"
        )
        # Asignar padres
        self.person.setParents(mother=mother, father=father)
        
        # Verificar que los padres se asignaron correctamente
        self.assertEqual(self.person.mother, mother)
        self.assertEqual(self.person.father, father)
        self.person.father.print_children()
        self.person.mother.print_children()
    
    def test_set_child(self):
        # Crear un hijo ficticio
        child = Person(
            name="Alice",
            last_name="Doe",
            birth_date="2020-01-01",
            dead_date=None,
            gender="Female"
        )
        
        # Verificar agregar hijo desde un padre (género masculino)
        self.person.gender = "Male"
        self.person.setChild(child=child)
        self.assertIn(child, self.person.children)
        self.assertEqual(child.father, self.person)
        self.assertIsNone(child.mother)

        # Crear otra persona como madre (género femenino)
        mother = Person(
            name="Jane",
            last_name="Smith",
            birth_date="1985-01-01",
            dead_date=None,
            gender="Female"
        )
        child2 = Person(
            name="Tom",
            last_name="Smith",
            birth_date="2021-05-01",
            dead_date=None,
            gender="Male"
        )
        mother.setChild(child=child2)
        self.assertIn(child2, mother.children)
        self.assertEqual(child2.mother, mother)
        self.assertIsNone(child2.father)

    def test_set_child_no_child(self):
        # Verificar comportamiento con child=None
        initial_children = len(self.person.children)
        self.person.setChild(child=None)
        self.assertEqual(len(self.person.children), initial_children)

    def test_string_representation(self):
        # Probar el método __str__
        self.assertEqual(str(self.person), "John")

if __name__ == "__main__":
    unittest.main()
