
# Food Outlet API Documentation

## **Overview**
This API provides an endpoint to fetch the total sales for a restaurant based on its ID from a SQL Server database.

---

## **Endpoints**

### **1. Get Total Sales for a Restaurant**

```http
GET /restaurants/<restaurant_id>/sales
```

#### **Request Parameters**
- **Path Parameter:**
  - `restaurant_id` (integer): The ID of the restaurant whose sales data you want to retrieve.

#### **Example Request**
```bash
curl -X GET http://localhost:8080/restaurants/1/sales
```

#### **Responses**

1. **Success (200):**
   ```json
   {
       "restaurantID": 1,
       "totalSales": 1500.50
   }
   ```

2. **Invalid Restaurant ID (400):**
   ```json
   {
       "error": "Invalid restaurant ID"
   }
   ```

3. **Server Error (500):**
   ```json
   {
       "error": "Failed to retrieve sales data"
   }
   ```

---

# **Running Microsoft SQL Server on Docker**

## **Step 1: Creating Docker Network**

```bash
docker network create my_network
```
## **Step 2: Running MS SQL Server on Docker**

```bash
docker run -d \
--name sqlserver \
--network my_network \
-e "ACCEPT_EULA=Y" \
-e 'SA_PASSWORD=Datadog2024!' \
-p 1433:1433 \
-v $(pwd)/init.sql:/usr/src/app/init.sql \
mcr.microsoft.com/mssql/server:2022-latest
```

## **Step 3: Creating Database and Tables on MS SQL Server**

```bash
docker exec -t sqlserver /bin/bash -c "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'Datadog2024!' -i /usr/src/app/init.sql -C" 
```

# **Setup and Run the API Using Docker**

## **Step 1: Prerequisites**
Ensure the following are installed on your machine:
- **Docker** for containerization.
- A running Microsoft SQL Server instance with the required database (`FoodOutlet`).

---

## **Step 2: Environment Variables**
Create a `.env` file in the project directory with the following content:

```dotenv
DATABASE_HOST=localhost
DATABASE_PORT=1433
DATABASE_NAME=FoodOutlet
DATABASE_USER=sa
DATABASE_PASSWORD=Datadog2024!
```

---

## **Step 3: Build and Run Docker**

### **Build the Docker Image**
Run the following command in your terminal to build the Docker image:
```bash
docker build -t food-outlet-api .
```

### **Run the Docker Container**
Run the container using the `docker run` command:

```bash
docker run -d --name food-outlet-api --network my_network -p 8080:5000 --env-file .env food-outlet-api
```

```bash
docker run -d --name food-outlet-api --network my_network -p 8080:5000 \
-e DATABASE_HOST=sqlserver \
-e DATABASE_PORT=1433 \
-e DATABASE_NAME=FoodOutlet \
-e DATABASE_USER=sa \
-e DATABASE_PASSWORD='Datadog2024!' \
food-outlet-api
```

This will start the application on port `8080`.

---

# **Test the API Using Docker**

## **Test the API Using `curl`**

1. **Fetch Total Sales for a Restaurant with ID 1:**
   ```bash
   curl -X GET http://localhost:8080/restaurants/1/sales
   ```

   **Example Response:**
   ```json
   {
       "restaurantID": 1,
       "totalSales": 1500.50
   }
   ```

2. **Test with an Invalid Restaurant ID:**
   ```bash
   curl -X GET http://localhost:8080/restaurants/-1/sales
   ```

   **Example Response:**
   ```json
   {
       "error": "Invalid restaurant ID"
   }
   ```

3. **Test with a Non-Existent Restaurant ID:**
   ```bash
   curl -X GET http://localhost:8080/restaurants/9999/sales
   ```

   **Example Response:**
   ```json
   {
       "restaurantID": 9999,
       "totalSales": 0
   }
   ```

---

## **View Logs**

To check the application logs from the running container, use the following command:
```bash
docker logs food-outlet-api
```

---

# **Stop and Clean Up Docker**

1. **Stop the Running Container:**
   ```bash
   docker stop food-outlet-api
   ```

2. **Remove the Stopped Container:**
   ```bash
   docker rm food-outlet-api
   ```

3. **Remove the Docker Image:**
   ```bash
   docker rmi food-outlet-api
   ```

---

# **Notes**
- Make sure your SQL Server instance is running and accessible from the container.
- If using a remote database, update the `DATABASE_HOST` in the `.env` file accordingly.
