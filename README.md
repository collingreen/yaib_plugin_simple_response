Yaib Simple Response Plugin
=================

A plugin for [yaib](https://github.com/collingreen/yaib) that provides some
simple responses for things said in chat. Can match messages and actions
against regular expressions, then respond with a random option from a list
specified in configuration. Also provides some helper tools for writing
custom commands and chat handlers in a similar fashion that require additional
logic.

Yaib can always respond with the same message, randomly pick from a list of
messages, or randomly pick from a list of messages and actions. All of the
responses are also formatted to replace '{nick}', '{channel}', and '{caller}'
so you can create responses that are much more immersive.

See the configuration options below for more details.

## Configuration
The Simple Response plugin is configured by adding a `simple_response` section
to the Yaib configuration file. An example is given at the bottom of this
section that demonstrates each of the different configuration types.

### Responses, Messages, and Actions
Each of these are dictionaries whose keys specify how Yaib should respond
in a given situation. These can be single strings, lists of strings, or
dicts with keys 'say' and 'do'. Yaib will randomly select from the
available options and say (or do!) the response in the channel.

The responses are all formatted with {nick}, {channel}, and {caller}, which
lets you specify output that includes the bot name or the channel in which
it is said, or the nick of the user who started the response without having
to write anything more than configuration.

#### Responses
The `responses` dict is used by the plugin internally. It expects 2 default
keys, `gift` and `high5`, which control how Yaib responds to `!botsnack`
and high fives.

For example, the !botsnack command simply calls
`self._sayDo(channel, nick, self.responses, 'gift')` and the `_sayDo`
function randomly picks from the options under the `gift` key and sends it
to the specified channel.

#### Messages and Actions
The `messages` and `actions` dicts are used to add custom messages to which
Yaib should respond. The keys for these dicts are regular expressions
(can include {nick}, which get formatted before the regex is run -- if your
bot name has regex control characters, you're going to have a bad time).
Anytime a message matches one of the regular expressions in
the `messages` dict or an action matches the `actions` dict, Yaib will
respond with a random message matching that regular expression.

For example, say we want to add two responses for Yaib. First, we want her to
reply to everyone who says 'hi Yaib'
to make Yaib say 'hi' back to any user who says hi to her. Secondly, we want her
to do an action '/me dances with ' anyone who does '/me dances'. This
configuration will result in the following exchange:
~~~
"simple_response": {
    "messages": {
        "hi,? {nick}": "hi, {caller}!"
    },
    "actions": {
        "dances": "dances with {caller}"
    }
}
~~~

~~~
collingreen: hi yaib
yaib: hi, collingreen
* collingreen dances
* yaib dances with collingreen
~~~

Note the regular expression in the messages key - the ,? will match zero or one
commas, so 'hi, yaib' and 'hi yaib' both result in Yaib's response.


### Botsnack
The Simple Response plugin adds a !botsnack command that responds with
entries from the `responses.gift` config.


### High Five
Yaib will jump in and finish high fives (any message ending with o/), at a
configurable rate. Set the `high5_regex` to configure exactly what is matched,
`high5_finish_chance` to change the frequency, and the `high5` block in
`responses` to control her actions.

`high5_regex`: 'o/'
`high5_finish_chance`: 0-1 chance to respond with \o to any matching message
`high5`: '\o'

### Example Config
Example config that demonstrates all of the different options:

    "simple_response": {
        "high5_regex": "(^|\\s+)[oO]/\\s*$",
        "high5_finish_chance": 0.25,
        "responses": {
            "gift": {
                "say": [
                    "yay!", "hey, thanks!", "mmmmm", "hooray!",
                    "Botsnack botsnack!", "nom nom nom"
                ],
                "do": ["jump for joy"]
            },
            "high5": "\\o"
        },
        "messages": {
            "i'?m not your friend,? buddy": "I'm not your buddy, guy!",
            "i'?m not your buddy,? guy": "I'm not your guy, friend!",
            "i'?m not your guy,? friend": "I'm not your friend, buddy!",
            "(<3|love|good|yay) {nick}": {
                "say": ["<3", ":D", "yay me!", "huzzah!"],
                "do": ["purrs", "beams with pride", "smiles"]
            }
        },
        "actions": {
            "(needs a hug)|(hugs {nick})": {"do": {"hugs {caller}"]}
        }
    }
