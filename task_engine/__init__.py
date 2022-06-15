from task_engine.gears import Gear, GearError
from typing import Union, List


class TaskEngine:
    """ 
    Engine for executing task gearsets.

    Feed the gears using add_gear() or set_gears() methods.
    
    Execute the made gearset using execute() method.
    """

    def __init__(self, **params) -> None:
        self.__version__ = "0.0.1.DEV"
        self._gears = []
        self._initial_parameters = params if params else {}

    def version(self) -> str:
        """
        Returns the current engine version.
        """
        return self.__version__
    
    def get_gears(self) -> List[Gear]:
        """
        Returns a list of gears (gearset).
        """
        return self._gears
    
    def get_initial_params(self) -> dict:
        """
        Returns the set parameters.
        """
        return self._initial_parameters
    
    def add_gear(self, gear: Gear) -> List[Gear]:
        """
        Adds a gear to the gearset.
        """
        self._gears.append(gear)
        return self.get_gears()
    
    def set_gears(self, gear_set: List[Gear]) -> List[Gear]:
        """
        Rewrites the currect engine gearset with the newly provided one. 
        """
        self._gears = gear_set
        return self.get_gears()
    
    def set_params(self, params: dict) -> dict:
        """
        Rewrites the current engine parameters with the newly provided ones.
        """
        self._initial_parameters = params
        return self._initial_parameters
    
    def update_params(self, params: dict) -> dict:
        """
        Updates the engine parameters.
        If a parameter that user passes is not in the engine parameters, it gets added.
        If a parameter that user passes in is in the engine parameters, it gets rewritten.
        Nothing gets removed/deleted.
        """
        self._initial_parameters.update(params)
        return self._initial_parameters
    
    def execute(self) -> Union[dict, GearError]:
        """
        Execute the engine gearset. This is where the fun begins.
        """
        if len(self._gears) < 1:
            return self._initial_parameters

        last_output = self._initial_parameters
        for gear in self._gears:
            last_output = gear.execute(last_output)
        return last_output