import string

def get_free(used):
    """
    Returns variable name that is not used yet

    Args:
        used: iterable of used variable names
    Returns:
        some unused variable name
    """
    for el in string.ascii_lowercase:
        if not el in used:
            return el
    raise ValueError()

class Var:
    """
    Variable term
    """
    def __init__(self, name):
        self.name = name

    def replace(self, var, subst):
        """
        Return term with variable replaced by term
        
        Args:
            var: variable name to be replaced
            subst: replacement term
        Returns:
            new term
        """
        if self.name == var:
            return subst
        return self

    def normalize(self):
        """
        Returns normalized term
        """
        return self

    def __str__(self):
        return self.name

    def rename(self, old, new):
        """
        Renames variable in the term
        
        Args:
            old: old variable name
            new: new variable name
        Returns:
            new term
        """
        if self.name == old:
            self.name = new

    def safe(self, used=None):
        """
        Renames variables to avoid collisions between variables
        inside the term and variables from 'used' set

        Args:
            used: set of already used variables
        Returns:
            new term
        """
        if used is None:
            used = set()
        used.add(self.name)

class Lambda:
    """
    Lambda term

    Represents term (λx.A)
    x - var
    A - body
    """
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def replace(self, var, subst):
        return Lambda(self.var, self.body.replace(var, subst))

    def call(self, arg):
        return self.body.replace(self.var, arg)

    def normalize(self):
        self.body.normalize()
        return self

    def __str__(self):
        return "(λ{}.{})".format(self.var, self.body)

    def rename(self, old, new):
        if self.var != old:
            self.body.rename(old, new)

    def safe(self, used=None):
        if used is None:
            used = set()
        if self.var in used:
            old = self.var
            self.var = get_free(used)
            self.body.rename(old, self.var)
        used.add(self.var)
        self.body.safe(used)

class Call:
    """
    Function call term
    
    Represents term (A B)
    A - func
    B - arg
    """
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def replace(self, var, subst):
        return Call(self.func.replace(var, subst), self.arg.replace(var, subst))

    def normalize(self):
        self.func = self.func.normalize()
        self.arg = self.arg.normalize()
        if type(self.func) is Lambda:
            return self.func.call(self.arg).normalize()
        return self

    def __str__(self):
        return "({} {})".format(self.func, self.arg)

    def safe(self, used=None):
        if not used:
            used = set()
        self.func.safe(used)
        self.arg.safe(used)

    def rename(self, old, new):
        self.func.rename(old, new)
        self.arg.rename(old, new)
