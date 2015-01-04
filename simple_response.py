import random
import re

from plugins.baseplugin import BasePlugin


class Plugin(BasePlugin):
    """Simple Chat Responses"""
    name = 'SimpleResponsePlugin'

    def configure(self, configuration):

        self.config = configuration.simple_response
        self.enabled = self.config != {}
        self.responses, self.messages, self.actions = {}, {}, {}

        if self.enabled:
            self.responses = self.config.responses or {}
            self.messages = self.config.messages or {}
            self.actions = self.config.actions or {}

    def _sayDo(self, channel, nick, block, key):
        """
        Randomly select a response from the matching object in the
        responses dict and says/does the result in the channel.
        """
        if not self.enabled:
            return

        response = self._randomResponse(block, key)
        if response:
            # format the response
            message = response[1].format(
                        caller=nick,
                        channel=channel,
                        nick=self.nick
                    )

            if response[0] == 'say':
                self.reply(channel, nick, message)
            else:
                self.action(channel if channel != self.nick else nick, message)

    def _randomResponse(self, block, key):
        """
        Randomly select a response from the matching key in the
        given 'block' dict and returns the result as a 2-tuple
        ('say'/'do', message) or None if the key is not found.
        Formats the response with {nick}, {channel}, and {caller}.
        """

        if key in block.keys():
            info = block[key]
            options = []

            # if response is a string, convert to 'say' commands
            if type(info) in [type(u''), type('')]:
                info = {'say': [info]}

            # if response is a list, convert to just 'say' commands
            elif type(info) == type([]):
                info = {'say': info}

            if 'say' in info:
                options += [('say', s) for s in info['say']]
            if 'do' in info:
                options += [('do', d) for d in info['do']]

            if len(options) > 0:
                return random.choice(options)

    def command_botsnack(self, user, nick, channel, rest):
        """Even bots need a little love sometimes"""
        self._sayDo(channel, nick, self.responses, 'gift')

    def onMessage(self, user, nick, channel, message, highlight):
        if not self.enabled:
            return

        # strip whitespace and make lowercase for comparing
        lower = message.lower().strip()

        # o/
        if lower.endswith('o/') and hasattr(self.config, 'high5_finish_chance'):
            if random.random() < self.config.high5_finish_chance:
                self._sayDo(channel, nick, self.responses, 'high5')

        # test against each message key as a regex
        for regex in self.messages.keys():
            match = re.search(self.formatDoc(regex), lower)
            if match:
                self._sayDo(channel, nick, self.messages, regex)

    def onUserAction(self, user, nick, channel, action):
        if not self.enabled:
            return

        # strip whitespace and make lowercase for comparing
        lower = action.lower().strip()

        # test against each action key as a regex
        for regex, response in self.actions.iteritems():
            match = re.search(self.formatDoc(regex), lower)
            if match:
                self._sayDo(channel, nick, self.actions, regex)
