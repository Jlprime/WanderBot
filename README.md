# WanderBot
For Hack &amp; Roll 2022


## Inspiration

As avid travelers and people who generally enjoy finding new places in Singapore, we thought that we could make a simple *something* that will help those who wish to be spontaneous in a new and unfamiliar city, without being too imposing or complicated to use. That's why we chose Telegram, which is fast becoming a dominant messaging app in general.
---
## What it does
**WanderBot** provides the user with a *customised* 'itinerary' of sorts. In keeping with the spirit of spontaneity, this 'itinerary' is effectively a list of suggestions, rather a prescribed minute-by-minute schedule. The 'itinerary' is obtained either through geolocation^ - wherein the bot factors in the Telegram user's exact location and generates places-of-interest within a specified radius (default 5 km) - or through text search, which will generate according to a city's predetermined centre point.

The generated 'itinerary' itself consists of four sections. In order:
- Weather conditions in the specified location
- A first place-of-interest to visit (e.g. museum, park, mall, attraction etc.)
- A place for refreshment (e.g. bar, restaurant, cafe etc.)
- A second place-of-interest to visit *that will not be of the same type as the first one*.
Each section will have accompanying images and locations that can be accessed through Google Maps.

Every iteration of the generated 'itinerary' is randomly generated with each query, keeping the experience unpredictable and exciting. Users can choose to "Reroll" their itinerary if it is not to their liking, or change the radius of search (up to a maximum of 50 km). 

^The user will be prompted for permission before location is obtained.
---
## How we built it
Utilizing Python as the main language with some JSON to parse the called data, we implemented multiple APIs into our bot, including:
- **pyTelegrambotAPI**
- **OpenWeatherMap API** for weather data
- Google's **Places API** (Place Search and Place Photos) which is the backbone of the bot
- Geopy Python Package, which implements **Nominatim API** for geocoding
WanderBot is also hosted on **Heroku**.
---
## Challenges we ran into
The biggest challenge was also our biggest benefactor: Places API. As college students with less-than-desirable financial prospects, we had to rely on the free credit given to new Places API users for everything from testing to debugging. We had to therefore meticulously plan every step we do before even knowing if it works, just so that we avoid busting the limit and sending us both into bankruptcy. This was a particular issue with Photos, which costs more to request. (API was intensely useful, though, so thanks Google!)

Another challenge was figuring out how WanderBot may be utilized non-linearly, making exception handling somewhat of a monumental task. The aim was to minimize user input by simplifying the bot usage flow so that this problem can be avoided, but it ultimately still presented as an issue in the final product. We spent a lot of the last few hours rooting out these loopholes.

## Accomplishments that we're proud of
Frankly, getting everything to work in the first place, especially for two non-CS students (one a hackathon first-timer). We thought the seamless implementation of multiple non-trivial APIs into WanderBot would be something we would not be able to achieve in 24 hours, but somehow we pulled it off. We're very proud to have a usable, fairly polished product to show.

## What we learned
Three lessons, besides picking up technical skills in programming:
- *Google spits out pretty much exactly what you ask for, even if it's not what you want.* At one point, we thought we were completely done with the bot, until we tested by searching up "Paris" (France) - and having the refreshment point-of-interest be a "Café Paris" somewhere in New Jersey, United States. We then realized that overly accurate results ("cafes+paris" was the search term) are as unhelpful as inaccurate ones, so we had to rejig quite a bit of code there.
- *The code is more powerful than your well-laid plans.* Literally changed our flow at least a dozen times to accommodate the APIs, bugs, exceptions and the lot. Lots of snacks were consumed in the process.
- *Falling asleep on the floor at 3am is not good for your joints.* Just don't do it.

## What's next for WanderBot
A potential step forward is to allow users to store their favorite itineraries in a database of sorts. However, in the context of a Telebot this will be more complicated and should require a lot more expertise if it is even feasible. Another possible enhancement is to further tailor the results generated according to the weather of the day; clear days will see results like parks, beaches and the like, while rainy days will see bookstores, restaurants and spas, for example.
