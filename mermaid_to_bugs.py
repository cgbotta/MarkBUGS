# define an object called node_constant that has a value and a name

# TODO make all the fields align with what they are called in DoodleBUGS
# TODO start processing from the end []   
class node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.attributes = []
        self.type = None #TODO could make this a predefined enum or something
        self.density = None #TODO this one too 
        self.parents = []
        self.children = []
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

    
def translate():
    # Array of order to create everything, add stuff to this after each line of the file is processed
    model_to_create = []
    print(model_to_create)

    file = open(file="./example_graph.txt")
    lines = file.readlines()

    connections = False
    for index, line in enumerate(lines):
        # if the first line does not start with "graph" then error
        if index == 0 and not line.startswith("graph"):
            raise ValueError("The first line must start with 'graph'")
        if line == '\n':
            continue
        
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
        
    BUGS_code = ''
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

    return BUGS_code