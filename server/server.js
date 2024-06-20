const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');

require('dotenv').config();
const PORT = process.env.PORT;
const URL = process.env.URL;

const app = express();

const userRoutes = require('./routes/userRoutes')

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors({ origin: true, credentials: true }));


app.use('/api/user', userRoutes)
const startServer = async () => {
  try {
    connectDB();
    app.listen(PORT, () => {
      console.log(`Server running on port http://${URL}:${PORT}`);
    });
  } catch (error) {
    console.log(error);
  }
};

startServer();