# Copper

## Behind the project

The Programmer's Hangout decided to have a month for everyone to build a diy server. As seen by the commits, I am a month behind it.

### Purpose

I have written a couple of toy webservers from scratch. One project was written in python and another in c++. I wanted to create a project using python async to further my understanding of async programming. 

This project is meant to follow the guide provided by TPH while also making it async

Since I'm using async, parts of TPH will not be used and asyncio abstraction will be used. I may comeback and rewrite to have a fully low level async python webserver, but not right now.

### Design

#### Core infrastructure
- main creates and starts Server
- on new connection, Server spawns Responders
- Responders read Request and generate Response

##### Request
- Request processes the headerline and headerfields
- required values in headerline (HTTP VERSION, METHOD, PATH) and headerfields (Content-Length) are processed and checked
- all headerfields are added to a dictionary
- If improper headerline is read, Error is generated immediately
- If required headerfields are missing, Error is generaeted immediately
- If Request is too long, error is generated immediately


##### Response
- Response Class represents a given response
- Different predefined responses are transformations on the Response Class


### Requirements

> python 3.8 or newer

### Installation

There currently is not an installation process to install this as a seperate standalone application. However, Copper can be ran by first installing the module using pip and then running the running the module. 

```
python -m Copper
```

### Development

It is highly recommended to use a virtual environment 







<!-- vim:set sw=4 ts=4 et: -->
