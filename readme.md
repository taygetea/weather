TermWeather
======
**TermWeather** shows you the weather in your terminal, and figures out what you mean. 

          _ __
       __( =  =- _     Tampa, FL
      (-       -  )_      ______   _____
     (  -=  - )   - =)   |____  | | ____|
    (_-= _(    =-    _)      / /  | |__
     -(_____-___ -_ _)      / /   |___ \
       /  /  /  /  /       / /     ___) |
        /  /  /  /        /_/     |____/
    
         Wed, 13 May 2015 22:02:22 -0400
         Wind: Calm
         


## Rationale

I didn't like having to leave my terminal to check the weather. But I didn't just want a couple boring lines of text either.


## Installation

First, make sure you're using Python 2.7.x. For the moment, clone the repository:

    $ git clone https://github.com/taygetea/weather.git
    
And then make weather.py executable:

    $ chmod +x weather.py
    
Optionally: Add the directory TermWeather is located in to your system PATH.


## Usage

    $ weather <time> <location>
If no time is chosen, the current time will be used. If no location is chosen, your location will be used. Time options at the moment are limited to:

    now, tomorrow, week


## Version 
* Version 0.1

