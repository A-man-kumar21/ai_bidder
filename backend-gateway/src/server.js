import "dotenv/config";
import cors from "cors";
import express from "express";
import { getAuditCollection } from "./db.js";

const app = express();
app.use(cors());
app.use(express.json());

app.get("/health", (_request, response) => {
  response.json({ service: "backend-gateway", status: "ready" });
});

const ENGINE_URL = process.env.AI_ENGINE_URL || "http://127.0.0.1:8000";
const VALID_DECISIONS = new Set(["approve", "reject", "request_more_info"]);

/**
 * Proxies the AI engine unchanged. The assessment is persisted separately; the
 * gateway never recalculates or changes the engine response.
 */
app.post("/api/compliance/verify", async (request, response, next) => {
  try {
    const engineResponse = await fetch(`${ENGINE_URL}/verify-compliance`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(request.body),
    });
    const assessment = await engineResponse.json();

    if (!engineResponse.ok) {
      return response.status(engineResponse.status).json(assessment);
    }

    const audit = await getAuditCollection();
    await audit.insertOne({
      bidder_id: assessment.bidder_id,
      timestamp: assessment.audit_log_entry.timestamp,
      compliance_score: assessment.compliance_score,
      risk_level: assessment.risk_level,
      pending_manual_review: assessment.pending_manual_review,
      officer_decision: null,
      officer_id: null,
    });

    return response.json(assessment);
  } catch (error) {
    return next(error);
  }
});

/** Records a human decision without modifying AI assessment fields. */
app.post("/api/audit/decision", async (request, response, next) => {
  try {
    const { bidder_id: bidderId, decision, officer_id: officerId } = request.body;
    if (!bidderId || !officerId || !VALID_DECISIONS.has(decision)) {
      return response.status(400).json({
        error: "bidder_id, officer_id, and decision (approve/reject/request_more_info) are required.",
      });
    }

    const audit = await getAuditCollection();
    const result = await audit.findOneAndUpdate(
      { bidder_id: bidderId, officer_decision: null },
      { $set: { officer_decision: decision, officer_id: officerId } },
      { sort: { timestamp: -1 }, returnDocument: "after" },
    );

    if (!result) {
      return response.status(404).json({
        error: "No undecided scoring audit entry exists for this bidder.",
      });
    }
    return response.json(result);
  } catch (error) {
    return next(error);
  }
});

/** Returns every scoring run and its independently recorded human decision. */
app.get("/api/audit/:bidderId", async (request, response, next) => {
  try {
    const audit = await getAuditCollection();
    const entries = await audit
      .find({ bidder_id: request.params.bidderId })
      .sort({ timestamp: -1 })
      .toArray();
    return response.json(entries);
  } catch (error) {
    return next(error);
  }
});

app.use((error, _request, response, _next) => {
  console.error(error);
  response.status(502).json({ error: "Gateway could not complete the requested operation." });
});

const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`Gateway listening on ${port}`));
