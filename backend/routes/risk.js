const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee");
const Alert = require("../models/Alert");
const { calculateRiskScore } = require("../engine/anomalyDetector");

router.post("/analyze", async (req, res) => {
  const io = req.app.get("io");
  const activity = req.body;
  const { riskScore, riskLevel, reasons } = calculateRiskScore(activity);

  try {
    await Employee.findOneAndUpdate(
      { userId: activity.userId },
      { riskScore, riskLevel, filesDownloaded: activity.filesDownloaded, usbConnected: activity.usbConnected, offHoursLogin: activity.offHoursLogin, $push: { riskHistory: { score: riskScore } } },
      { upsert: true, new: true }
    );
    if (riskScore >= 60) {
      const alert = await Alert.create({ userId: activity.userId, riskScore, reasons });
      io.emit("new-alert", { ...alert.toObject(), riskLevel });
    }
  } catch {}

  res.json({ userId: activity.userId, riskScore, riskLevel, reasons });
});

router.get("/:userId", async (req, res) => {
  try {
    const emp = await Employee.findOne({ userId: req.params.userId });
    if (!emp) return res.status(404).json({ error: "User not found" });
    res.json({ userId: emp.userId, riskScore: emp.riskScore, riskLevel: emp.riskLevel, riskHistory: emp.riskHistory });
  } catch {
    res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
