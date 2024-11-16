const { Pool } = require('pg');
require('dotenv').config();

const connectionString = process.env.DB_CONNECTION_STRING;

const pool = new Pool({
  connectionString: connectionString,
  ssl: {
    rejectUnauthorized: false,  // Set to true if you have the SSL certificate for your RDS instance
  },
});

pool.connect()
  .then(client => {
    console.log('Connected to the database successfully');
    client.release();  // Release the client when done
  })
  .catch(err => {
    console.error('Error during database connection:', err.message);  // Print error message
    console.error(err.stack);  // Print full error stack trace
  });

module.exports = pool;
