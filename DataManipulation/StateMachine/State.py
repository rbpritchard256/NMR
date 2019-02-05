# StateMachine/State.py

class State(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self, name):
        self.name = name 

    def __str__(self):
        return self.name
