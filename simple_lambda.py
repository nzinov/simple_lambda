import string

def get_free(used):
    for el in string.ascii_lowercase:
        if not el in used:
            return el
    raise ValueError()

class Var:
    def __init__(self, name):
        self.name = name

    def replace(self, var, subst):
        if self.name == var:
            return subst
        return self

    def normalize(self):
        return self

    def __str__(self):
        return self.name

    def rename(self, old, new):
        if self.name == old:
            self.name = new

    def safe(self, used=None):
        if used is None:
            used = set()
        used.add(self.name)

class Lambda:
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
    def __init__(self, *arg):
        self.data = arg

    def replace(self, var, subst):
        return Call(*map(lambda x: x.replace(var, subst), self.data))

    def normalize(self):
        self.data = list(map(lambda x: x.normalize(), self.data))
        if type(self.data[0]) is Lambda:
            return self.data[0].call(self.data[1]).normalize()
        return self

    def __str__(self):
        return "({} {})".format(*self.data)

    def safe(self, used=None):
        if not used:
            used = set()
        for el in self.data:
            el.safe(used)

    def rename(self, old, new):
        for el in self.data:
            el.rename(old, new)
