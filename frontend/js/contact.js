const API_URL =
    "http://127.0.0.1:5000";


const form =
    document.getElementById(
        "contactForm"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const result =
            document.getElementById(
                "contactResult"
            );


        const name =
            document.getElementById(
                "contactName"
            ).value.trim();


        const email =
            document.getElementById(
                "contactEmail"
            ).value.trim();


        const subject =
            document.getElementById(
                "contactSubject"
            ).value.trim();


        const message =
            document.getElementById(
                "contactMessage"
            ).value.trim();


        result.innerHTML =
            "<p>Sending...</p>";


        try {

            const response =
                await fetch(
                    `${API_URL}/api/contact`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name,
                            email,
                            subject,
                            message

                        })
                    }
                );


            const data =
                await response.json();


            if (data.success) {

                result.innerHTML =
                    "<p>✅ Message sent successfully!</p>";

                form.reset();

            }

            else {

                result.innerHTML =
                    `<p>${data.error}</p>`;

            }

        }

        catch(error) {

            console.error(error);

            result.innerHTML =
                "<p>Unable to send message.</p>";

        }

    }
);