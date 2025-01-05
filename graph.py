from person import Person
from pyvis.network import Network


def inject_modal_logic(html_file):
    # Modificar el HTML generado por pyvis
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Insertar el código del modal en el HTML
    modal_code = """
    <!-- Modal para mostrar información del nodo -->
    <div class="modal fade" id="nodeInfoModal" tabindex="-1" aria-labelledby="nodeInfoModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="nodeInfoModalLabel">Información del Nodo</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="nodeInfoContent">
                    <!-- Aquí se llenará la información del nodo -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Script para manejar clics en nodos -->
    <script>
        network.on("click", function (params) {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const nodeData = nodes.get(nodeId);
                console.log(nodeData)
                // Extraer atributos personalizados
                const name = nodeData.data ? nodeData.data.name : "Desconocido";
                const last_name = nodeData.data ? nodeData.data.last_name : "Desconocido";
                const birth_date = nodeData.data ? nodeData.data.birth_date : "Desconocido";
                const dead_date = nodeData.data ? nodeData.data.dead_date : "Desconocido";
                // Actualizar contenido del modal
                document.getElementById("nodeInfoContent").innerHTML = `
                    <!-- <p><strong>ID:</strong> ${nodeId}</p> -->
                    <p><strong>Nombres:</strong> ${name}</p>
                    <p><strong>Apellidos:</strong> ${last_name}</p>
                    <p><strong>Fecha de Nacimiento:</strong> ${birth_date}</p>
                    <p><strong>Fecha de Defuncion:</strong> ${dead_date}</p>
                `;
                
                // Mostrar el modal
                new bootstrap.Modal(document.getElementById('nodeInfoModal')).show();
            }
        });
    </script>
    """

    # Incluir el código del modal antes del cierre de la etiqueta </body>
    updated_html = html_content.replace("</body>", modal_code + "</body>")

    # Guardar el archivo HTML modificado
    with open(html_file, "w") as file:
        file.write(updated_html)

# Función para agregar nodos de forma segura
def safe_add_node(net, node_id, **kwargs):
    nombre = node_id.name + " " + node_id.last_name
    node_id = id(node_id)
    # Verificar si el nodo ya existe
    if any(node["id"] == node_id for node in net.nodes):
        print(f"Nodo {nombre} con ID {node_id} ya existe.")
    else:
        net.add_node(node_id, **kwargs)
        print(f"Nodo {nombre} con ID {node_id} agregado.")

# Función para agregar nodos de forma segura
def safe_add_node_union(net, node_id, **kwargs):

    # Verificar si el nodo ya existe
    if any(node["id"] == node_id for node in net.nodes):
        print(f"Nodo con ID {node_id} ya existe.")
    else:
        net.add_node(node_id, **kwargs)
        print(f"Nodo con ID {node_id} agregado.")

def generate_family_tree(root_person, filename="family_tree.html"):
    net = Network(directed=True)

    def add_person_to_graph(person):
        if person:
            # Agregar nodo para la persona
            person_data = {
                        "name": person.name,
                        "last_name": person.last_name,
                        "birth_date": person.birth_date,
                        "dead_date": person.dead_date,
                    }
            safe_add_node(net,person, label=f"{person.name} {person.last_name}",data=person_data)
            # Agregar hijos al grafo
            for child in person.children:
                child_data = {
                        "name": child.name,
                        "last_name": child.last_name,
                        "birth_date": child.birth_date,
                        "dead_date": child.dead_date,
                    }
                safe_add_node(net,child, label=f"{child.name} {child.last_name}",data=child_data)
                #net.add_edge(id(person), id(child))
                if(person.gender == "Male"):
                    mother = child.mother
                    mother_data = {
                        "name": mother.name,
                        "last_name": mother.last_name,
                        "birth_date": mother.birth_date,
                        "dead_date": mother.dead_date,
                    }
                    safe_add_node(net,mother, label=f"{mother.name} {mother.last_name}", data=mother_data)
                    union_id = f"union_{id(person)}{id(mother)}"
                    safe_add_node_union(net, union_id, label="")
                    net.add_edge(id(mother), union_id)
                    net.add_edge(id(person), union_id)
                    
                    net.add_edge(union_id, id(child))
                else:
                    father = child.father
                    father_data = {
                        "name": father.name,
                        "last_name": father.last_name,
                        "birth_date": father.birth_date,
                        "dead_date": father.dead_date,
                    }
                    safe_add_node(net,father, label=f"{father.name} {father.last_name}",data=father_data)
                    union_id = f"union_{id(father)}{id(person)}"
                    safe_add_node_union(net, union_id, label="")
                    net.add_edge(id(father), union_id)
                    net.add_edge(id(person), union_id)
                    
                    net.add_edge(union_id, id(child))
                    
                    #net.add_edge(id(father), id(child))
                
                
                add_person_to_graph(child)

    # Construir el grafo comenzando desde la raíz
    add_person_to_graph(root_person)
    # Configuración para la visualización
    net.repulsion(node_distance=200, spring_length=300)
    # Configurar el diseño jerárquico (de arriba hacia abajo)
    net.set_options("""
    {   
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "UD", 
                "sortMethod": "directed" 
            }
        },
        "physics": {
            "enabled": true,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 200,
                "springConstant": 0.08
            },
            "minVelocity": 0.75
        }
    }
    """)
    # Guardar el resultado
    
    net.show(filename,notebook=False)
    inject_modal_logic(filename)

def desc_tree(subject,branch=0):
    #print(subject)
    for child in subject.children:
        #print(f"----{child}")
        asc_tree(child,branch)


def asc_tree(subject,branch):
    print(f"{'----'*branch} {subject.father}-{subject.mother}")
    branch+=1
    siblings_by_mother_and_father = list(set(subject.father.children) & set (subject.mother.children))
    for child in siblings_by_mother_and_father:
        print(f"{'----'*branch} {child}")
        desc_tree(child,branch+1)
        

abuelo = Person(name="Luis Antonio",
               last_name="Hernandez Moreno",
               birth_date="15-01-1956",
               dead_date="10-09-2020",
               gender="Male",
               )

abuela = Person(name="Mery Clotilde",
               last_name="Cañarte Valencia",
               birth_date="15-03-1976",
               dead_date="",
               gender="Female",
               )
padre = Person(name="Luis Antonio",
               last_name="Hernandez Cañarte",
               birth_date="15-01-1956",
               dead_date="10-09-2020",
               gender="Male",
               )

madre_1 = Person(name="Fabiola",
               last_name="Herrera Arredondo",
               birth_date="15-03-1976",
               dead_date="",
               gender="Female",
               )


madre_2 = Person(name="Patricia",
               last_name="Rodriguez",
               birth_date="15-03-1976",
               dead_date="",
               gender="Female",
               )

child_1 = Person(name="Luis",
               last_name="Hernandez Herrera",
               birth_date="02-02-1998",
               dead_date="",
               gender="Male",
               )

child_2 = Person(name="Leidy Lorena",
               last_name="Hernandez Rodriguez",
               birth_date="02-02-1998",
               dead_date="",
               gender="Female",
               )

padre.setParents(mother=abuela,father=abuelo)
child_1.setParents(mother=madre_1,father=padre)
child_2.setParents(mother=madre_2,father=padre)


desc_tree(abuela,0)
#asc_tree(padre)

generate_family_tree(abuelo)

