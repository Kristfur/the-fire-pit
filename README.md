# The Fire Pit
The Fire Pit is a fictional resturaunt based in Wexford, Ireland. This website is a place where customers can make an account and reserve tables at the resturaunt.
Customers can easily edit and/or cancel their reservations. The resturaunt staff have unique access to view and edit all reservations and they can edit the resturaunts seating capacity.

# Table of Contents
* [User Experience](#user-experience)
    * [Site Goals](#site-goals)
    * [User Stories](#user-stories)
    * [Agile Planning](#agile-planning)
        * [Milestones](#milestones)
* [Design](#design)
    * [Wireframes](#wireframes)
    * [Database Structure](#database-structure)
    * [Security](#security)
* [Features](#features)
    * [Features to Implement](#features-to-implement)
* [Technologies](#technologies)
* [Testing](#testing)
    * [PEP8 Validation](#pep8-validation)
    * [Unfixed Bugs](#unfixed-bugs)
    * [Notable (Fixed) Bugs](#notable-fixed-bugs)
* [Deployment](#deployment)
    * [Version Control](#version-control)
    * [Deployment to Heroku](#deployment-to-heroku)
    * [Clone the Repository Code Locally](#clone-the-repository-code-locally)
* [Credits](#credits)

# User Experience
## Site Goals
* To provide an easy way for customers to reserve tables at the resturaunt.
* To provide the staff with all the information reagrding the reservations.

## User Stories
* As a user, I want to make a reservation so that I have a table reserved for my group when I go out.
* As a user, I want to make changes to my reservation so that my reservation stays up-to-date with my plans.
* As a staff member, I want to see all reservations so that I can get the tables ready for the customers.
* As a staff memebr, I want to change any reservation, so that all reservations can stay up-to-date.
* As a staff member, I want to be able to change the capacity of the resturaunt, so that we can do outdoor dining and our reservation capacity reflects that.

User Story:
> As a user, I want to make a reservation so that I have a table reserved for my group when I go out.

Acceptance Criteria:
* The user can create and view their reservations with ease

Implementation:
* The user creates an account so that their bookings are visible to only them. The bookings page is easy to navigate to, from there the user can view and create their bookings easily.

User Story:
> As a user, I want to make changes to my reservation so that my reservation stays up-to-date with my plans.

Acceptance Criteria:
* The user can make changes to their reservation.

Implementation:
* From the bookings page, the user can edit and/or cancel each of their bookings with easy to follow prompts.

User Story:
> As a staff member, I want to see all reservations so that I can get the tables ready for the customers.

Acceptance Criteria:
* Only the staff memebers can view all reservations.

Implementation:
* The staff members have unique permissions wich allows them to view all reservations. The can search each reservation by booking reference and by date so that the resturaunt can run smoothly 

User Story:
> As a staff memebr, I want to change any reservation, so that all reservations can stay up-to-date.

Acceptance Criteria:
* Only the staff memebers can change all reservations.

Implementation:
* The staff members have uninque permissions to be able to edit and/or cancel a booking in case a customer calls by phone wanting to change their booking. This way the staff can change the booking and keep it up to date.

User Story:
> As a staff member, I want to be able to change the capacity of the resturaunt, so that we can do outdoor dining and our reservation capacity reflects that.

Acceptance Criteria:
* The staff can change the number of available tables for reservations.

Implementation:
* The staff can set the capacity and amount of three sizes of tables. They can add tables to the available tables so that they can have more reservations.

## Agile Planning

### Milestones
The project had 6 main milestones:
#### 1: Base Setup
#### 2: Stand Alone Pages
#### 3: Authentication
#### 4: Booking
#### 5: Deployment
#### 6: Documentation

# Features
## Features to Implement

# Design
## Wireframes
## Database Structure
## Security

# Technologies
- Codeanywhere
    - The game was developed using [Codeanywhere](https://app.codeanywhere.com/).

- GitHub
    - The source code is hosted on [GitHub](https://github.com/Kristfur/battleships).

- Git
    - Used for version control during the development of the game.

- Python
    - Python was the main language used
    - Python packages used:
        - colorama - Used to make colored text in the terminal.
        - pyfiglet - Used to create the title text.

- Heroku
    - The game is hosted on the heroku platform. The live link to the app is [here](https://battleships-kristfur.herokuapp.com/).

# Testing

## PEP8 Validation

## Unfixed Bugs

## Notable (Fixed) Bugs



# Deployment

## Version Control
The following Git commands were used throughout development:

    git add <file> 

Was used to add files to the staging area before they are committed.

    git commit -m "commit message"

Was used to commit changes to the local repository queue.

    git push

Was used to push all committed code to the remote repository on GitHub.

## Deployment to Heroku
The steps for deployment are:

1. Log in to or create your Heroku account
2. Fork or clone this repository
3. Create a new Heroku app
4. In the settings, add config vars
5. Link the Heroku app to the repository
6. Click Deploy

## Clone the Repository Code Locally

The steps to clone the repository are as follows:

1. From the repository, click the *code* drop down menu
2. Click on *HTTPS*
3. Copy the link
4. Open your IDE (that has git installed)
5. Paste the git command into the IDE terminal
6. The project is now cloned on your local machine

# Credits

Python packages: 
