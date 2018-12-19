class PublicModel(dict):
    def __init__(self, kwargs):
        if kwargs:
            super().__init__(kwargs)
            for k, v in kwargs.items():
                setattr(self, k, v)
