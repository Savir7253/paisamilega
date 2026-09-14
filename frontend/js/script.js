const form = document.getElementById("predictionForm");

const result = document.getElementById("result");


form.addEventListener("submit", async function (event) {

    event.preventDefault();


    // Get values

    const state =
        document.getElementById("state").value;

    const city =
        document.getElementById("city").value;

    const material =
        document.getElementById("material").value;

    const quality =
        document.getElementById("quality").value;

    const weight =
        document.getElementById("weight").value;

    const date =
        document.getElementById("date").value;


    result.innerHTML = "Predicting...";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    state: state,

                    city: city,

                    material: material,

                    quality: quality,

                    weight: weight,

                    date: date

                })
            }
        );


        const data = await response.json();


        if (data.success) {

            result.innerHTML = `
                <h2>Prediction Result</h2>

                <p>
                    Price per kg:
                    <strong>₹${data.price_per_kg}</strong>
                </p>

                <p>
                    Weight:
                    <strong>${data.weight} kg</strong>
                </p>

                <p>
                    Estimated Total Value:
                    <strong>₹${data.total_price}</strong>
                </p>
            `;

        } else {

            result.innerHTML =
                `<p>Error: ${data.error}</p>`;

        }

    }

    catch (error) {

        result.innerHTML =
            `<p>
                Backend server is not running.
             </p>`;

        console.log(error);

    }

});