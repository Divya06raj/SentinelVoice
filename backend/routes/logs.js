const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee");

// Mock data fallback
const mockEmployees = [
  { userId: "USR001", riskScore: 12, riskLevel: "low", filesDownloaded: 5, usbConnected: false, offHoursLogin: false },
  { userId: "USR002", riskScore: 45, riskLevel: "medium", filesDownloaded: 22, usbConnected: false, offHoursLogin: true },
  { userId: "USR003", riskScore: 78, riskLevel: "high", filesDownloaded: 87, usbConnected: true, offHoursLogin: true },
  { userId: "USR004", riskScore: 20, riskLevel: "low", filesDownloaded: 8, usbConnected: false, offHoursLogin: false },
  { userId: "USR005", riskScore: 55, riskLevel: "medium", filesDownloaded: 31, usbConnected: false, offHoursLogin: true },
];

router.get("/", async (req, res) => {
  try {
    const employees = await Employee.find().sort({ riskScore: -1 });
    if (employees.length === 0) return res.json(mockEmployees);
    res.json(employees);
  } catch {
    res.json(mockEmployees);
  }
});

router.get("/:userId", async (req, res) => {
  try {
    const emp = await Employee.findOne({ userId: req.params.userId });
    if (!emp) {
      const mock = mockEmployees.find(e => e.userId === req.params.userId);
      return mock ? res.json(mock) : res.status(404).json({ error: "Not found" });
    }
    res.json(emp);
  } catch {
    res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
