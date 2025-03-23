# GameOn - Find and Organize Sports Games 🎮

## Table of Contents
- [Overview](#overview)
- [Application Flow](#application-flow)
  - [1. Welcome Page](#1-welcome-page)
  - [2. Authentication](#2-authentication)
  - [3. Game Creation](#3-game-creation)
  - [4. Game Discovery](#4-game-discovery)
  - [5. Game Details](#5-game-details)
  - [6. Profile Management](#6-profile-management)
  - [7. Notifications](#7-notifications)
- [Technical Stack](#technical-stack)
- [Database Schema](#database-schema)
  - [Users Table](#users-table)
  - [Games Table](#games-table)
  - [GameParticipants Table](#gameparticipants-table)
  - [Notifications Table](#notifications-table)
  - [UserSettings Table](#usersettings-table)
- [Project Structure](#project-structure)

## Overview

GameOn is a platform that connects sports enthusiasts, making it easy to create, discover, and join sports games in your area. Whether you're organizing a friendly match or looking to join one, GameOn streamlines the process.

## Application Flow

### 1. Welcome Page
- Initial screen featuring app logo and slogan
- Main actions:
  - Login button
  - Create Account button

### 2. Authentication
- **Login Options:**
  - Email and password
  - "Forgot Password?" functionality
- **Account Creation Fields:**
  - Username
  - Email
  - Date of birth
  - Zone/Country
  - Password

### 3. Game Creation
Users can create games with the following details:
- 📍 **Location**
  - Sports field
  - Indoor facility
  - City
- 📅 **Date and Time**
- 👥 **Available Spots**
- 🏷️ **Game Type**
  - Public (visible and open to all users)
  - Private (invitation-only)
- 🔗 **Invitation Link** (for private games)
- 💬 **Additional Notes** (e.g., "bring white t-shirt")

### 4. Game Discovery
Main search page featuring:
- Available games in user's area
- Search functionality with filters:
  - Location
  - Date
  - Available spots
  - Game type (public/private)

### 5. Game Details
Comprehensive game information page with:
- ✅ Join button (public games)
- 🔒 Request access button (private games)
- 📲 Share functionality
- 📢 Game chat for participant communication
- 📌 Navigation integration (Google/Apple Maps)

### 6. Profile Management
User profile section including:
- Personal information
- Notification settings
- Game management:
  - Created games
  - Joined games
  - Saved favorites
- Game history (past and upcoming)
- Game editing and cancellation options

### 7. Notifications
Automated system providing alerts for:
- Upcoming game reminders
- Nearly full games
- Organizer updates
- Private game access requests

## Technical Stack

### Frontend
- HTML
- tailwind css

### Backend
- 

### Database
- Microsoft SQL Server (User and game data storage)

## Database Schema

### Users Table
```sql
CREATE TABLE Users (
    UserId INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    DateOfBirth DATE NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    LastLogin DATETIME,
    ProfilePicture NVARCHAR(255),
    IsActive BIT DEFAULT 1
)
```

### Games Table
```sql
CREATE TABLE Games (
    GameId INT PRIMARY KEY IDENTITY(1,1),
    CreatorId INT FOREIGN KEY REFERENCES Users(UserId),
    Title NVARCHAR(100) NOT NULL,
    Location NVARCHAR(255) NOT NULL,
    GameDateTime DATETIME NOT NULL,
    AvailableSpots INT NOT NULL,
    GameType BIT NOT NULL, -- 0: Public, 1: Private
    InviteLink NVARCHAR(100),
    Description NVARCHAR(500),
    CreatedAt DATETIME DEFAULT GETDATE(),
    IsActive BIT DEFAULT 1
)
```

### GameParticipants Table
```sql
CREATE TABLE GameParticipants (
    GameId INT FOREIGN KEY REFERENCES Games(GameId),
    UserId INT FOREIGN KEY REFERENCES Users(UserId),
    JoinedAt DATETIME DEFAULT GETDATE(),
    Status NVARCHAR(20) DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED
    PRIMARY KEY (GameId, UserId)
)
```

### Notifications Table
```sql
CREATE TABLE Notifications (
    NotificationId INT PRIMARY KEY IDENTITY(1,1),
    UserId INT FOREIGN KEY REFERENCES Users(UserId),
    GameId INT FOREIGN KEY REFERENCES Games(GameId),
    Type NVARCHAR(50) NOT NULL, -- REMINDER, GAME_UPDATE, ACCESS_REQUEST
    Message NVARCHAR(255) NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    IsRead BIT DEFAULT 0
)
```

### UserSettings Table
```sql
CREATE TABLE UserSettings (
    UserId INT PRIMARY KEY FOREIGN KEY REFERENCES Users(UserId),
    NotificationsEnabled BIT DEFAULT 1,
    EmailNotifications BIT DEFAULT 1,
    PushNotifications BIT DEFAULT 1,
    PreferredRadius INT DEFAULT 10, -- in kilometers
    Language NVARCHAR(10) DEFAULT 'en'
)
```

## Project Structure 