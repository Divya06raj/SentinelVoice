const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee");
const Alert = require("../models/Alert");
const { calculateRiskScore } = require("../engine/anomalyDetector");

// Simulate insider attack for demo
router.post("/simulate-attack", async (req, res) => {
  const io = req.app.get("io");
  const userId = req.body.userId || "USR023";

  const activity = {
    userId,
    timestamp: new Date("2024-01-16T02:30:00"),
    filesDownloaded: 500,
    usbConnected: true,
    offHoursLogin: true,
    externalEmail: true,
    sensitiveFileAccess: true
  };

  const { riskScore, riskLevel, reasons } = calculateRiskScore(activity);

  // Simulate score rising over time
  const steps = [15, 30, 50, 70, 85, riskScore];
  let delay = 0;

  steps.forEach((score, i) => {
    setTimeout(() => {
      io.emit("risk-update", { userId, riskScore: score, riskLevel: score >= 60 ? "high" : score >= 30 ? "medium" : "low" });
      if (score >= 60 && i === steps.length - 1) {
        io.emit("new-alert", { userId, riskScore: score, reasons, riskLevel: "high", timestamp: new Date() });
      }
    }, delay);
    delay += 800;
  });

  try {
    await Employee.findOneAndUpdate({ userId }, { riskScore, riskLevel, filesDownloaded: 500, usbConnected: true, offHoursLogin: true, $push: { riskHistory: { score: riskScore } } }, { upsert: true });
    await Alert.create({ userId, riskScore, reasons });
  } catch {}

  res.json({ success: true, userId, riskScore, riskLevel, reasons });
});

// Verify PIN - normal vs duress
router.post("/verify-pin", (req, res) => {
  const io = req.app.get("io");
  const { userId, pin } = req.body;
  const NORMAL_PIN = "1234";
  const DURESS_PIN = "9999";

  if (pin === DURESS_PIN) {
    io.emit("duress-alert", { userId, message: "🚨 DURESS PIN ENTERED - EMPLOYEE NEEDS HELP", timestamp: new Date() });
    return res.json({ status: "granted", message: "Access Granted", isDuress: true });
  }
  if (pin === NORMAL_PIN) {
    // Risk score kam karo - verified normal
    io.emit("risk-update", { userId, riskScore: 15, riskLevel: "low", verified: true });
    return res.json({ status: "granted", message: "Access Granted", isDuress: false, riskReduced: true });
  }
  return res.json({ status: "denied", message: "Access Denied - Action Blocked" });
});

module.exports = router;
