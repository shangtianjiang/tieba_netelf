class no_data(RuntimeError):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return repr(self.val)

