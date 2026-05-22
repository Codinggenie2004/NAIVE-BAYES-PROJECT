// ── DOM Elements ──────────────────────────────────────────────────────────
const messageInput  = document.getElementById("messageInput");
const charCount     = document.getElementById("charCount");
const predictBtn    = document.getElementById("predictBtn");
const resultContainer = document.getElementById("resultContainer");
const resultBadge   = document.getElementById("resultBadge");
const resultIcon    = document.getElementById("resultIcon");
const resultLabel   = document.getElementById("resultLabel");
const hamBar        = document.getElementById("hamBar");
const spamBar       = document.getElementById("spamBar");
const hamPercent    = document.getElementById("hamPercent");
const spamPercent   = document.getElementById("spamPercent");
const confidenceValue = document.getElementById("confidenceValue");

// ── Character counter ─────────────────────────────────────────────────────
messageInput.addEventListener("input", () => {
    charCount.textContent = messageInput.value.length;
});

// ── Classify ──────────────────────────────────────────────────────────────
async function classifyMessage() {
    const message = messageInput.value.trim();
    if (!message) {
        messageInput.focus();
        messageInput.style.borderColor = "var(--accent-red)";
        setTimeout(() => messageInput.style.borderColor = "", 1500);
        return;
    }

    // Loading state
    predictBtn.classList.add("loading");
    predictBtn.disabled = true;

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        showResult(data);
    } catch (err) {
        console.error(err);
        alert("Something went wrong. Is the server running?");
    } finally {
        predictBtn.classList.remove("loading");
        predictBtn.disabled = false;
    }
}

// ── Show Result ───────────────────────────────────────────────────────────
function showResult(data) {
    const isSpam = data.prediction === "spam";

    // Badge
    resultBadge.className = "result-badge " + data.prediction;
    resultIcon.textContent = isSpam ? "🚫" : "✅";
    resultLabel.textContent = isSpam ? "Spam Detected" : "Ham — Safe Message";

    // Confidence bars
    hamBar.style.width  = data.ham_probability + "%";
    spamBar.style.width = data.spam_probability + "%";
    hamPercent.textContent  = data.ham_probability + "%";
    spamPercent.textContent = data.spam_probability + "%";
    confidenceValue.textContent = data.confidence + "%";

    // Show
    resultContainer.classList.add("show");

    // Scroll into view
    resultContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Sample Message Fill ───────────────────────────────────────────────────
function fillSample(btn) {
    // Get text content minus the tag
    const tag = btn.querySelector(".sample-tag");
    let text = btn.textContent.replace(tag.textContent, "").trim();
    messageInput.value = text;
    charCount.textContent = text.length;

    // Scroll up and focus
    document.getElementById("classifierCard").scrollIntoView({ behavior: "smooth" });
    messageInput.focus();

    // Auto-classify after a short delay
    setTimeout(classifyMessage, 400);
}

// ── Load Stats on Page Load ───────────────────────────────────────────────
async function loadStats() {
    try {
        const res = await fetch("/stats");
        const s = await res.json();

        document.getElementById("statAccuracy").textContent  = s.accuracy + "%";
        document.getElementById("statPrecision").textContent = s.precision + "%";
        document.getElementById("statRecall").textContent    = s.recall + "%";
        document.getElementById("statF1").textContent        = s.f1 + "%";

        document.getElementById("infoTotal").textContent = s.total_samples.toLocaleString();
        document.getElementById("infoHam").textContent   = s.ham_count.toLocaleString();
        document.getElementById("infoSpam").textContent  = s.spam_count.toLocaleString();
        document.getElementById("infoVocab").textContent = s.vocab_size.toLocaleString();
        document.getElementById("infoTrain").textContent = s.train_samples.toLocaleString();
        document.getElementById("infoTest").textContent  = s.test_samples.toLocaleString();

        // Confusion matrix [TN, FP], [FN, TP] (sklearn format for binary)
        const cm = s.confusion_matrix;
        document.getElementById("cmTN").textContent = cm[0][0];
        document.getElementById("cmFP").textContent = cm[0][1];
        document.getElementById("cmFN").textContent = cm[1][0];
        document.getElementById("cmTP").textContent = cm[1][1];
    } catch (err) {
        console.error("Failed to load stats:", err);
    }
}

// ── Keyboard shortcut: Enter to classify ──────────────────────────────────
messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        classifyMessage();
    }
});

// ── Init ──────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", loadStats);
