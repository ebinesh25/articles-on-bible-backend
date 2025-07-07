// MongoDB initialization script
db = db.getSiblingDB('fastapi_db');

// Create a user for the application
db.createUser({
  user: 'fastapi_user',
  pwd: 'fastapi_password',
  roles: [
    {
      role: 'readWrite',
      db: 'fastapi_db'
    }
  ]
});

// Create initial collection and insert sample data
db.items.insertMany([
  {
    name: "Sample Item 1",
    description: "This is a sample item",
    price: 29.99,
    quantity: 10
  },
  {
    name: "Sample Item 2", 
    description: "Another sample item",
    price: 49.99,
    quantity: 5
  }
]);

print("Database initialized with sample data");