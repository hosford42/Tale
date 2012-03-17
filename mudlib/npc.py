"""
Non-Player-Character classes

Snakepit mud driver and mudlib - Copyright by Irmen de Jong (irmen@razorvine.net)
"""

from __future__ import print_function, division
from . import baseobjects
from . import languagetools
from .errors import ActionRefused


class NPC(baseobjects.Living):
    """
    Non-Player-Character: computer controlled entity.
    These are neutral or friendly, aggressive NPCs should be Monsters.
    """
    def __init__(self, name, gender, title=None, description=None, race="human"):
        super(NPC, self).__init__(name, gender, title, description, race)

    def allow(self, action, item, actor):
        """
        Validates that this living allows something to happen by someone, with a certain action (such as 'give').
        Raises ActionRefused('message') if the intended action was refused.
        Make sure the message contains the name or title of the item: it is meant to be shown to the player.
        By default, NPC refuse every special action on them.
        Recognised action types:
        - give (give it something)
        """
        super(NPC, self).allow(action, item, actor)
        if action == "give" and item:
            raise ActionRefused("%s doesn't want %s." % (languagetools.capital(self.title), item.title))
        raise ActionRefused("You can't do that.")


class Monster(NPC):
    """
    Special kind of NPC: a monster can be hostile and attack other Livings.
    Usually has Weapons, Armour, and attack actions.
    """
    def __init__(self, name, gender, race, title=None, description=None):
        super(Monster, self).__init__(name, gender, title, description, race)
        self.aggressive = True

    def start_attack(self, victim):
        """
        Starts attacking the given living until death ensues on either side
        """
        name = languagetools.capital(self.title)
        room_msg = "%s starts attacking %s!" % (name, victim.title)
        victim_msg = "%s starts attacking you!" % name
        attacker_msg = "You start attacking %s!" % victim.title
        victim.tell(victim_msg)
        victim.location.tell(room_msg, exclude_living=victim, specific_targets=[self], specific_target_msg=attacker_msg)
