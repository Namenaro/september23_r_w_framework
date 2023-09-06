class G:
    def __init__(self):
        self.ws = [3, 2 ,1]
        self.xs = ["a", "b", "c"]
        self.i=-1

    def __iter__(self):
        return self

    def __next__(self):
        self.i+=1
        if self.i>= len(self.ws):
            raise StopIteration
        return self.ws[self.i], self.xs[self.i]

g = G()
for w, x in g:
    print(str(w) + str(",") + str(x))