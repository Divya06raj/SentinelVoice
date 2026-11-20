const mongoose = require("mongoose");

const employeeSchema = new mongoose.Schema({
  userId: { type: String, required: true, unique: true },
  riskScore: { type: Number, default: 0 },
  riskLevel: { type: String, default: "low" },
  lastLogin: Date,
  filesDownloaded: { type: Number, default: 0 },
  usbConnected: { type: Boolean, default: false },
  offHoursLogin: { type: Boolean, default: false },
  externalEmail: { type: Boolean, default: false },
  riskHistory: [{ score: Number, timestamp: { type: Date, default: Date.now } }]
}, { timestamps: true });

module.exports = mongoose.model("Employee", employeeSchema);
