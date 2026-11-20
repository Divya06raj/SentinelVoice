function calculateRiskScore(activity) {
  let score = 0;
  const reasons = [];

  const hour = new Date(activity.timestamp || Date.now()).getHours();
  if (hour >= 22 || hour <= 6) {
    score += 25;
    reasons.push("Off-hours login detected");
  }

  const files = activity.filesDownloaded || 0;
  if (files > 50) { score += 30; reasons.push(`${files} files downloaded (critical)`); }
  else if (files > 20) { score += 15; reasons.push(`${files} files downloaded (high)`); }
  else if (files > 10) { score += 8; reasons.push(`${files} files downloaded`); }

  if (activity.usbConnected) {
    score += 20;
    reasons.push("USB device connected");
  }

  if (activity.externalEmail) {
    score += 15;
    reasons.push("External email sent");
  }

  if (activity.sensitiveFileAccess) {
    score += 10;
    reasons.push("Sensitive file accessed");
  }

  const riskScore = Math.min(score, 100);
  const riskLevel = riskScore >= 60 ? "high" : riskScore >= 30 ? "medium" : "low";

  return { riskScore, riskLevel, reasons };
}

module.exports = { calculateRiskScore };
