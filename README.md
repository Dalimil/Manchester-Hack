# Student Hack IV - Manchester (4-6th March 2016)

## This is the backend part of the app

### Name: Park Painter
### Tagline: Create and explore virtual art in local parks.

### Super-short summary for others: An app that allows users to geo-cache digital paintings in local parks.

### Project Goal:
Promote engagement in a local community by providing a fun new way to interact with parks in your city.

### Concept:
Users can share their experiences in local parks with others via collaborative art boards in each park. These boards can hold images, drawings, text (poems, thoughts, etc). The content of the boards can only be viewed or modified if the user is physically in the park at the location of the board’s creation.

### Architecture:
Yelp API to get Park locations, names, pictures, and other details
Back end = AWS server with custom API endpoints and database, sends data to iOS app via JSON
Font end = iOS app

### Basic UX Flow:

Users can see the park they are currently in and all of the boards within it (both on a map and in a list). They can then create a new board or modify an existing one. To modify one, they must be very close to the location where the board was created. Creating a board will place it at their current location.

Boards can be of two types: images or drawings. Images can be uploaded from the user’s device or taken within the app. Text can then be overlaid on the image (how artsy). Drawings allow users to touch and drag lines on the canvas, and change the pen color, stroke, etc.

Users can also see a list of parks nearby (from Yelp), along with their names, preview image, ratings, and distance from the user. A detail view of a park allows for more information (map, directions, larger images, open/close times, etc).

Users have a profile which includes their picture, name, and rank (with how many parks they have visited). The name and picture can be changed. They can also view all the ranks possible and share their current rank on social media.

### Additional Features (time-permitting):
• Users can ‘like’ boards by other people
• Boards display the image and name of those who created them
• Global list of recently added boards around the world
