const express = require('express');
const { addEvent, getUserEventsDay, getUserEventsMonth, deleteEvent } = require('../controller/eventController');

const router = express.Router();

router.patch('/add_event', addEvent);

router.get('/:user_id/day/:event_date', getUserEventsDay);

router.get('/:user_id/month/:event_month', getUserEventsMonth);

router.post('/delete_event', deleteEvent);

module.exports = router;
