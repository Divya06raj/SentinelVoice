const mongoose = require("mongoose");

const alertSchema = new mongoose.Schema({
  userId: { type: String, required: true },
  riskScore: Number,
  reasons: [String],
  status: { type: String, default: "active" },
  isDuress: { type: Boolean, default: false },
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Alert", alertSchema);
