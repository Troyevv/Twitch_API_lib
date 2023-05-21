TwitchAPI Library
The TwitchAPI library provides a simple way to interact with the Twitch API and retrieve information about streams, viewers, clips, and followers. It requires a valid Twitch username, client ID, and client secret to authenticate and make API requests.

Installation
You can install the TwitchAPI library using pip:

Copy code
pip install twitchapi
Usage
Here's an example of how to use the TwitchAPI library:

python
Copy code
from twitchapi import TwitchAPI

# Create an instance of the TwitchAPI class
twitch = TwitchAPI(username="example_user", client_id="your_client_id", client_secret="your_client_secret")

# Check if the stream is currently online
is_online = twitch.is_stream_online()
print(is_online)

# Get the URL of the channel's profile image
image_url = twitch.channel_image()
print(image_url)

# Get the number of viewers in the current stream
viewers_count = twitch.get_viewers_count()
print(viewers_count)

# Get the title of the current stream
title = twitch.get_title()
print(title)

# Get the name of the game being streamed
game_name = twitch.get_game()
print(game_name)

# Get the start time of the current stream
started_at = twitch.get_started_at()
print(started_at)

# Get the duration of the current stream in a specified timezone
duration = twitch.stream_duration(timezone="Europe/Moscow")
print(duration)

# Get information about the chatters in the current stream
chatters = twitch.get_chatters()
print(chatters)

# Create a clip of the current stream
clip_id = twitch.create_clip()
print(clip_id)

# Get information about clips based on specified parameters
clips = twitch.get_clips(started_at="2023-05-20T00:00:00Z", ended_at="2023-05-20T23:59:59Z")
print(clips)

# Get information about the followers of the streamer
followers = twitch.get_followers()
print(followers)
Make sure to replace "example_user", "your_client_id", and "your_client_secret" with your own Twitch username, client ID, and client secret.

Exceptions
The TwitchAPI library includes the following exceptions:

MissingParamsError: Raised when required parameters are missing for an API request.

APIError: Raised when an error occurs during an API request. Provides information about the status code and error message.

Documentation
For more detailed documentation, including method descriptions and parameter information, please refer to the TwitchAPI Library Documentation file.
