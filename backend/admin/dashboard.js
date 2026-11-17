// ===== CONFIG =====
// Yahan apne backend ka base URL daalo. Local development mein
// FastAPI default se http://127.0.0.1:8000 par chalta hai
// (uvicorn backend.main:app --reload)
const API_BASE_URL = "http://127.0.0.1:8000";

// Page load hote hi sab data fetch karo
document.addEventListener("DOMContentLoaded", () => {
    loadStats();
    loadFileTypes();
    loadRecentAnalyses();
    loadRecentUsers();
});

// ---- 1. Top stat cards ----
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/dashboard/stats`);
        if (!response.ok) throw new Error("Stats request failed");

        const data = await response.json();

        document.getElementById("totalUsers").textContent = data.total_users;
        document.getElementById("totalAnalyses").textContent = data.total_analyses;
        document.getElementById("realCount").textContent = data.real_count;
        document.getElementById("fakeCount").textContent = data.fake_count;

        // "Database data pending" ki jagah ab kuch nahi dikhana, ya
        // chaho to last-updated time dikha sakti ho
        document.getElementById("totalUsersNote").textContent = "Live from database";
        document.getElementById("totalAnalysesNote").textContent = "Live from database";
        document.getElementById("realCountNote").textContent = "Live from database";
        document.getElementById("fakeCountNote").textContent = "Live from database";

    } catch (error) {
        console.error("Stats load failed:", error);
        // Agar backend down ho to purane placeholders hi rehne dete hain
    }
}

// ---- 2. File type donut + legend ----
async function loadFileTypes() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/dashboard/file-types`);
        if (!response.ok) throw new Error("File-types request failed");

        const data = await response.json();
        const total = data.image + data.video + data.audio;

        document.getElementById("donutTotal").textContent = total;
        document.getElementById("imageCount").textContent = data.image;
        document.getElementById("videoCount").textContent = data.video;
        document.getElementById("audioCount").textContent = data.audio;

    } catch (error) {
        console.error("File-type load failed:", error);
    }
}

// ---- 3. Recent analyses table ----
async function loadRecentAnalyses() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/dashboard/recent-analyses`);
        if (!response.ok) throw new Error("Recent analyses request failed");

        const analyses = await response.json();
        const tbody = document.getElementById("recentAnalysesBody");

        if (!analyses.length) {
            tbody.innerHTML = `<tr><td colspan="5" class="empty-row">No analysis data available yet.</td></tr>`;
            return;
        }

        tbody.innerHTML = analyses.map(item => `
            <tr>
                <td>${item.file_name}</td>
                <td>${item.file_type ?? "-"}</td>
                <td>${item.result ?? "-"}</td>
                <td>${item.confidence != null ? (item.confidence * 100).toFixed(1) + "%" : "-"}</td>
                <td>${item.created_at ? new Date(item.created_at).toLocaleString() : "-"}</td>
            </tr>
        `).join("");

    } catch (error) {
        console.error("Recent analyses load failed:", error);
    }
}

// ---- 4. Recent users table ----
async function loadRecentUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/dashboard/recent-users`);
        if (!response.ok) throw new Error("Recent users request failed");

        const users = await response.json();
        const tbody = document.getElementById("recentUsersBody");

        if (!users.length) {
            tbody.innerHTML = `<tr><td colspan="5" class="empty-row">No user data available yet.</td></tr>`;
            return;
        }

        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.role}</td>
                <td>${user.status}</td>
                <td>${user.created_at ? new Date(user.created_at).toLocaleString() : "-"}</td>
            </tr>
        `).join("");

    } catch (error) {
        console.error("Recent users load failed:", error);
    }
}