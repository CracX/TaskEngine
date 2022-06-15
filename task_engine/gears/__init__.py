from typing import Union

class GearError:
    """
    Class for gears to return errors. This object is exclusevly used by Gears.
    Whenever a gear fails to execute it's code, it is going to return a GearError object.
    """
    def __init__(self, gear_name, message) -> None:
        self._gear_name = gear_name
        self._message = message
    
    def get_gear_name(self) -> str:
        """
        Returns the errored gear name
        """
        return self._gear_name
    
    def get_message(self) -> str:
        """
        Returns the error message
        """
        return self._message

    def get_error(self) -> str:
        """
        Returns the full error string
        """
        return f"ERROR > [{self.get_gear_name()}] {self.get_message()}"

class Gear:
    """
    Gear is a class that performs some kind of mini task. It takes in a dictionary as an input,
    processes it and returns the processed dictionary back to the engine.
    Collection of gears is called a gearset. 
    """
    def __init__(self) -> None:
        self._gear_name = "Gear"
        self._gear_version = "0.1"
    
    def execute(self, params: dict) -> Union[dict, GearError]:
        """
        Called by the engine when this gear is next in the gearset.
        This is a public function and SHOULD NOT be overwritten, as it includes event handlers.
        """
        self._on_before_execute(params)
        new_params = self._execute(params)
        if isinstance(new_params, GearError):
            self._on_after_execute(params, params, error=new_params)
            return new_params
        final_params = self._on_after_execute(params, new_params)
        return final_params
    
    def _execute(self, params: dict) -> Union[dict, GearError]:
        """
        This method is called whenever a public variant gets executed.
        This is a private function and sub-classes should overwrite this function
        to include the gear-specific instructions.
        """
        return params
    
    def error(self, message: str) -> GearError:
        """
        This method creates a GearError object, triggers the on_error event returns the
         GearError object.
        """
        _err = GearError(self._gear_name, message)
        self._on_error(_err)
        return _err
    
    def log(self, message: str) -> None:
        """
        Debug method that shoudl be used instead of print due to users ability to mute such messages.
        """
        print(f"INFO > [{self._gear_name}] {message}")
    
    def _on_error(self, error: GearError) -> None:
        """
        Event that is called whenever a gear returns an error.
        """
        pass
    
    def _on_before_execute(self, old_params) -> dict:
        """
        Event that is called after executing the public execute() method but before executing the private variant.
        """
        return old_params
    
    def _on_after_execute(self, old_params, new_params, error=None) -> dict:
        """
        Event that is called after executing the private execute() method.
        """
        return new_params