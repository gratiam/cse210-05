from game.scripting.action import Action
from game.scripting.draw_actors_action import DrawActorsAction

class MoveActorsAction(Action):
    """Methods:
    execute(self, cast, script)"""
    def execute(self, cast, script):
        """Moves the position of the actors."""
        actors = cast.get_all_actors()
        for actor in actors:
            actor.move_next()