-- Create the database
CREATE DATABASE FoodOutlet;
GO

-- Switch to the newly created database
USE FoodOutlet;
GO

-- Create the Orders table
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,    -- Unique identifier for each order
    CustomerID INT NOT NULL,                 -- ID of the customer placing the order
    RestaurantID INT NOT NULL,               -- ID of the restaurant fulfilling the order
    OrderAmount DECIMAL(10, 2) NOT NULL,     -- Total amount for the order
    OrderDate DATETIME DEFAULT GETDATE()     -- Date and time the order was placed
);
GO

-- Insert sample data into the Orders table
INSERT INTO Orders (CustomerID, RestaurantID, OrderAmount, OrderDate) VALUES 
(1, 101, 50.00, '2024-11-01 10:00:00'),
(2, 102, 120.50, '2024-11-02 11:30:00'),
(3, 101, 75.25, '2024-11-03 15:45:00'),
(4, 103, 200.00, '2024-11-04 18:00:00'),
(5, 102, 35.50, '2024-11-05 13:20:00'),
(6, 101, 60.75, '2024-11-06 14:10:00'),
(7, 103, 150.00, '2024-11-07 19:25:00'),
(8, 102, 80.00, '2024-11-08 12:35:00');
GO

-- Verify that the data has been inserted
SELECT * FROM Orders;
GO