const express = require('express');
const {
  createUser, addEvent, getUserEventsDay,
  getUserEventsMonth
} = require('../controller/userController');

const router = express.Router();

router.post('/create-user', createUser)

router.patch('/add-event', addEvent)

router.get('/:username/day/:dateString', getUserEventsDay)

router.get('/:username/month/:dateString', getUserEventsMonth)


module.exports = router;