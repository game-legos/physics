from typing_extensions import Self
import typing
import abc
import typing
import enum

import pygame
from physics.types_ import Mass, Acceleration, Velocity, Position  # type: ignore


class Sides(enum.Enum):
    """
    An enum representing the sides of a rectangle.

    Args:
        RIGHT: The right side of the rectangle.
        LEFT: The left side of the rectangle.
        TOP: The top side of the rectangle.
        BOTTOM: The bottom side of the rectangle.
    """

    RIGHT = enum.auto()
    LEFT = enum.auto()
    TOP = enum.auto()
    BOTTOM = enum.auto()


class PhysicalEntity(abc.ABC):
    """
    Abstract Base Class to provide blueprint of an entity which is bound to physics.

    Attributes:
        mass: Mass of entity.
        acceleration: Acceleration of entity.
        velocity: Current velocity at which entity is travelling.
    """

    def __init__(
        self,
        mass: Mass,
        acceleration: Acceleration,
        initial_velocity: Velocity,
        position: Position,
        rect: typing.Optional[pygame.Rect] = None,
    ) -> None:
        self.mass = mass
        self.acceleration = acceleration
        self.velocity = pygame.Vector2(*initial_velocity)
        self.position = pygame.Vector2(*position)

        self.rect = rect
        self.collidable = self.rect != None

    def reset_collidable(self) -> None:
        """
        Resets the collidability of the object.
        """
        self.collidable = False

    def next_position(self) -> Position:
        """
        Returns the position of the entity in the next frame.
        """
        return self.position + self.velocity

    def would_collide_with(self, other_entity: Self) -> typing.Optional[Side]:
        """
        Checks if entity would collide with the other entity in the next frame,
        and returns the side in which the entity collides with.

        Args:
            other_entity: The other physical entity.

        Returns:
            The side of the hitbox in which the entity collides
            with the other entity, None if no collision happens.
        """

        if self.rect is None or other_entity.rect is None:
            raise TypeError(
                "Both PhysicalEntity objects must have a 'rect' attribute which is not None."
            )

        collides = self.rect.colliderect(other_entity.rect)
        if not collides:
            return None

        next_position = self.peak_position()
        other_next_position = other_entity.peak_position()

        if next_position.x <= other_next_position.x:
            return Side.RIGHT
        elif next_position.x > other_next_position.x:
            return Side.LEFT

        if next_position.y <= other_next_position.y:
            return Side.TOP
        elif next_position.t > other_next_position.y:
            return Side.BOTTOM


class World2D:
    """A class for handling movement and interaction of all entities in a 2D plane."""

    def __init__(self) -> None:
        self._entities: set[PhysicalEntity] = set()

    def add(self, entity: PhysicalEntity) -> None:
        """Adds an entity to the world.

        Args:
            entity: A physical entity to add to the world.
        """
        self._entities.add(entity)

    def update(self) -> None:
        """Updates the physical quantities of the PhysicalEntity objects."""
        for entity in self._entities:
            entity.velocity += entity.acceleration
            entity.position += entity.velocity
    

