const API_URL = "http://127.0.0.1:5000";

const token =
    localStorage.getItem("scrapsetu_token");

const userData =
    localStorage.getItem("scrapsetu_user");


if (!token || !userData) {

    window.location.href = "login.html";

}


const user = JSON.parse(userData);


document.getElementById(
    "welcomeMessage"
).innerHTML =
    `Welcome, <strong>${user.name}</strong> 👋`;


// Prediction

function goToPrediction() {

    window.location.href =
        "prediction.html";

}


// Rates

function goToRates() {

    window.location.href =
        "rates.html";

}


// Pickup

function goToPickup() {

    window.location.href =
        "pickup.html";

}


// My pickups

async function viewPickups() {

    const result =
        document.getElementById(
            "dashboardResult"
        );

    result.innerHTML =
        "Loading pickups...";


    try {

        const response =
            await fetch(
                `${API_URL}/api/pickups`,
                {
                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );


        const data =
            await response.json();


        if (!data.success) {

            result.innerHTML =
                `<p>${data.error}</p>`;

            return;

        }


        if (data.pickups.length === 0) {

            result.innerHTML =
                "<p>No pickups booked yet.</p>";

            return;

        }


        let html =
            "<h2>My Pickups</h2>";


        data.pickups.forEach(pickup => {

            html += `

                <div class="pickup-card">

                    <h3>
                        ${pickup.material}
                    </h3>

                    <p>
                        Quality:
                        ${pickup.quality}
                    </p>

                    <p>
                        Weight:
                        ${pickup.weight} kg
                    </p>

                    <p>
                        Estimated Price:
                        ₹${pickup.estimated_price}
                    </p>

                    <p>
                        Pickup Date:
                        ${pickup.pickup_date}
                    </p>

                    <p>
                        Pickup Time:
                        ${pickup.pickup_time}
                    </p>

                    <p>
                        Status:
                        <strong>
                            ${pickup.status}
                        </strong>
                    </p>

                </div>

                <hr>

            `;

        });


        result.innerHTML = html;

    }

    catch (error) {

        console.error(error);

        result.innerHTML =
            "<p>Unable to load pickups.</p>";

    }

}


// Logout

function logout() {

    localStorage.removeItem(
        "scrapsetu_token"
    );

    localStorage.removeItem(
        "scrapsetu_user"
    );

    window.location.href =
        "login.html";

}