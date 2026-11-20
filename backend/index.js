const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const http = require("http");
const { Server } = require("socket.io");
const axios = require("axios");
require("dotenv").config();

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(cors());
app.use(express.json());


mongoose.connect(process.env.MONGO_URI || "mongodb://localhost:27017/sentinelvoice")
  .then(() => console.log("MongoDB connected"))
  .catch(() => console.log("MongoDB not connected - using mock data"));


app.set("io", io);


app.use("/api/logs", require("./routes/logs"));
app.use("/api/alerts", require("./routes/alerts"));
app.use("/api/risk", require("./routes/risk"));
app.use("/api/demo", require("./routes/demo"));

io.on("connection", (socket) => {
  console.log("Dashboard connected:", socket.id);

  socket.on("employee-login", (data) => {
    console.log(`Employee logged in: ${data.userId}`);
    io.emit("employee-login", { ...data, timestamp: new Date() });
  });
});

server.listen(5000, () => console.log("SentinelVoice backend running on port 5000"));
