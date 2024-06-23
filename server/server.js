const express = require('express');
const cors = require('cors');

const userRoutes = require('./routes/userRoutes');
const eventRoutes = require('./routes/eventRoutes');

require('dotenv').config();
const PORT = process.env.PORT;
const URL = process.env.URL;

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors({ origin: true, credentials: true }));

app.use('/api/user', userRoutes);
app.use('/api/event', eventRoutes);

const startServer = async () => {
  try {
    app.listen(PORT, () => {
      console.log(`Server running on port http://${URL}:${PORT}`);
    });
  } catch (error) {
    console.log(error);
  }
};

startServer();
