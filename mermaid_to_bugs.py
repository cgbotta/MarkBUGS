# define an object called node_constant that has a value and a name
import collections.abc
from tokenize import tokenize
from io import BytesIO
from keyword import iskeyword


node_dict = {}

# TODO make all the fields align with what they are called in DoodleBUGS
# TODO start processing from the end []   


BUILT_IN_FUNCTIONS = [
    "step"
]


class node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.attributes = []
        self.type = None #TODO could make this a predefined enum or something
        self.density = None #TODO this one too 
        self.function = None #TODO and this one
        self.parents = []
        self.children = []
        self.name_only = False
    def __str__(self):
        rtn = f"Name: {self.name}\nValue: {self.value}\nType: {self.type}\nDensity: {self.density}\n"
        rtn = rtn + 'Parents: '
        for p in self.parents:
            rtn = rtn + p.name + ', '

        rtn = rtn + '\nChildren: '
        for c in self.children:
            rtn = rtn + c.name + ', '
        return rtn + '\n\n'

class connection:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
    def __str__(self):
        return f"Parent: {self.parent}\nChild: {self.child}\n\n"

def getSubstringBetweenTwoChars(ch1,ch2,str):
    if '[' not in str or ']' not in str:
        return None
    return str[str.find(ch1)+1:str.find(ch2)]

def addConnection(parent, child, model_to_create):
    parent_node = None
    child_node = None
    for component in model_to_create:
        if isinstance(component, node) and component.name == parent:
            parent_node = component
        if isinstance(component, node) and component.name == child:
            child_node = component
    if parent_node is None or child_node is None:
        raise ValueError("Invalid connection")
    
    parent_node.children.append(child_node)
    child_node.parents.append(parent_node)

def identify_connections(to_process):
    if len(to_process) == 1:
        return [[str.strip(n) for n in to_process[0].split(',')]]
    elif len(to_process) == 2:
        nodes = []
        parents = [str.strip(n) for n in to_process[0].split(',')]
        children = [str.strip(n) for n in to_process[1].split(',')]
        if len(parents) > 1 and len(children) > 1:
            raise ValueError("Cannot have multiple nodes on both sides of connection")
        for parent in parents:
            for child in children:
                nodes.append([parent, child])
        return nodes
    else:
        raise ValueError("Invalid number of components")

    
def translate_v1(mermaid_code):
    # Array of order to create everything, add stuff to this after each line of the file is processed
    model_to_create = []

    # File method
    # file = open(file="./example_graph.txt")
    # lines = file.readlines()

    # Split lines method
    lines = [str.strip(line) for line in mermaid_code.splitlines()]
    print(lines)
    # exit()


    connections = False
    for index, line in enumerate(lines):
        # if the first line does not start with "graph" then error
        if line == '\n' or line == '':
            continue
        if index == 0 and not line.startswith("graph"):
            raise ValueError("The first line must start with 'graph'")
        
        if index > 0:
            # Check if we have reached connections
            if '->' in line and connections is False:
                connections = True
            if '->' not in line and connections is True:
                raise ValueError("Defined node in connections section")

            if not connections:
                # Process all the nodes
                if '[' not in line or ']' not in line:
                    raise ValueError("Node definition does not have value")
                
                n = node('','')
                node_value = getSubstringBetweenTwoChars('[',']',line)
                if node_value.isnumeric():
                    n.value = float(node_value)
                else:
                    n.value = node_value

                # Process the name
                n.name = line[0:line.find(':')]
                
                #Process the list of attributes
                n.attributes = line[line.find(':')+1 : line.find('[')].split()
                
                for attribute in n.attributes:
                    attribute_pair = attribute.split('=')
                    
                    if attribute_pair[0] == 'type':
                        n.type = attribute_pair[1]
                    elif attribute_pair[0] == 'density':
                        n.density = attribute_pair[1]
                        n.type = 'stochastic'
                    else:
                        raise ValueError("Invalid attribute type")

                model_to_create.append(n)
                print(model_to_create)

            else:
                # Process all the connections 
                if '[' in line or ']' in line:
                    raise ValueError("Node values cannot be set in the connections section")
                
                parent = line[0:line.find('-->')].strip()
                child = line[line.find('-->') + 3:len(line)].strip()

                # c = connection(parent[0:parent.find(':')],child[0:child.find(':')])
                # model_to_create.append(c)
                parent = parent[0:parent.find(':')]
                child = child[0:child.find(':')]
                addConnection(parent, child, model_to_create)
        
    BUGS_code = 'model {\n'
    print(model_to_create)
    for component in model_to_create:
        # In this section, need to generate actual BUGS code
        print(component)

        if isinstance(component, node):
            n = component
            if n.type == 'constant':
                BUGS_code = BUGS_code + f'{n.name} <- {n.value}\n'
            elif n.type == 'logical':
                BUGS_code = BUGS_code + f'{n.name} <- ({n.value})\n'

            else:
                BUGS_code = BUGS_code + f'{n.name} ~ {n.density}({n.value})\n'


        else:
            print("Yah")
    BUGS_code = BUGS_code + '}'
    return BUGS_code

def update_graph(n: node):
    if n.name_only:
        return
    else:
        node_dict[n.name] = n

# TODO what I am trying to do it a put against a database, essentially. Should probably check each thing that I am updating
def parse_node(node_str : str):
    n = node('','')

    no_name = False
    no_attributes = False

    if node_str.find(':') == -1:
        no_attributes = True
        n.name = node_str
    else:
        n.name = node_str[0:node_str.find(':')]

    # try to load existing node
    if n.name in node_dict:
        n = node_dict[n.name]

    value = getSubstringBetweenTwoChars('[',']',node_str)
    if value is None:
        no_name = True
    elif value.isnumeric():
        n.value = float(value)
    else:
        n.value = value

    # Process the name
    if node_str.find(':') == -1:
        no_attributes = True
    else:
        #Process the list of attributes
        n.attributes = node_str[node_str.find(':')+1 : node_str.find('[')].split()

        # TODO should move this to beginning, then see if the syntax and fuinction options are correct for the given type
        for attribute in n.attributes:        
            if attribute == 'constant':
                n.type = 'constant'
            elif attribute == 'logical':
                n.type = 'logical'
                n.function = n.value
            elif attribute == 'stochastic':
                n.type = 'stochastic'
                n.density = n.value
            else:
                raise ValueError("Invalid attribute: ", attribute)
    
    if no_name and no_attributes:
        n.name_only = True

    return n
    
def create_nodes(array_of_nodes: str):
    if len(array_of_nodes) == 2:
        # This is a connection
        parent = parse_node(array_of_nodes[0])
        child = parse_node(array_of_nodes[1])

        if child not in parent.children:
            parent.children.append(child)
        if parent not in child.parents:
            child.parents.append(parent)

        return[parent, child]
        
    elif len(array_of_nodes) == 1:
        # This is simply a node, might want to do this to everyting
        return [parse_node(array_of_nodes[0])]

    else:
        raise ValueError("Internal Server Error: Only Nodes and Connections are allowed types")

# Translate input from Design 3 into BUGS
def translate_v2(mermaid_code):
    # Array of order to create everything, add stuff to this after each line of the file is processed
    nodes_to_process = []

    lines = [str.strip(line) for line in mermaid_code.splitlines()]
    
    for index, line in enumerate(lines):
        # Skip blank lines
        if line == '\n' or line == '':
            continue
        to_process = [line]
        if '->' in line:
            # Split into 2 halves to process
            to_process = [str.strip(piece) for piece in line.split('-->')] 
        # TODO send to function to return final array with all connections specified
        next_batch = identify_connections(to_process)
        for x in next_batch:
            nodes_to_process.append(x)
    print(nodes_to_process)

    #TODO now need to iterate over nodes_to_process and create the actual node objects with connections
    print("nodes_to_process",nodes_to_process)
    for element in nodes_to_process:
        node_objects = create_nodes(element)
        for node_update in node_objects:
            update_graph(node_update)
    
    for key, value in node_dict.items():
        print(key, value)
            

    BUGS_code = 'model {\n'
    for node_name, node_object in node_dict.items():
        if isinstance(node_object, node):
            n = node_object
        else:
            raise ValueError("Internal Server Error: Node is only accepted type")
        
        if n.type == 'constant':
            BUGS_code = BUGS_code + f'{n.name} <- {n.value}\n'
        elif n.type == 'logical':
            if len(n.parents) == 0:
                BUGS_code = BUGS_code + f'{n.name} <- ({n.value})\n'
            else:
                # if n.function == 'step':
                    # Identify possible variables to replace
                g = tokenize(BytesIO(n.value.encode("utf-8")).readline)
                possible_variables = []
                for toktype, tokval, st, end, _ in g:
                    if tokval.isidentifier():
                        possible_variables.append(tokval)
                print("possible_variables", possible_variables)

                for token in possible_variables:
                    if token in BUILT_IN_FUNCTIONS:
                        possible_variables.remove(token)
                print("possible_variables", possible_variables)

                if len(n.parents) != len(possible_variables):
                    raise ValueError(f"Number of parents does not equal number of variables in child: {n.parents} != {possible_variables}")
                updated_value = n.value
                print("updated value", updated_value)
                for index, val in enumerate(possible_variables):
                    print("val", val)
                    print("parent", n.parents[index].name)
                    updated_value = updated_value.replace(val, n.parents[index].name)
                print("updated value", updated_value)

                BUGS_code = BUGS_code + f'{n.name} <- ({updated_value})\n'

                # else:
                #     raise ValueError(f"Invalid logical function: {n.function}")
        elif n.type == 'stochastic':
            if len(n.parents) == 0:
                # TODO ??
                BUGS_code = BUGS_code + f'{n.name} <- ({n.value})\n'
            else:
                if n.density == 'dbin':
                    # Takes 2 arguments
                    if len(n.parents) == 2:
                        BUGS_code = BUGS_code + f'{n.name} <- dbin({n.parents[0].value},{n.parents[1].value})\n'
                    else:
                        raise ValueError(f"dbin requires 2 parents, recieved {len(n.parents)}")

                else:
                    raise ValueError(f"Invalid stochastic function: {n.density}")


    BUGS_code = BUGS_code + '}'
    return BUGS_code

def generate_mermaid():
    mermaid_code = 'graph TD\n'

    # # Process all nodes
    # for key, value in node_dict.items():
    #     mermaid_code = mermaid_code + f'{key}[{value.value}]\n'

    # # Process all connections
    # for key, value in node_dict.items():
    #     for child in value.children:
    #         mermaid_code = mermaid_code + f'{key}[{value.value}] --> {child.name}[{child.value}]\n'


    # Another version
    # Process all nodes
    for key, value in node_dict.items():
        mermaid_code = mermaid_code + f'{key}\n'

    # Process all connections
    for key, value in node_dict.items():
        for child in value.children:
            mermaid_code = mermaid_code + f'{key} --> {child.name}\n'


    return mermaid_code