import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.color import Color
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._winner = Color(0, 0, 0)
    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        """Updates the score nd moves the food if the snake collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # scores
        scores = cast.get_actors("scores")
        score_red = scores[0]
        score_green = scores[1]
        # food
        food = cast.get_first_actor("foods")
        # cycles
        cycles = cast.get_actors("cycles")
        head_red = cycles[0].get_head()
        head_green = cycles[1].get_head()

        # red food collision
        if head_red.get_position().equals(food.get_position()):
            points = food.get_points()
            cycles[0].grow_tail(points)
            score_red.add_points(points)
            food.reset()
        # green food collision
        elif head_green.get_position().equals(food.get_position()):
            points = food.get_points()
            cycles[1].grow_tail(points)
            score_green.add_points(points)
            food.reset()
    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        
        cycles = cast.get_actors("cycles")
        # red
        head_red = cycles[0].get_segments()[0]
        segments_red = cycles[0].get_segments()[1:]
        # green
        head_green = cycles[1].get_segments()[0]
        segments_green = cycles[1].get_segments()[1:]
        
        
        for segment in segments_red:
            # green hits red
            if head_green.get_position().equals(segment.get_position()):
                self._is_game_over = True
                # red wins
                self._winner = constants.RED
            # red hits red
            elif head_red.get_position().equals(segment.get_position()):
                self._is_game_over = True
                # green wins
                self._winner = constants.GREEN
                

        for segment in segments_green:
            # red hits green
            if head_red.get_position().equals(segment.get_position()):
                self._is_game_over = True
                # green wins
                self._winner = constants.GREEN
            # green hits green
            elif head_green.get_position().equals(segment.get_position()):
                self._is_game_over = True
                # red wins
                self._winner = constants.RED

        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycles = cast.get_actors("cycles")
            segments_red = cycles[0].get_segments()
            segments_green = cycles[1].get_segments()
            food = cast.get_first_actor("foods")

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)
            
            # set game over message
            message = Actor()
            if self._winner == constants.RED:
                message.set_text("Red Wins!") 
            else: message.set_text("Green Wins!")

            message.set_position(position)
            cast.add_actor("messages", message)
            
            ## Turn losing cycle white
            # if red wins
            if self._winner == constants.RED:
                for segment in segments_green:
                    segment.set_color(constants.WHITE)
            # if green wins
            else:
                for segment in segments_red:
                    segment.set_color(constants.WHITE)
            food.set_color(constants.WHITE)