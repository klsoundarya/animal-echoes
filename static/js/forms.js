// delete button for blog post submit

document.addEventListener("DOMContentLoaded", function () {
    const clearFormBtn = document.getElementById("clearFormBtn");

    if (clearFormBtn) {
        clearFormBtn.addEventListener("click", function () {
            const inputs = document.querySelectorAll("input, textarea");
            inputs.forEach(function (input) {
                if (input.name !== "csrfmiddlewaretoken") {
                    input.value = ""; // Clear only non-CSRF fields
                }  
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
                if (input.name !== "csrfmiddlewaretoken") {
                    input.value = ""; // Clear only non-CSRF fields
                }
            });
        });
    }
});
