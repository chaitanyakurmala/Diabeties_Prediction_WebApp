// --- Login ---
document.getElementById("loginForm")?.addEventListener("submit", function (e) {
  e.preventDefault();
  const username = this.username.value;
  const password = this.password.value;

  const stored = localStorage.getItem("registered_" + username);
  if (stored) {
    const user = JSON.parse(stored);
    if (user.password === password) {
      localStorage.setItem("username", username);
      window.location.href = "/dashboard";
    } else {
      alert("Incorrect password");
    }
  } else {
    alert("User not found");
  }
});

// --- Register ---
document.getElementById("registerForm")?.addEventListener("submit", function (e) {
  e.preventDefault();
  const username = this.username.value;
  const password = this.password.value;
  const email = this.email.value;

  const userObj = { username, password, email };
  localStorage.setItem("registered_" + username, JSON.stringify(userObj));
  alert("Registered! You can login now.");
  window.location.href = "/";
});
