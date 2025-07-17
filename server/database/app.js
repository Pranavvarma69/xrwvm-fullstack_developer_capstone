const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');

const Dealership = require('./dealership');
const Review = require('./review');

const app = express();
const port = 3030;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/dealershipsDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Load data from JSON files
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Seed the database
async function seedDB() {
  try {
    await Review.deleteMany({});
    await Dealership.deleteMany({});

    await Review.insertMany(reviews_data.reviews);
    await Dealership.insertMany(dealerships_data.dealerships);
    console.log("Database seeded successfully.");
  } catch (error) {
    console.error("Error seeding database:", error);
  }
}

seedDB();

// Routes
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const reviews = await Review.find();
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Fetch reviews by dealership ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const reviews = await Review.find({ dealership: parseInt(req.params.id) });
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealership.find();
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

// Fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealers = await Dealership.find({ state: req.params.state });
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

// Fetch dealership by ID
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealership.findOne({ id: parseInt(req.params.id) });
    res.json(dealer);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by ID' });
  }
});

// Insert new review
app.post('/insert_review', async (req, res) => {
  try {
    const latest = await Review.find().sort({ id: -1 }).limit(1);
    const new_id = latest.length > 0 ? latest[0].id + 1 : 1;

    const review = new Review({
      id: new_id,
      name: req.body.name,
      dealership: req.body.dealership,
      review: req.body.review,
      purchase: req.body.purchase,
      purchase_date: req.body.purchase_date,
      car_make: req.body.car_make,
      car_model: req.body.car_model,
      car_year: req.body.car_year
    });

    const saved = await review.save();
    res.json(saved);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});