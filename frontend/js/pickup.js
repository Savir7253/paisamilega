const API_URL = "http://127.0.0.1:5000";

const token =
    localStorage.getItem(
        "scrapsetu_token"
    );


if (!token) {

    window.location.href =
        "login.html";

}


const form =
    document.getElementById(
        "pickupForm"
    );


const result =
    document.getElementById(
        "pickupResult"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const material =
            document.getElementById(
                "material"
            ).value;


        const quality =
            document.getElementById(
                "quality"
            ).value;


        const weight =
            parseFloat(
                document.getElementById(
                    "weight"
                ).value
            );


        const state =
            document.getElementById(
                "state"
            ).value;


        const city =
            document.getElementById(
                "city"
            ).value;


        const address =
            document.getElementById(
                "address"
            ).value;


        const pickup_date =
            document.getElementById(
                "pickup_date"
            ).value;


        const pickup_time =
            document.getElementById(
                "pickup_time"
            ).value;


        result.innerHTML =
            "<p>Booking pickup...</p>";


        try {

            /*
             * First get AI estimated price
             */

            const predictionResponse =
                await fetch(
                    `${API_URL}/predict`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            state,
                            city,
                            material,
                            quality,
                            weight,
                            date: pickup_date

                        })
                    }
                );


            const prediction =
                await predictionResponse.json();


            if (!prediction.success) {

                result.innerHTML =
                    `<p>
                        ${prediction.error}
                    </p>`;

                return;

            }


            /*
             * Now create pickup
             */

            const pickupResponse =
                await fetch(
                    `${API_URL}/api/pickups`,
                    {
                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json",

                            "Authorization":
                                `Bearer ${token}`

                        },

                        body: JSON.stringify({

                            material,
                            quality,
                            weight,

                            estimated_price:
                                prediction.total_price,

                            address,
                            city,
                            pickup_date,
                            pickup_time

                        })
                    }
                );


            const data =
                await pickupResponse.json();


            if (data.success) {

                result.innerHTML = `

                    <h2>✅ Pickup Booked</h2>

                    <p>
                        Pickup ID:
                        <strong>
                            #${data.pickup_id}
                        </strong>
                    </p>

                    <p>
                        Estimated Value:
                        <strong>
                            ₹${prediction.total_price}
                        </strong>
                    </p>

                    <p>
                        Status:
                        <strong>
                            ${data.status}
                        </strong>
                    </p>

                `;

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
                "<p>Something went wrong.</p>";

        }

    }
);


function goDashboard() {

    window.location.href =
        "dashboard.html";

}