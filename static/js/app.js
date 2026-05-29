document.addEventListener("DOMContentLoaded", function () {

    console.log("DevOps Digger Loaded Successfully");

    const experienceField = document.querySelector(
        'input[name="experience"]'
    );

    if (experienceField) {

        experienceField.addEventListener("change", function () {

            let value = parseInt(this.value);

            if (value < 1) {
                alert("Experience cannot be less than 1 year");
                this.value = 1;
            }

            if (value > 25) {
                alert("Maximum experience allowed is 25 years");
                this.value = 25;
            }

        });

    }

});