from abc import ABC, abstractmethod


class AbstractState(ABC):

    def __init__(self, context):
        self._context = context

    @abstractmethod
    def validate(self, input):
        pass

    @abstractmethod
    def set_next_state(self):
        pass
