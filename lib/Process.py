import multiprocessing


class Process(multiprocessing.Process):
    def __init__(self, **kwargs) -> None:
        super(Process, self).__init__(**kwargs)
        self._target = kwargs.get('target')

    @property
    def target_class(self) -> object:
        return self._target
