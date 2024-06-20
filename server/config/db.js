const mongoose = require('mongoose')
require('dotenv').config()

const db = process.env.MONGO_URI

const connectDB = async () => {
    try {
        mongoose.set('strictQuery', true);
        await mongoose.connect(db, {
            useNewUrlParser: true,
        });

        console.log('MongoDB is connected')
    } catch (err) {
        console.error(err.message);
        process.exit(1);
    }
};

module.exports = connectDB;