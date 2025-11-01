# 🗃️ MySQL Database Seeder (ALX_prodev)

This project sets up and seeds a MySQL database named **`ALX_prodev`** with sample user data from a CSV file (`user_data.csv`).

The script:
- Connects to a MySQL server
- Creates the database `ALX_prodev` if it doesn’t exist
- Creates a `users` table if it doesn’t exist
- Reads data from `user_data.csv`
- Inserts user records (with unique UUIDs) into the table

---

## 🧠 Features

✅ Connects to MySQL using credentials from a `.env` file  
✅ Automatically creates the database and table  
✅ Generates UUIDs for each user  
✅ Loads data from CSV and inserts it into MySQL  
✅ Modular design with reusable functions  

---

## 📂 Project Structure

```
project/
│
├── seed.py          # Main script to set up and seed the database
├── user_data.csv    # CSV file containing sample user data
├── .env             # Environment variables for database credentials
└── README.md        # Documentation file
```

---

## ⚙️ Requirements

- Python 3.8+
- MySQL Server 8.0+
- Required Python packages:
  - `mysql-connector-python`
  - `python-dotenv`

---

## 📦 Installation

1. **Clone the repository** (or copy the project files):
   ```bash
   git clone https://github.com/yourusername/mysql-seeder.git
   cd mysql-seeder
   ```

2. **Install dependencies:**
   ```bash
   pip install mysql-connector-python python-dotenv
   ```

3. **Create a `.env` file** in the project root directory:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   ```

4. **Create the CSV file** (`user_data.csv`) with sample data:
   ```csv
   name,email,age
   John Doe,john@example.com,28
   Jane Smith,jane@example.com,32
   Michael Brown,mike@example.com,25
   ```

---

## 🚀 Usage

1. **Run the script:**
   ```bash
   python seed.py
   ```

2. The script will:
   - Connect to your MySQL server  
   - Create the `ALX_prodev` database  
   - Create the `users` table  
   - Insert data from `user_data.csv`  

3. **Verify the inserted data:**
   ```sql
   USE ALX_prodev;
   SELECT * FROM users;
   ```

---

## 🧩 Function Overview

| Function | Description |
|-----------|-------------|
| `connect_db()` | Connects to the MySQL server (no specific DB). |
| `create_database(connection)` | Creates `ALX_prodev` if it doesn’t exist. |
| `connect_to_prodev()` | Connects to the `ALX_prodev` database. |
| `create_table(connection)` | Creates the `users` table if missing. |
| `insert_data(connection, data)` | Inserts a user record into the table. |
| `read_csv(file_path)` | Reads CSV data and returns a list of user records. |

---

## 🧱 Database Schema

**Database:** `ALX_prodev`  
**Table:** `users`

| Field | Type | Attributes |
|--------|------|-------------|
| `user_id` | CHAR(36) | Primary Key (UUID) |
| `name` | VARCHAR(255) | NOT NULL |
| `email` | VARCHAR(255) | NOT NULL |
| `age` | DECIMAL(3,0) | NOT NULL |

---

## 💡 Troubleshooting

### ❌ Error: `Authentication plugin 'caching_sha2_password' is not supported`
Fix by upgrading the connector or changing the MySQL user authentication plugin:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

or install the latest connector:
```bash
pip install --upgrade mysql-connector-python
```

---

## 📜 License

This project is open-source and free to use for educational or professional purposes.

---

## 👨‍💻 Author

**Abednego Komla Tenge**  
Cloud Engineer | Backend Engineer | Python Developer
