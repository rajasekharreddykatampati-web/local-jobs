import { auth, googleProvider, signInWithPopup, signOut, onAuthStateChanged } from './firebase-config.js';
import { loginWithFirebaseToken, fetchUser } from './api.js';

export async function handleGoogleSignIn() {
    try {
        const result = await signInWithPopup(auth, googleProvider);
        const user = result.user;
        const token = await user.getIdToken();
        
        // Send to backend
        await loginWithFirebaseToken(token, user.email, user.displayName || 'User', user.uid);
        
        // Redirect to dashboard or home
        window.location.href = 'index.html';
    } catch (error) {
        console.error("Error signing in with Google:", error);
        alert(error.message);
    }
}

export async function handleLogout() {
    try {
        await signOut(auth);
        localStorage.removeItem("access_token");
        window.location.href = 'index.html';
    } catch (error) {
        console.error("Logout error", error);
    }
}

// Check session on load to toggle UI
document.addEventListener("DOMContentLoaded", async () => {
    onAuthStateChanged(auth, async (user) => {
        const navAuth = document.getElementById("nav-auth");
        if (user && localStorage.getItem("access_token")) {
            // Logged in
            const backendUser = await fetchUser();
            if (backendUser && navAuth) {
                navAuth.innerHTML = `
                    <span class="text-gray-700 mr-4">Hi, ${backendUser.name || 'User'}</span>
                    <a href="${backendUser.role === 'admin' ? 'admin.html' : 'profile.html'}" class="text-violet-600 hover:text-violet-900 font-medium">Dashboard</a>
                    <button id="logout-btn" class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md font-medium hover:bg-gray-300 transition ml-4">Logout</button>
                `;
                document.getElementById('logout-btn').addEventListener('click', handleLogout);
            }
        } else {
            // Not logged in (default state in HTML)
        }
    });
});
