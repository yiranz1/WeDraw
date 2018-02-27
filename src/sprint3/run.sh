#!/bin/bash
brew install redis  # Install Redis using Homebrew
ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents  # Enable Redis autostart

launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist  # Start Redis server via launchctl
# homebrew.mxcl.redis.plist contains reference to redis.conf file location: /usr/local/etc/redis.conf 

redis-server /usr/local/etc/redis.conf # Start Redis server using configuration file, Ctrl+C to stop
redis-cli ping # Check if the Redis server is running

#launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.redis.plist # Disable Redis autostart
