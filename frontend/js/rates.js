const API_URL = "http://127.0.0.1:5000";


async function loadRates() {

    const container =
        document.getElementById(
            "ratesContainer"
        );


    try {

        const response =
            await fetch(
                `${API_URL}/api/rates`
            );


        const data =
            await response.json();


        if (!data.success) {

            container.innerHTML =
                `<p>${data.error}</p>`;

            return;

        }


        let html = "";


        data.rates.forEach(rate => {

            html += `

                <div class="rate-card">

                    <h2>
                        ${rate.material}
                    </h2>

                    <p>
                        Category:
                        ${rate.category}
                    </p>

                    <p>
                        Base Rate:
                        <strong>
                            ₹${rate.base_price}/kg
                        </strong>
                    </p>

                </div>

                <hr>

            `;

        });


        container.innerHTML = html;

    }

    catch(error) {

        console.error(error);

        container.innerHTML =
            "<p>Unable to load rates.</p>";

    }

}


function goDashboard() {

    window.location.href =
        "dashboard.html";

}


loadRates();