############################ IMPORT SECTION ##########################

import os
import time
import re
import copy
import pdb

######################### MISELANEUS SECTION ##########################
def clean():
    os.system('cls')

def sleep(seconds = 1):
    time.sleep(seconds)

def get_option(input_msg = 'chose an option:'):
    """
    solicite to the user the option in integer value

    RETURNS
    ---------
        option - integer
            the option given by the user
    """
    option =  input(input_msg)

    while True:
        if option.isdigit():
            option = int(option)
            break
        print('Error: the input is not a int')
        option =  input(input_msg)

    return option

def check_bounds(index, init = 0, end = 1):
    """
    if the index of the is out from init and end interval it return None
    """
    if index >= init and index <= end:
        return index
    return None

def list_union(list1, list2):
    newlist = list1
    for elem in list2:
        if not elem in newlist:
            newlist.append(elem)
    return newlist

def anykey():
    input('press any input for exit:')

############################ DEV SECTION ##########################
def get_equation_by_str(equation_str):
    """
    for convert a string into a dictionary with number values

    Parameters
    -----------
        equation_str - string
            -string with the equations writer in form of '1x + 3y - 5z = 10'
    Returns
    ----------
        equation_dict - dictionary
            -a dictionary with varables like x,y,z as keys asigned the numerical
            variables, aswell in const key for the independent varible
    """
    #separation the equality
    param, const = re.split(r'=',equation_str ,2)
    #delete the white spaces
    param = re.sub('\s', '', param)
    #create the pattern for separate the equation Parameters
    pattern = re.compile(r'(?P<num>[-+]?[0-9]*)(?P<var>[a-z])')
    #find the separated parameters
    params = pattern.finditer(param)

    equation_dict = {}
    #save the params data on equation_dict
    for parameter in params:
        num = parameter.group('num')
        if not bool(re.search(r'\d', num)):
            num += '1'
        num = int(num)
        var = parameter.group('var')
        equation_dict[var] = num
    equation_dict['const'] = int(const)

    return equation_dict

class equation():
    """
    this class constains and magnament the equation dictionary
    provide of methods for manipulating the dictionary
    sum and multiplication.
    """
    def __init__(self, equation):
        """
        This class can be initializese a equation by a equations
        dictionary or a equation string.

        Parameters
        -----------
            -Equation - string - optional
                -if equation is not define it by default take the equations
                in the form of 1x=0 by default
                -if the equation is a string has to have this form
                'ax + by + ... + cz = d'
        """
        if equation is None:
            equation = 'x + y = 0'

        self.equation_dict = get_equation_by_str(equation)
        #default varible order.
        self.variable_order = 'xyzuvwrstqpabcdefghijklmno'
        self.order_varibles()

    def addvars(self, var_dict):
        self.equation_dict.update(var_dict)
        self.order_varibles()

    def deletevars(self, var_list):
        for v in var_list:
            if v != 'const':
                self.equation_dict.pop(v, None)

    def order_varibles(self, variable_order = None):
        """
        this is for order the variables in the dictionary for standarize
        the order of variables in all equations of this class

        Parameters
        ----------
            - variable_order - optional
                -the variable order is defined by a existing string in This
                class but if is needed a new order you can specify that here
        """
        #check if varible is diferent than default
        if variable_order is None:
            variable_order = self.variable_order
        else:
            self.variable_order = variable_order

        dict_keys = self.equation_dict.keys()
        ordered_keys = []

        #make a list with ordered keys
        for v in variable_order:
            if v in dict_keys:
                ordered_keys.append(v)
        #create a new dictionary with ordered varables
        new_dict = {}
        for key in ordered_keys:
            new_dict[key] = self.equation_dict[key]
        new_dict['const'] = self.equation_dict['const']
        #replace the actual dictionary by the new
        self.equation_dict = new_dict

    def get_variables_list(self):
        return self.equation_dict.keys()

    def get_parameters_list(self):
        return self.equation_dict.values()

    def get_dictionary(self):
        return self.equation_dict

    #equation operations
    def multiply(self, multiplier):
        """
        mulpiplicate every variables in the equation by
        a number called multiplier
        """
        for key in self.equation_dict.keys():
            self.equation_dict[key] *= multiplier

    def sum(self, eq_dict):
        """
        Sum the dictionary of this class and multiply by the variable
        of the eq_dictionary
        """
        #get two keys list
        dict_keys = self.equation_dict.keys()
        eq_dict_keys = eq_dict.keys()

        #intercetate the 2 lists
        common_keys = []

        for key in dict_keys:
            if key in eq_dict_keys:
                common_keys.append(key)
        #sum in the common keys
        for key in common_keys:
            self.equation_dict[key] += eq_dict[key]

    def __add__(self, equation2):
        """
        it do the same thing that self.sum() method but it returns a new object
        """
        new_equation = copy.deepcopy(self)
        new_equation.sum(equation2.get_dictionary())
        return new_equation

    def __mul__(self, multiplier):
        """
        it do the same thing that self.multiply() method but it returns a new object
        """
        new_equation = copy.deepcopy(self)
        new_equation.multiply(multiplier)
        return new_equation

    def __str__(self):
        str_representation = ''
        for key, value in self.equation_dict.items():
            if key != 'const':
                str_representation += '{0:+}{1}'.format(value, key)
        str_representation += ' = {0:+}'.format(self.equation_dict['const'])
        return str_representation

    def __repr__(self):
        return '<{} --> equation object>'.format(str(self))


class matrix():
    """
    This class is for create a matrix object for englobate
    the matrix operations print and get the actual equations
    """
    def __init__(self, equations):
        """
        this initialize the equation find all the variables in equations and uniform it
        varables in all equations.

        Parameters
        -----------
            - equations - equation objects list
        """
        self.equations = equations
        self.system_variables = None
        self.search_all_system_variables()
        self.uniform_equations()

    def updatematrix(self):
        self.search_all_system_variables()
        self.uniform_equations()

    def search_all_system_variables(self):
        system_variables = []
        #search all the system variables in equations object list.
        for equation in self.equations:
            for key in equation.get_variables_list():
                if not key in system_variables:
                    system_variables.append(key)
        #create or assing all the system variables
        self.system_variables = system_variables

    def uniform_equations(self):
        """
        this add the variables in each equation for make what every ecuation
        constains the same variables.
        """
        for equation in self.equations:
            #search the unexisted variables in equation
            variables_to_add = []
            for var in self.system_variables:
                if not var in equation.get_variables_list():
                    variables_to_add.append(var)
            #create variable to add in list format
            dict_to_add = {}
            for var in variables_to_add:
                dict_to_add.update({var:0})
            #add variables
            equation.addvars(dict_to_add)

    def addequation(self, equations):
        self.equations += equations
        self.updatematrix()

    def deleteequation(self, equations):
        for eq in equations:
            eq = eq - 1
            if check_bounds(eq, end = len(self.equations)):
                del self.equations[eq]
            else:
                print('Error: out of bounds index in deleteequation')
        self.updatematrix()

    def sum_equations(self, eq1, eq2, multiplier = 1):
        """
        This method is for sum to a equiton  a multiply of any other equation

        Parameters
        ----------
            eq1 - integer
                The position in equation list counting in 1 to n not 0 to n-1
                n is the amount of equations. it define to what equation is be
                aplied the sum
            eq2 - integer
                The position in equation list counting in 1 to n not 0 to n-1
                n is the amount of equations. it define the equiton will be sum to
                eq1.
            multiplier - integer - optional
                the number to multiply to eq2
        """
        eq1 = eq1 - 1
        eq2 = eq2 - 1
        self.equations[eq1].sum((self.equations[eq2] * multiplier).get_dictionary())


    def mul_equation(self, eq, multiplier):
        eq = eq - 1
        self.equations[eq].multiply(multiplier)

    def change_equations(self, eq1, eq2):
        eq1 = eq1 - 1
        eq2 = eq2 - 1
        self.equations[eq1], self.equations[eq2] = self.equations[eq2], self.equations[eq1]

    def get_equation(self, equation):
        equation = equation - 1
        return self.equations[equation]

    def get_matrix_representation(self):
        #search the most large numbers in digits in the equations
        spaces = [1 for x in range(len(self.system_variables))]

        for eq in self.equations:
            eq_vals = eq.get_parameters_list()

            for i, val in enumerate(eq_vals):
                if len(str(val)) > spaces[i]:
                    spaces[i] = len(str(val))
        #normalize the spaces in base to 1 length.
        spaces = [x + 1 for x in spaces]
        #create the representation str
        representation = ''
        for i, eq in enumerate(self.equations):
            representation_line = '|'
            eq_vals = eq.get_parameters_list()
            for j, val in enumerate(eq_vals):
                white_spaces = ' '*(spaces[j] - len(str(val)))
                representation_line += '{:.2f}{}'.format(val, white_spaces)
            representation_line += '|  ({})\n'.format(i + 1)
            representation += representation_line
        return representation


def equation_system_input():
    print('Please enter the linear equations in format:')
    print('ax + by + ... + cz = d')
    print('introduce ( d ) for Done')

    equations = []

    i = 1
    while True:
        equation_str = input('set the {} equation:'.format(i))
        if equation_str == 'd':
            print('Abort the prosses')
            break
        else:
            eq = equation(equation_str)
            equations.append(eq)
        i += 1

    return equations

def default_system():
    eq1 = equation('3x+2y+2z=5')
    eq2 = equation('x+3y+3z=10')
    eq3 = equation('5x-6y+20z=20')
    return [eq1, eq2, eq3]

def print_help():
    print('-----Help-----')
    print('-----Basic commands')
    print('h - for get help about the commands')
    print('s - show actual matrix')
    print('q - for exit')
    print('-----Matrix elemental operations commands')
    print('ch [eq1] [eq2] -- Sawp 2 equations')
    print('sum [eq1] [eq2] [multiplier] - sum to eq1 to parameters of eq2')
    print('                               multiplied by the  multiplier')
    print('mul [eq] [multiplier]        - multiply the parameters of eq')
    print('                               multiplied by the  multiplier')
    print('div [eq] [divider]           - divide the parameters of eq')
    print('                               divided by the divider')

def execute_command(command_str, system_matrix):
    change_command = 'ch'
    sum_command = 'sum'
    mul_command = 'mul'
    div_command = 'div'

    if bool(re.match(change_command, command_str)):
        command_elements = re.split(' ',command_str)
        eq1_id = int(command_elements[1])
        eq2_id = int(command_elements[2])
        system_matrix.change_equations(eq1_id, eq2_id)
    elif bool(re.match(sum_command, command_str)):
        command_elements = re.split(' ',command_str)
        eq1_id = int(command_elements[1])
        eq2_id = int(command_elements[2])
        #operator = command_elements[3]
        multiplier = int(command_elements[3])
        #if operator == '*':
        system_matrix.sum_equations(eq1_id, eq2_id, multiplier)
        #elif operator == '/':
            #system_matrix.sum_equations(eq1_id, eq2_id, float(1/multiplier))

    elif bool(re.match(mul_command, command_str)):
        command_elements = re.split(' ',command_str)
        eq_id = int(command_elements[1])
        multiplier = int(command_elements[2])
        system_matrix.mul_equation(eq_id, multiplier)


    elif bool(re.match(div_command, div_command)):
        command_elements = re.split(' ',command_str)
        eq_id = int(command_elements[1])
        divider = int(command_elements[2])
        system_matrix.mul_equation(eq_id, float(1/divider))

def solve_screen():
    clean()
    print('-----Linear matrix equations solve-----')
    print('n - for introduce new equation system')
    print('d - for load the default system')
    print('q - for exit')

    option = input('introduce your option:')

    equations = None

    if option == 'n':
        equations = equation_system_input()
    elif option == 'd':
        equations = default_system()
    elif option == 'q':
        return None
    else:
        print('No valid input the default_system is loaded')
    if equations is None:
        equations = default_system()
    #create system_matrix
    clean()
    print('-----Linear matrix equations solve-----')
    print('h - for get help about the commands')
    print('s - show actual matrix')
    print('q - for exit')
    print('-----------------')
    print('Original Matrix')
    system_matrix = matrix(equations)

    print(system_matrix.get_matrix_representation())

    #working loop
    while True:
        option = input('>>:')
        if option == 'h':
            print_help()
        elif option == 'q':
            print('Final Matrix')
            print('-------------')
            print(system_matrix.get_matrix_representation())
            break
        elif option == 's':
            print('Actual Matrix')
            print('-------------')
            print(system_matrix.get_matrix_representation())
        else:
            execute_command(option, system_matrix)
            print(system_matrix.get_matrix_representation())
    anykey()


############################## TESTING SECTION ##########################

def test_equation_class():
    """
    Test the equation class in its methods
    """
    eq1 = '+1x + 3y + 5z = 3'
    eq2 = '-14x + 7y = 10'
    eq3 = '-23x - 34y + 23z + 50w = 90'
    pdb.set_trace()
    eq1 = equation(eq1)
    eq2 = equation(eq2)
    eq3 = eq1 + eq2
    eq3 =  equation(eq3)

def test_matrix_class():
    eq1 = equation('+1x + 3y + 5z = 3')
    eq2 = equation('-14x + 7y = 10')
    eq3 =  equation('-23x - 34y + 23z + 50w = 90')
    equations = [eq1, eq2, eq3]
    system_matrix = matrix(equations)

    print(system_matrix.get_matrix_representation())
    pdb.set_trace()
    print('end test')



def test_get_equation_by_str():
    """
    this is for testing the convertion betwen string equation to a dictionary
    version with numerical values.
    """

    eq1 = '+1x + 3y + 5z = 3'
    eq2 = '-14x + 7y = 10'
    eq3 = '-23x - 34y + 23z + 50w = 90'

    print('test in text equations')
    print(eq1)
    print(eq2)
    print(eq3)

    print('dictionary version')
    print(get_equation_by_str(eq1))
    print(get_equation_by_str(eq2))
    print(get_equation_by_str(eq3))


fuctions_to_test = [test_get_equation_by_str, test_equation_class, test_matrix_class]

def test_mode():
    """
    screen for testing the fuctions of this program
    """
    clean()
    print('q: for exit')

    #print all test posibles.
    for i, func in enumerate(fuctions_to_test):
        print('{} - for test {} fuction'.format(i, func.__name__))
    #get the option in input
    option =  get_option()
    #check the bounds in fuction list length
    option = check_bounds(int(option), end = len(fuctions_to_test))
    if option is not None:
        #execute the choose fuction
        fuctions_to_test[option]()
        anykey()
    else:
        print('Error: chosen an unexist option')
        sleep()

############################## MAIN SECTION ###########################

def main_menu():
    while True:
        clean()
        print('Welcome to the linear sistem solver --- WIP')
        print('1 - Solve linear sytem by matrix')
        print('t - test [dev option]')
        print('q - exit')


        res = input('chose your option:')

        if res == str(1):
            solve_screen()
        elif res == 'q':
            clean()
            break
        elif res == 't':
            test_mode()
        else:
            print('Not exist this option try again')
            sleep()

    print('End the program')

def main_func():
    main_menu()

if __name__ == "__main__":
    main_func()
