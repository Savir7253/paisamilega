const API_URL = "http://127.0.0.1:5000";

const form = document.getElementById("predictionForm");
const result = document.getElementById("result");


// Set today's date automatically
const dateInput = document.getElementById("date");

if (dateInput) {

    const today = new Date();

    const year = today.getFullYear();

    const month = String(today.getMonth() + 1).padStart(2, "0");

    const day = String(today.getDate()).padStart(2, "0");

    dateInput.value = `${year}-${month}-${day}`;
}


// Prediction form
form.addEventListener("submit", async function (event) {

    event.preventDefault();


    const state = document.getElementById("state").value.trim();

    const city = document.getElementById("city").value.trim();

    const material = document.getElementById("material").value;

    const quality = document.getElementById("quality").value;

    const weight = Number(document.getElementById("weight").value);

    const date = document.getElementById("date").value;


    // Basic validation
    if (!state || !city || !material || !quality || !weight || !date) {

        result.style.display = "block";

        result.innerHTML = `
            <p style="color:red;">
                Please fill all fields.
            </p>
        `;

        return;
    }


    result.style.display = "block";

    result.innerHTML = `
        <p>⏳ Calculating scrap price...</p>
    `;


    try {

        const response = await fetch(`${API_URL}/predict`, {

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

        });


        const data = await response.json();


        console.log("Prediction response:", data);


        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "Prediction failed"
            );

        }


        result.innerHTML = `

            <h2>Estimated Scrap Value</h2>

            <p>
                <strong>Material:</strong>
                ${material}
            </p>

            <p>
                <strong>Quality:</strong>
                ${quality}
            </p>

            <p>
                <strong>Weight:</strong>
                ${weight} kg
            </p>

            <p>
                <strong>Estimated Price:</strong>
                ₹${data.price_per_kg} / kg
            </p>

            <p>
                <strong>Total Estimated Value:</strong>
                ₹${data.total_price}
            </p>

            <hr>

            <p>
                This is an ML-based estimated scrap value.
                Actual market price may vary.
            </p>

        `;


    } catch (error) {

        console.error("Prediction Error:", error);


        result.innerHTML = `

            <h3 style="color:red;">
                Prediction Failed
            </h3>

            <p>
                ${error.message}
            </p>

            <p>
                Make sure your Flask backend is running at
                <strong>127.0.0.1:5000</strong>.
            </p>

        `;

    }

});