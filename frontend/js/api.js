const API_BASE_URL = "http://localhost:8000/api";

function getHeaders() {
    const token = localStorage.getItem("access_token");
    const headers = {
        "Content-Type": "application/json"
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

export async function loginWithFirebaseToken(firebaseToken, email, name, uid) {
    const response = await fetch(`${API_BASE_URL}/users/firebase-login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ firebase_token: firebaseToken, email, name, uid })
    });
    if (!response.ok) throw new Error("Backend login failed");
    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
    return data;
}

export async function fetchUser() {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, { headers: getHeaders() });
        if (!response.ok) {
            if (response.status === 401) localStorage.removeItem("access_token");
            return null;
        }
        return await response.json();
    } catch(err) {
        console.error("Error fetching user:", err);
        return null;
    }
}

export async function fetchWorkers(serviceType, location) {
    let url = `${API_BASE_URL}/workers/`;
    const params = new URLSearchParams();
    if (serviceType) params.append("service_type", serviceType);
    if (location) params.append("location", location);
    if (params.toString()) url += `?${params.toString()}`;
    
    const response = await fetch(url, { headers: getHeaders() });
    if (!response.ok) return [];
    return await response.json();
}

export async function saveWorkerProfile(profileData) {
    const response = await fetch(`${API_BASE_URL}/workers/profile`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(profileData)
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Failed to save profile");
    }
    return await response.json();
}

export async function fetchAdminWorkers() {
    const response = await fetch(`${API_BASE_URL}/admin/workers`, { headers: getHeaders() });
    if (!response.ok) return [];
    return await response.json();
}

export async function approveWorker(id) {
    const response = await fetch(`${API_BASE_URL}/admin/workers/${id}/approve`, {
        method: "PUT",
        headers: getHeaders()
    });
    return response.ok;
}

export async function removeWorker(id) {
    const response = await fetch(`${API_BASE_URL}/admin/workers/${id}`, {
        method: "DELETE",
        headers: getHeaders()
    });
    return response.ok;
}

export async function fetchChatHistory(otherUserId) {
    const response = await fetch(`${API_BASE_URL}/messages/${otherUserId}`, { headers: getHeaders() });
    if (!response.ok) return [];
    return await response.json();
}

export async function sendMessage(receiverId, content) {
    const response = await fetch(`${API_BASE_URL}/messages/`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({ receiver_id: parseInt(receiverId), content: content })
    });
    if (!response.ok) throw new Error("Failed to send message");
    return await response.json();
}

export async function fetchWorkerById(id) {
    const response = await fetch(`${API_BASE_URL}/workers/${id}`, { headers: getHeaders() });
    if (!response.ok) return null;
    return await response.json();
}
