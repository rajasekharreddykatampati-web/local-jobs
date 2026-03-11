import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBgYlhKQw4njJP2MNVCI7e3FCI_PuLw7DA",
  authDomain: "local-job-ac7d9.firebaseapp.com",
  projectId: "local-job-ac7d9",
  storageBucket: "local-job-ac7d9.firebasestorage.app",
  messagingSenderId: "55255571600",
  appId: "1:55255571600:web:1d4c4e812c4893b5374c15",
  measurementId: "G-ENV9JKS5NC"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export { signInWithPopup, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged };
