const API_URL = "http://127.0.0.1:5000";


// ===============================
// REGISTER
// ===============================

const registerForm =
    document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const name =
                document.getElementById("name").value.trim();

            const email =
                document.getElementById("email").value.trim();

            const password =
                document.getElementById("password").value;

            const confirmPassword =
                document.getElementById("confirmPassword").value;

            const message =
                document.getElementById("authMessage");


            // Check passwords

            if (password !== confirmPassword) {

                message.innerHTML =
                    "<p>Passwords do not match.</p>";

                return;
            }


            message.innerHTML =
                "<p>Creating account...</p>";


            try {

                const response = await fetch(
                    `${API_URL}/api/register`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name: name,
                            email: email,
                            password: password

                        })
                    }
                );


                const data =
                    await response.json();


                if (data.success) {

                    message.innerHTML = `
                        <p>
                            Account created successfully!
                        </p>

                        <p>
                            Redirecting to login...
                        </p>
                    `;


                    setTimeout(() => {

                        window.location.href =
                            "login.html";

                    }, 1500);


                } else {

                    message.innerHTML = `
                        <p>
                            ${data.error}
                        </p>
                    `;

                }

            }

            catch (error) {

                console.error(error);

                message.innerHTML = `
                    <p>
                        Backend server is not running.
                    </p>
                `;

            }

        }
    );

}



// ===============================
// LOGIN
// ===============================

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const email =
                document
                    .getElementById("loginEmail")
                    .value
                    .trim();


            const password =
                document
                    .getElementById("loginPassword")
                    .value;


            const message =
                document.getElementById(
                    "authMessage"
                );


            message.innerHTML =
                "<p>Logging in...</p>";


            try {

                const response = await fetch(
                    `${API_URL}/api/login`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email: email,
                            password: password

                        })
                    }
                );


                const data =
                    await response.json();


                if (data.success) {

                    // Save login information

                    localStorage.setItem(
                        "scrapsetu_token",
                        data.token
                    );


                    localStorage.setItem(
                        "scrapsetu_user",
                        JSON.stringify(data.user)
                    );


                    message.innerHTML = `
                        <p>
                            Login successful!
                        </p>

                        <p>
                            Redirecting...
                        </p>
                    `;


                    setTimeout(() => {

                        window.location.href =
                            "dashboard.html";

                    }, 1000);


                } else {

                    message.innerHTML = `
                        <p>
                            ${data.error}
                        </p>
                    `;

                }

            }

            catch (error) {

                console.error(error);

                message.innerHTML = `
                    <p>
                        Backend server is not running.
                    </p>
                `;

            }

        }
    );

}