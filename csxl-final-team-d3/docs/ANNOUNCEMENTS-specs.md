Authors: 

Ahmed Raiyan: https://github.com/ahmadraiyan039

Nawfal Mohamed: https://github.com/Nawfal547 

Zaid Kamdar: https://github.com/zkamdar1

Denizhan Killac: https://github.com/denizhankilic19

# Get Started with Announcement Feature!

## Model Used: Announcement

The main model that is utilized for our announcement feature:  

![example](./images/docpics/Announcement%20Model%20Picture.png)

The announcement model is specifically designed for setting up a data representation of all the factors needed for an announcement.  Each field used in this model is essential information needed for each announcement. For example, the headline, organization, and synopsis are all fields needed for every announcement that is posted so UNC CS students know what they are looking at. This allows for announcements to be properly distinguished and helps CS students to know what organization is posted and what events they want to go to.  

We also have implemented multiple API routes: 

| Type of API  | Purpose |
| ------------- | ------------- |
| PUT  | Update Announcements  |
| GET  | Get announcements, Get all announcements, Get Announcement by Slug   |
| DELETE | Delete Announcements  |
| POST  | Creating Announcements  |

## Description of Underlying Database/Entity-Level Representation Decisions:

In our entity/database level, we added a new announcement entity. The announcement entity defines the structure of data of each announcement. This entity is very similar to our model as both need to hold the same information needed for an announcement to be an announcement. As users post announcements each filed will be filled in with data to distinguish one announcement from another.  

## Technical and UX Design Choices:

When we first began creating the user interface, we wanted our interface to mirror Canvas’s interface. We wanted the announcements to be seen from top to bottom and then users can pick which announcement they want to see. However, we decided that having the user be able to choose what date they want to see announcements from would overall be much more organized and easier to use. Rather than seeing all announcements at once, users would only see the few announcements for a certain day. Also, for this feature, we assimilated with the current format and structure of the website, such as the fonts and colors used throughout. 

## Feature Intro and Brief Tour:

From a technical sense, everyday students can view announcements posted.  Finally, higher faculty members in the CS department can create announcements while also deleting and editing all other announcements.  

As you are getting started with learning more about the announcement feature, you can look through the announcement folder within the frontend and backend. Both folders have the information on how our feature works including the backend services which call the specific API routes needed to initiate HTTP requests to the server. Additionally, there is a model folder in which the announcement model is held, and more models can be created if needed. Front end wise there are components that contain widgets for creating an announcement and being able to see past announcements. This can be found within the announcement folder within the front-end folder. Finally, we have a 100% test coverage for all the backend services guaranteeing our feature to work.  

## Image Flow of Group Project Feature:

General Home Page When a User Is Not Logged In
![example](./images/docpics/start%20page%20not%20logged%20in.png)

General Home Page When a User Is Logged In
![example](./images/docpics/logged%20in%20general%20start.png)

General Home Page When Admin Is Logged In
![example](./images/docpics/rhonda%20start%20page.png)

Form to Create An Announcement 
![example](./images/docpics/rhonda%20edit.png)

Announcement Page When An Announcement Is Clicked 
![example](./images/docpics/rhonda%20details%20page.png)
