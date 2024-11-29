// delete button for blog post submit

document.addEventListener("DOMContentLoaded", function () {
    const clearFormBtn = document.getElementById("clearFormBtn");

    if (clearFormBtn) {
        clearFormBtn.addEventListener("click", function () {
            const inputs = document.querySelectorAll("input, textarea");
            inputs.forEach(function (input) {
                input.value = "";
            });
        });
    }
});


// clear button for contact page
document.addEventListener("DOMContentLoaded", function () {
    const clearBtn = document.getElementById("clearBtn");

    if (clearBtn) {
        clearBtn.addEventListener("click", function () {
            const inputs = document.querySelectorAll("input, textarea");
            inputs.forEach(function (input) {
                input.value = "";
            });
        });
    }
});
