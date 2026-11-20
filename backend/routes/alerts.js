const express = require("express");
const router = express.Router();
const Alert = require("../models/Alert");

const mockAlerts = [
  { userId: "USR003", riskScore: 78, reasons: ["Off-hours login", "87 files downloaded", "USB connected"], status: "active", isDuress: false, timestamp: new Date() },
  { userId: "USR005", riskScore: 55, reasons: ["Off-hours login", "31 files downloaded"], status: "active", isDuress: false, timestamp: new Date(Date.now() - 300000) },
  { userId: "USR002", riskScore: 45, reasons: ["22 files downloaded", "Off-hours login"], status: "active", isDuress: false, timestamp: new Date(Date.now() - 720000) },
];

router.get("/", async (req, res) => {
  try {
    const alerts = await Alert.find().sort({ timestamp: -1 }).limit(20);
    if (alerts.length === 0) return res.json(mockAlerts);
    res.json(alerts);
  } catch {
    res.json(mockAlerts);
  }
});

// Duress trigger
router.post("/duress/:userId", async (req, res) => {
  const io = req.app.get("io");
  const alert = { userId: req.params.userId, type: "DURESS", message: "🚨 DURESS SITUATION DETECTED", timestamp: new Date() };
  try {
    await Alert.create({ userId: req.params.userId, riskScore: 100, reasons: ["DURESS TRIGGER ACTIVATED"], isDuress: true });
  } catch {}
  io.emit("duress-alert", alert);
  res.json({ success: true, message: "Silent alert sent to security team" });
});

module.exports = router;
