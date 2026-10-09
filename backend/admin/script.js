const loginForm = document.getElementById("loginForm");

const message = document.getElementById("message");

loginForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const email = document.getElementById("email").value.trim();

    const password = document.getElementById("password").value.trim();


    if (email === "" || password === "") {

        message.textContent = "Please enter your email and password.";

        return;
    }


    window.location.href = "dashboard.html";

});