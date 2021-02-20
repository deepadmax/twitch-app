import socket
import ssl

from message import TwitchMessage


IRC_SERVER = 'irc.chat.twitch.tv'
IRC_PORT = 6697
    

class IRCBot:
    def __init__(self, user_token, username, channels):
        """
        Arguments:
            user_token: Twitch OAuth token
            username: Twitch username
            channels: which channels to connect to
        """

        self.user_token = user_token
        self.username = username
        self.channels = channels

    def is_connected(self):
        """Get connection status of socket"""
        return hasattr(self, 'irc')

    def send_command(self, command):
        """Send a command to IRC"""
        
        # Only print to console if not the password
        if not command.startswith('PASS'):
            print(f'< {command}')

        # Send command to IRC
        self.irc.send((command + '\r\n').encode())

    def send_message(self, channel, text):
        """Send a message to a channel"""
        self.send_command(f'PRIVMSG #{channel} : {text}')

    def connect(self):
        """Connect bot to the Twitch IRC over a socket"""

        # Connect to IRC
        self.irc = ssl.wrap_socket(socket.socket())
        self.irc.connect((IRC_SERVER, IRC_PORT))

        # Authenticate to Twitch
        self.send_command(f'PASS {self.user_token}')
        self.send_command(f'NICK {self.username}')

        # Connect to all channels
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
            print(f'Joined #{channel}')
            # self.send_message(channel, "Don't mind me! I'm just here to test.")

    def feed(self):
        """Receive messages from channels and loop over them"""

        # Connect if not already connect
        if not self.is_connected():
            self.connect()

        # Receive messages
        while True:
            messages = self.irc.recv(2048).decode()

            for raw_message in messages.split('\r\n'):
                # Ignore if empty
                if len(raw_message) == 0:
                    continue
                
                # Parse message
                twitch_message = TwitchMessage(raw_message)

                # PONG if Twitch PINGs the client
                # to make sure the connection is maintained
                if twitch_message.irc_command == 'PING':
                    self.send_command('PONG :tmi.twitch.tv')

                yield raw_message, twitch_message