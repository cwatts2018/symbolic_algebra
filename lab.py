"""
6.1010 Spring '23 Lab 10: Symbolic Algebra
"""

import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

class Symbol:
    """
    Represents an instance of an algebraic symbol.
    """
    precedence = 10
    right_parens = False
    left_parens = False
    
    def __add__(self, y):
        return Add(self, y)
   
    def __sub__(self, y):
        return Sub(self, y)
   
    def __mul__(self, y):
        return Mul(self, y)
   
    def __truediv__(self, y):
        return Div(self, y)
    
    def __pow__(self, y):
        return Pow(self, y)
   
    def __radd__(self, non):
        return Add(non, self)
   
    def __rsub__(self, non):
        return Sub(non, self)
    
    def __rmul__(self, non):
        return Mul(non, self)
    
    def __rtruediv__(self, non):
        return Div(non, self)
    
    def __rpow__(self, non):
        return Pow(non, self)
        
    def simplify(self):
        # print('HI')
        return self



class Var(Symbol):
    """
    Represents a variable.
    """
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"
    
    def calculate(self, mapping):
        for key in mapping:
            if key == self.name:
                return mapping[key]
        raise NameError
    
    def getAttribute(self):
        return self.name
    
    def __eq__(self, other):
        try:
            if self.name == other.name:
                return True
        except:
            return False
        return False
    
    def deriv(self, var):
        if var == self.name:
            return Num(1)
        return Num(0)
    
    def expression(self):
        return Var(self.name)

class Num(Symbol):
    """
    Represents a number.
    """
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
    
    def calculate(self, mapping):
        return self.n

    def getAttribute(self):
        return self.n
    
    def __eq__(self, other):
        try:
            if self.n == other.n:
                return True
        except:
            return False
        return False
    
    def deriv(self, var):
        return Num(0)
    
    def expression(self):
        return Var(self.n)

class BinOp(Symbol):
    """
    Represents a binary expression.
    """
    operand = "" #delete?
    def __init__(self, left, right):
        """
        Initializer. Stores Symbol instances
        as left and right hand operands
        """
        if isinstance(left, int) or isinstance(left, float):
            self.left = Num(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            self.left = left
        if isinstance(right, int) or isinstance(right, float):
            self.right = Num(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            self.right = right

    def __str__(self):
        l_prec = self.left.precedence
        r_prec = self.right.precedence
        def parens(prec, self_prec, string):
            if prec < self_prec:
                return "(" + string + ")"
            return string
        if l_prec == self.precedence and self.left_parens:
            result = "(" + str(self.left) + ")"
        else:
            result = parens(l_prec, self.precedence, str(self.left))
        result += " " + self.operand + " "
        if r_prec == self.precedence and self.right_parens:
            result += "(" + str(self.right) + ")"
        else:
            result += parens(r_prec, self.precedence, str(self.right))
        return result
    
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"
        
    def eval(self, mapping):
        return self.calculate(mapping)
    
    def __eq__(self, other):
        if isinstance(other, BinOp) and other.operand == self.operand:
            if self.left == other.left and self.right == other.right:
                return True
        return False


class Add(BinOp):
    """
    Represents a binary addition expression.
    """
    precedence = 1
    operand = "+"
    def calculate(self, mapping):
        """
        Calculates the expression.
        """
        return self.left.calculate(mapping) + self.right.calculate(mapping)
    
    def deriv(self, var):
        """
        Takes the derivative of the expression with respect to var.
        """
        #x+y
        return self.left.deriv(var) + self.right.deriv(var)
    
    def simplify(self):
        """
        Simplifies the expression.
        """
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()
        if left_simplified == Num(0):
            return right_simplified
        elif right_simplified == Num(0):
            return left_simplified
        else:
            try: 
                total = Add(left_simplified, right_simplified).eval({})
                return Num(total)
            except:
                return Add(left_simplified, right_simplified)
        
class Sub(BinOp):
    """
    Represents a binary subtration expression.
    """
    precedence = 1
    operand = "-"
    right_parens = True
    
    def calculate(self, mapping):
        """
        Calculates the expression.
        """
        return self.left.calculate(mapping) - self.right.calculate(mapping)
    
    def deriv(self, var):
        """
        Takes the derivative of the expression with respect to var.
        """
        #x-y
        return self.left.deriv(var) - self.right.deriv(var)
    
    def simplify(self):
        """
        Simplifies the expression.
        """
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()
        if right_simplified == Num(0):
            return left_simplified
        else:
            try: 
                # print('hererererererere')
                total = Sub(left_simplified, right_simplified).eval({})
                return Num(total)
            except:
                return Sub(left_simplified, right_simplified)
    

class Mul(BinOp):
    """
    Represents a binary multiplication expression.
    """
    precedence = 2
    operand = "*"
    def calculate(self, mapping):
        """
        Calculates the expression.
        """
        return self.left.calculate(mapping) * self.right.calculate(mapping)
    
    def deriv(self, var):
        """
        Takes the derivative of the expression with respect to var.
        """
        # x*y (x+2)*y
        return Add(Mul(self.right.deriv(var), self.left), Mul(self.left.deriv(var), self.right))

    def simplify(self):
        """
        Simplifies the expression.
        """
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()
        if left_simplified == Num(1):
            return right_simplified
        elif right_simplified == Num(1):
            return left_simplified
        elif left_simplified == Num(0) or right_simplified == Num(0):
            return Num(0)
        else:
            try: 
                total = Mul(left_simplified, right_simplified).eval({})
                return Num(total)
            except:
                return Mul(left_simplified, right_simplified)
        
        

class Div(BinOp):
    """
    Represents a binary division expression.
    """
    precedence = 2
    operand = "/"
    right_parens = True
    
    def calculate(self, mapping):
        """
        Calculates the expression.
        """
        return self.left.calculate(mapping) / self.right.calculate(mapping)
    
    def deriv(self, var):
        """
        Takes the derivative of the expression with respect to var.
        """
        # x*y (x+2)*y
        return Div(Sub(Mul(self.left.deriv(var), self.right), Mul(self.right.deriv(var), self.left)), Mul(self.right, self.right))

    def simplify(self):
        """
        Simplifies the expression.
        """
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()
        if right_simplified == Num(1):
            return left_simplified
        elif left_simplified == Num(0):
            return Num(0)
        else:
            try: 
                total = Div(left_simplified, right_simplified).eval({})
                return Num(total)
            except:
                return Div(left_simplified, right_simplified)

class Pow(BinOp):
    """
    Represents a binary power expression.
    """
    precedence = 3
    operand = "**"
    left_parens = True
    
    def calculate(self, mapping):
        """
        Calculates the expression.
        """
        return self.left.calculate(mapping) ** self.right.calculate(mapping)
    
    def deriv(self, var):
        """
        Takes the derivative of the expression with respect to var.
        """
        if not isinstance(self.right, Num):
            raise TypeError
        return Mul(Mul(self.right, Pow(self.left, self.right-1)), self.left.deriv(var))

    def simplify(self):
        """
        Simplifies the expression.
        """
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()
        if right_simplified == Num(1):
            return left_simplified
        elif right_simplified == Num(0):
            return Num(1)
        elif left_simplified == Num(0):
            return Num(0)
        else:
            try: 
                total = Pow(left_simplified, right_simplified).eval({})
                return Num(total)
            except:
                return Pow(left_simplified, right_simplified)

def expression(s):
    """
    Given a string representing an expression, converts it into a BinOp object.

    """
    def tokenize(s):
        """
        Tokenizes the string into a list of chars.
        """
        new_s = ""
        for char in s:
            if char == "(":
                new_s += "( "
            elif char == ")":
                new_s += " )"
            else:
                new_s += char
        tokens = new_s.split(" ")
        return tokens
    
    tokens = tokenize(s)
 
    def parse(tokens):
        """
        Parses the entire expression using recursion.
        """
        def parse_expression(index):
            """
            Parses an individual expression.
            """
            
            def get_parens_end(index):
                """
                Determines the end of an expression by returning the index
                of its closing parentheses.
                """
                open_par = 0
                close_par = 0
                for i in range(index, len(tokens)):
                    elt = tokens[i]
                    if elt == "(":
                        open_par += 1
                    elif elt == ")":
                        close_par += 1
                    # print('here', i, open_par, close_par)
                    if open_par == close_par:
                        return i
                    
            # print('start parse exp', index, tokens)
            if tokens[index] == "(":
                # print('token')
                i = get_parens_end(index)
                # print('last parens index', i)
                return (parse(tokens[index+1:i]), i+1) #parse(tokens[i+2:])), i+1)
            try:
                x = float(tokens[index])
                # print('num')
                return(Num(float(tokens[index])), index+1)
            except:
                # print('var')
                return(Var(tokens[index]), index+1)
           
        next_index = 0
        parsed_exp, next_index = parse_expression(next_index)
        next_index += 1
        while next_index < len(tokens):
            new_parsed_exp, new_next_index = parse_expression(next_index)
            op = tokens[next_index-1]
            if op == "*":
                parsed_exp = Mul(parsed_exp, new_parsed_exp)
            elif op == "/":
                parsed_exp = Div(parsed_exp, new_parsed_exp) 
            elif op == "+":
                parsed_exp = Add(parsed_exp, new_parsed_exp) 
            elif op == "-":
                parsed_exp = Sub(parsed_exp, new_parsed_exp)
            elif op == "**":
                parsed_exp = Pow(parsed_exp, new_parsed_exp)
            next_index = new_next_index+1
        
        return parsed_exp
  
    return parse(tokens)

if __name__ == "__main__":
    doctest.testmod()
    
 
