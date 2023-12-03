// init-mongo.js
db = db.getSiblingDB("aidb");

db.createUser({
  user: "dev",
  pwd: "admindev",
  roles: [{ role: "readWrite", db: "aidb" }],
});

// Check if the user has been created
db.getUsers();

// Create collections
db.createCollection("logs");
db.createCollection("chats");

// Create indexes
db.chats.createIndex({ chat_from: 1 });
db.logs.createIndex({ id: 1 });
