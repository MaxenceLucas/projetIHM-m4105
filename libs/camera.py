class camera:
    def __init__(self, p, v):
        self.position   = p
        self.viewpoint  = v
        self.up         = [0, 1, 0]
        self.near       = .1
        self.far        = 2000

