-- 1. ŽÁNRY
CREATE TABLE Genres (
    GenreID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50) NOT NULL UNIQUE
);

-- 2. UŽIVATELÉ
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Email NVARCHAR(100) NOT NULL,
    WalletBalance FLOAT NOT NULL DEFAULT 0.0 CHECK (WalletBalance >= 0),
    IsAdmin BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME DEFAULT GETDATE()
);

-- 3. HRY
CREATE TABLE Games (
    GameID INT PRIMARY KEY IDENTITY(1,1),
    GenreID INT, -- Vazba na žánr
    Title NVARCHAR(100) NOT NULL,
    Price FLOAT NOT NULL CHECK (Price >= 0),
    Description NVARCHAR(MAX),
    Status NVARCHAR(20) CHECK (Status IN ('Available', 'EarlyAccess', 'Deprecated')) DEFAULT 'Available',
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID) ON DELETE SET NULL
);

-- 4. RECENZE
CREATE TABLE Reviews (
    ReviewID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    Rating INT NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
    Comment NVARCHAR(500),
    ReviewDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

-- 5. OBJEDNÁVKY
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    OrderDate DATETIME DEFAULT GETDATE(),
    TotalAmount FLOAT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- 6. POLOŽKY OBJEDNÁVKY
CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT NOT NULL,
    GameID INT NOT NULL,
    PriceAtPurchase FLOAT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);
GO

-- POHLED (Report)
CREATE VIEW v_UserActivity AS
SELECT u.Username, COUNT(o.OrderID) as OrdersCount, ISNULL(SUM(o.TotalAmount), 0) as TotalSpent
FROM Users u LEFT JOIN Orders o ON u.UserID = o.UserID
GROUP BY u.Username;
GO

-- DATA
INSERT INTO Genres (Name) VALUES ('RPG'), ('FPS'), ('Strategy');
INSERT INTO Users (Username, Email, WalletBalance, IsAdmin) VALUES ('Admin', 'ad@min.com', 9999, 1), ('Player1', 'p1@test.com', 500, 0);
INSERT INTO Games (GenreID, Title, Price, Description, Status) VALUES (1, 'Witcher 3', 29.99, 'Top RPG', 'Available'), (2, 'Doom', 19.99, 'Shoot em up', 'Available');
INSERT INTO Reviews (UserID, GameID, Rating, Comment) VALUES (2, 1, 5, 'Super hra');
INSERT INTO Orders (UserID, TotalAmount) VALUES (2, 29.99);